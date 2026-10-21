"""Adapter for editorial Vietnamese direction; metadata is never speech text."""
import hashlib
import json
from pathlib import Path
import re

from .subtitles import read


def space(text):
    return re.sub(r'\s+', ' ', text).strip()


def read_package(folder, supplied_srt=None):
    folder = Path(folder)
    direction = json.loads((folder/'02_Dao_Dien_Giong_Viet.json').read_text(encoding='utf-8-sig'))
    clean = (folder/'01_Loi_Ke_Sach.txt').read_text(encoding='utf-8-sig')
    srt = folder/'03_Maya_Timecode_Tham_Chieu.srt'
    if direction['language'] != 'vi-VN':
        raise ValueError('Bộ đạo diễn phải dùng tiếng Việt.')
    if hashlib.sha256(srt.read_bytes()).hexdigest() != direction['source_sha256']:
        raise ValueError('SRT không khớp hash nguồn JSON.')
    if supplied_srt and Path(supplied_srt).read_bytes() != srt.read_bytes():
        raise ValueError('SRT người dùng mới gửi khác SRT trong gói; cần đối chiếu trước.')
    cues = direction['source_cues']
    parsed = read(srt)
    if len(parsed) != len(cues) or any(space(a['text']) != space(b['text']) for a,b in zip(parsed,cues)):
        raise ValueError('SRT và source_cues không cùng lời.')
    if space(clean) != space(' '.join(b['text'] for b in direction['beats'])):
        raise ValueError('TXT và beats[].text không cùng lời.')
    by_id = {c['id']:c for c in cues}
    covered = []
    for beat in direction['beats']:
        ids = beat['source_cue_ids']
        if space(beat['text']) != space(' '.join(by_id[i]['text'] for i in ids)):
            raise ValueError('Lời beat khác nội dung nguồn: '+beat['id'])
        if ids != list(range(ids[0],ids[-1]+1)):
            raise ValueError('Cue trong beat không liên tục.')
        covered.extend(ids)
    if covered != [c['id'] for c in cues]:
        raise ValueError('Cue bị bỏ hoặc lặp trong beats.')
    return direction


def cue_offsets(beat, by_id):
    """Offsets address beats[].text; source cues only locate existing words."""
    text = space(beat['text']); cursor = 0; offsets = {}
    for ident in beat['source_cue_ids']:
        fragment = space(by_id[ident]['text'])
        if text[cursor:cursor+len(fragment)] != fragment:
            raise ValueError('Không truy nguyên được lời beat.')
        offsets[ident] = (cursor,cursor+len(fragment))
        cursor += len(fragment)+1
    return text,offsets


def pause_target(beat, end_cue, is_beat_end, default_ms=350):
    events = [e for e in beat.get('pause_events',[]) if e['after_source_cue']==end_cue]
    if len(events)>1:
        raise ValueError('Nhiều pause_events tại cùng ranh giới; cần xử lý ý đồ trước.')
    if events:
        return dict(target_ms=events[0]['ms_target'],source='pause_event',reason=events[0]['reason'],
                    replaces_beat_pause=bool(is_beat_end))
    return dict(target_ms=beat['pause_after_ms_target'] if is_beat_end else default_ms,
                source='beat_end' if is_beat_end else 'semantic_boundary',
                reason='Ranh giới câu/cụm nghĩa; không tách từng dấu phẩy.',replaces_beat_pause=False)


def compile_excerpt(direction, first, last, max_chars=280, default_ms=350):
    by_id={c['id']:c for c in direction['source_cues']}
    protected=direction['rendering']['protected_cue_spans']
    forbidden={i for a,b in protected for i in range(a,b)}
    if first-1 in forbidden or last in forbidden:
        raise ValueError('Trích đoạn cắt vào cụm phải giữ liền.')
    result=[]
    for beat in direction['beats']:
        ids=[i for i in beat['source_cue_ids'] if first<=i<=last]
        if not ids: continue
        text,offsets=cue_offsets(beat,by_id)
        events={e['after_source_cue'] for e in beat.get('pause_events',[])}
        atoms=[]; current=[]
        for ident in ids:
            current.append(ident)
            complete=bool(re.search(r'[.!?][”\"]?$',space(by_id[ident]['text'])))
            if ident in events and (not complete or ident in forbidden):
                raise ValueError('Pause event cần alignment riêng, không được cắt giữa cụm: '+str(ident))
            if complete and ident not in forbidden:
                atoms.append(current);current=[]
        if current:
            if current[-1] != beat['source_cue_ids'][-1]:
                raise ValueError('Trích đoạn dừng giữa một câu chưa hoàn chỉnh.')
            atoms.append(current)
        phrases=beat['delivery'].get('emphasis_phrases',[])
        groups=[]; pending=[]
        def wording(cue_ids):
            return text[offsets[cue_ids[0]][0]:offsets[cue_ids[-1]][1]]
        for atom in atoms:
            atom_text=wording(atom)
            focused=any(p.casefold() in atom_text.casefold() for p in phrases)
            if pending and (len(wording(pending+atom))>max_chars or focused):
                groups.append(pending);pending=[]
            pending.extend(atom)
            if atom[-1] in events or focused:
                groups.append(pending);pending=[]
        if pending:groups.append(pending)
        for group in groups:
            spoken=wording(group)
            if len(spoken)>max_chars:
                raise ValueError('Câu hoàn chỉnh vượt giới hạn; cần chia theo cú pháp, không cắt tự động: '+str(group))
            matches=[p for p in phrases if p.casefold() in spoken.casefold()]
            speed=.98 if beat['delivery']['pace_relative_to_natural_voice']=='chậm hơn nhẹ' else 1.
            gain=0.
            if matches:
                speed*=.99
                gain=.45 if beat['delivery']['emotion_intensity']=='vừa' else .3
            if len(spoken.split())<=4: # A reflective short repeat, not a dramatic shout.
                gain=min(gain,.15)
            end=group[-1];is_beat_end=end==beat['source_cue_ids'][-1]
            pause=pause_target(beat,end,is_beat_end,default_ms)
            if end==last and not is_beat_end and end not in events:
                pause=dict(target_ms=0,source='partial_excerpt_end',reason='Không áp nghỉ cuối beat ở phần trích chưa hết beat.',replaces_beat_pause=False)
            result.append(dict(beat_id=beat['id'],source_cue_ids=group,text=spoken,
                text_origin='beats[].text',pace_multiplier=speed,gain_db=gain,pause=pause,
                matched_emphasis_phrases=matches,emphasis_scope='whole_semantic_unit_not_word_aligned',
                original_editorial_direction=beat['delivery']))
    if space(' '.join(u['text'] for u in result)) != space(' '.join(by_id[i]['text'] for i in range(first,last+1))):
        raise ValueError('Adapter làm mất hoặc lặp lời.')
    boundaries={u['source_cue_ids'][-1] for u in result[:-1]}
    if boundaries & forbidden:
        raise ValueError('Adapter đã cắt cụm bảo vệ.')
    return result


def pause_padding_ms(trailing_ms, leading_ms, target_ms):
    """Only top up existing silence. No trimming or stacking beat/event targets."""
    return max(0.,float(target_ms)-float(trailing_ms)-float(leading_ms))
