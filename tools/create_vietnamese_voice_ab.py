"""Create Vietnamese-only, same-speaker auditions; listening QC stays pending."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.reference_voice import configure_cache, load_profile, postprocess_filters
from studio.vietnamese_narration import apply_readings

DEST = ROOT / 'voices/demos/vietnamese_ab'
PROFILE = ROOT / 'voices/mo_den_EFp49inlLuQ_04.voice.json'
ROWS = [
    dict(id='01_ke_binh_thuong', purpose='Kể bình thường',
         original='Mình là Mỏ Đen. Hôm nay, chúng ta thử nhìn lịch sử từ một chi tiết rất nhỏ: một cuốn sổ đã sờn mép. Những thứ tưởng như bình thường đôi khi lại giữ một câu chuyện rất dài.',
         speed_b=1., gain_b=0., gap_b=.35),
    dict(id='02_tim_dau_vet', purpose='Tò mò, đặt câu hỏi',
         original='Giữa những trang giấy cũ, có một dòng ghi chú bị bỏ dở. Ai đã viết nó, và vì sao câu chuyện dừng lại ở đây?',
         speed_b=.985, gain_b=0., gap_b=.5),
    dict(id='03_to_mo', purpose='Tò mò, gợi suy nghĩ',
         original='Khoan đã. Nếu trang giấy ấy không bị mất, liệu chúng ta có hiểu quá khứ theo một cách khác không?',
         speed_b=.97, gain_b=.3, gap_b=.6),
    dict(id='04_nhan_cam_xuc', purpose='Một điểm nhấn cảm xúc vừa đủ',
         original='Điều khiến mình day dứt không phải là một khoảng trống, mà là những con người có thể đã bị lãng quên. Họ từng sống, từng hy vọng và từng chờ một ngày bình yên.',
         speed_b=.97, gain_b=.7, gap_b=.65),
    dict(id='05_sau_thanh', purpose='Kiểm tra sáu thanh tiếng Việt',
         original='Giờ thử nghe rõ sáu thanh: ma, má, mà, mả, mã, mạ.',
         speed_b=1., gain_b=0., gap_b=.3),
    dict(id='06_so_ngay_don_vi', purpose='Kiểm tra ngày, số thập phân, đơn vị và viết tắt',
         original='Trong ví dụ này, ngày 21/10/2026, An đi 2,5 km đến TP.HCM.',
         readings=[('21/10/2026','hai mươi mốt tháng mười năm hai nghìn không trăm hai mươi sáu','Ngày theo thứ tự ngày/tháng/năm ở Việt Nam; giữ từ ngày đứng trước.'),
                   ('2,5 km','hai phẩy năm ki lô mét','Khoảng cách theo đơn vị ki lô mét, dấu phẩy thập phân.'),
                   ('TP.HCM','thành phố Hồ Chí Minh','Viết tắt địa danh trong câu kể, đọc tên đầy đủ.')],
         speed_b=1., gain_b=0., gap_b=.3),
    dict(id='07_ten_rieng', purpose='Kiểm tra tên riêng và cách đọc từ nước ngoài',
         original='Tên Trần Hưng Đạo, địa danh Hà Nội, từ UNESCO và New York cần được đọc rõ theo ngữ cảnh.',
         readings=[('UNESCO','u nét cô','Cách đọc Việt hóa dùng riêng trong bài thử; vẫn giữ tên gốc để đối chiếu.'),
                   ('New York','Niu Oóc','Cách đọc Việt hóa địa danh trong lời kể tiếng Việt; không chuyển cả câu sang tiếng Anh.')],
         speed_b=1., gain_b=0., gap_b=.35),
    dict(id='08_ket_lang', purpose='Kết lắng, gần gũi',
         original='Không phải câu hỏi nào cũng có đáp án ngay. Nhưng khi biết lắng nghe và kiểm tra bằng chứng, chúng ta sẽ tiến gần hơn đến sự thật.',
         speed_b=.97, gain_b=-.7, gap_b=.55),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ff(*args):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],
                   check=True, creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))


def prepare():
    rows=[]
    for row in ROWS:
        row=dict(row)
        edits=[]
        for expected,spoken,reason in row.pop('readings',[]):
            if row['original'].count(expected)!=1:
                raise ValueError('Cần chọn đúng vị trí cách đọc: '+expected)
            start=row['original'].index(expected)
            edits.append(dict(start=start,end=start+len(expected),expected=expected,
                              spoken=spoken,reason=reason))
        row['spoken'],row['reading_edits']=apply_readings(row['original'],edits)
        if any(c.isdigit() for c in row['spoken']):
            raise ValueError('Bài thử vẫn còn số chưa chuẩn hóa.')
        rows.append(row)
    return rows


def main():
    import numpy as np
    import soundfile as sf
    profile=load_profile(PROFILE)
    if profile.get('delivery',{}).get('selected_version')=='B':
        raise RuntimeError('Bản B đã được người dùng chốt. Không ghi đè WAV và dữ liệu demo đã chọn.')
    if profile.get('language')!='vi-VN' or profile.get('region')!='Bắc':
        raise ValueError('Cần xác nhận tiếng Việt và vùng giọng Bắc trước khi dựng A/B.')
    selected=PROFILE.parent/profile['selected_audition']
    selected_hash=sha(selected)
    if selected_hash!=profile['selected_audition_sha256']:
        raise ValueError('Mẫu đã chọn bị thay đổi.')
    DEST.mkdir(parents=True,exist_ok=True)
    raw_dir=DEST/'raw'; raw_dir.mkdir(exist_ok=True)
    rows=prepare()
    (DEST/'kich_ban_goc.txt').write_text('\n\n'.join(r['original'] for r in rows),encoding='utf-8')
    spoken='\n\n'.join(r['spoken'] for r in rows)
    (DEST/'kich_ban_doc.txt').write_text(spoken,encoding='utf-8')
    (DEST/'doi_chieu_cach_doc.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    configure_cache()
    os.environ['HF_HUB_OFFLINE']='1'
    from vieneu import Vieneu
    from vieneu_utils.phonemize_text import normalize_to_chunks_v3_with_gaps
    tts=Vieneu(mode='v3turbo',device='cpu',backend='onnx',precision='fp32',threads=4)
    with np.load(profile['codes_path'],allow_pickle=False) as data:
        voice=dict(speaker_emb=data['speaker_emb'].astype(np.float32),codes=data['codes'].astype(np.int64))
    for i,row in enumerate(rows):
        seed=20261021+i
        signature=hashlib.sha256(json.dumps(dict(text=row['spoken'],seed=seed,
            codes=profile['codes_sha256'],max_chars=280,temperature=.6,top_k=25),ensure_ascii=False,sort_keys=True).encode()).hexdigest()
        raw=raw_dir/(row['id']+'.wav'); marker=raw.with_suffix('.sha256')
        chunks,gaps=normalize_to_chunks_v3_with_gaps(row['spoken'],max_chars=280)
        row['engine_chunks']=chunks; row['engine_gaps']=gaps
        if not raw.is_file() or not marker.is_file() or marker.read_text()!=signature:
            print(f'Tạo lời {i+1}/{len(rows)}: '+row['purpose'],flush=True)
            np.random.seed(seed)
            audio=np.asarray(tts.infer(row['spoken'],voice=voice,temperature=.6,top_k=25,max_chars=280),dtype=np.float32)
            if not audio.size or not np.isfinite(audio).all():
                raise RuntimeError('Âm thanh lỗi ở '+row['id'])
            sf.write(raw,audio,tts.sample_rate,subtype='PCM_16')
            marker.write_text(signature)
        info=sf.info(raw)
        row['raw_seconds']=info.duration
        row['raw_file']=str(raw.relative_to(DEST))
    raw_seconds=sum(r['raw_seconds'] for r in rows)
    # Use natural generated duration where possible; only a modest common pacing fit.
    gap_a=.3; lead=.18; tail=.5
    estimate=raw_seconds/profile['postprocess']['tempo']+lead+tail+gap_a*(len(rows)-1)
    fit=1. if 47<=estimate<=56 else (raw_seconds/profile['postprocess']['tempo'])/(51-lead-tail-gap_a*(len(rows)-1))
    if not .9<=fit<=1.1:
        raise RuntimeError(f'Cần chỉnh độ dài nội dung thay vì ép nhịp: tự nhiên {estimate:.2f}s, fit {fit:.3f}')
    results=[]
    for version in ['A','B']:
        parts=[np.zeros(round(lead*48000),dtype=np.float32)]; cues=[]; cursor=lead
        for i,row in enumerate(rows):
            local_speed=fit*(row['speed_b'] if version=='B' else 1.)
            local_volume=10**(row['gain_b']/20) if version=='B' else 1.
            output=DEST/(version+'_'+row['id']+'.wav')
            filters=postprocess_filters(profile,local_speed,local_volume)
            ff('-i',DEST/row['raw_file'],'-af',filters,'-ar',48000,'-ac',1,'-c:a','pcm_s16le',output)
            audio,rate=sf.read(output,dtype='float32')
            duration=len(audio)/rate
            cues.append(dict(start=round(cursor,4),end=round(cursor+duration,4),purpose=row['purpose'],
                             text=row['spoken'],speed=local_speed,gain_db=row['gain_b'] if version=='B' else 0,
                             pitch_semitones=profile['postprocess']['pitch_semitones'],raw_sha256=sha(DEST/row['raw_file'])))
            parts.append(audio); cursor+=duration
            if i<len(rows)-1:
                gap=row['gap_b'] if version=='B' else gap_a
                parts.append(np.zeros(round(gap*rate),dtype=np.float32));cursor+=gap
        parts.append(np.zeros(round(tail*48000),dtype=np.float32))
        assembled=DEST/(version+'_ghep.wav')
        sf.write(assembled,np.concatenate(parts),48000,subtype='PCM_16')
        final=DEST/(version+'_giong_ke_tieng_viet.wav')
        ff('-i',assembled,'-af','loudnorm=I=-18:TP=-2:LRA=7,alimiter=limit=0.98:level=false',
           '-ar',48000,'-ac',1,'-c:a','pcm_s16le',final)
        audio,rate=sf.read(final,dtype='float32')
        duration=len(audio)/rate
        if not 45<=duration<=60:
            raise RuntimeError(f'Bản {version} ngoài khoảng 45–60 giây: {duration:.2f}s')
        if not np.isfinite(audio).all() or float(np.max(np.abs(audio)))>=1:
            raise RuntimeError('Lỗi tín hiệu; không đánh giá phát âm từ kiểm tra này.')
        results.append(dict(version=version,file=final.name,seconds=round(duration,3),
                            sha256=sha(final),spoken_text_sha256=hashlib.sha256(spoken.encode()).hexdigest(),cues=cues))
        print(f'Bản {version}: {duration:.3f} giây',flush=True)
    assert sha(selected)==selected_hash
    report=dict(language='vi-VN',region='Bắc',region_source='Người dùng xác nhận',
        model='pnnbao-ump/VieNeu-TTS-v3-Turbo',sdk=importlib.metadata.version('vieneu'),
        backend='ONNX CPU fp32',same_reference_codes_sha256=profile['codes_sha256'],
        shared_raw_speech_between_A_B=True,common_fit=fit,selected_voice_unchanged=True,
        method='A kể đều; B chỉ đổi nhẹ nhịp, khoảng nghỉ, cường độ. Không thêm đường cao độ cảm xúc. Cùng văn bản, mã giọng, và cao độ toàn cục đã chọn.',
        automatic_check_scope='Cơ chế, định dạng, thời lượng, dữ liệu hữu hạn; không kết luận chất lượng nghe.',
        listening_qc={key:'chưa kiểm tra nghe' for key in ['đọc_đủ_lời','sáu_thanh','giọng_Bắc_nhất_quán',
            'số_ngày_đơn_vị','tên_riêng','cụm_nghĩa','tự_nhiên_và_cảm_xúc','sạch_nhạc_nền_của_reference']},
        status='demo_cho_nghe_doi_chieu_chua_danh_dau_dat_chat_luong',rows=rows,results=results)
    (DEST/'bao_cao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':
    main()
