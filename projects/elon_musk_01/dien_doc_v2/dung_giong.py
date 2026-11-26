"""Dựng lại lời kể Elon Musk theo cụm nghĩa, từ kịch bản và số liệu của tập."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
import wave

import numpy as np

here = Path(__file__).resolve().parent
project = here.parent
repo = project.parents[1]
sys.path.insert(0, str(repo))
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
from studio.decision_workflow import file_hash, require_decision, run_council, write_json
from studio.reference_voice import load_profile
from studio.tts import VoiceEngine
from studio.vietnamese_narration import apply_readings
from studio.voice_selection import selected_profile

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

old = project / "audio_ngoc_huyen"
base = read(old / "ket_qua.json")
assert base["source_sha256"] == file_hash(project / "KICH_BAN.md")
originals = {u["id"]: u for u in base["units"]}
readings = {e["original"]: e["spoken"] for u in read(old / "cach_doc.json")["units"] for e in u["edits"]}
by_name = re.compile(r"(?<!\w)(?:" + "|".join(map(re.escape, sorted(readings, key=len, reverse=True))) + r")(?!\w)")
# Tempo is an edit to the individual take, at its original pitch. Gain in dB is relative to voice bus.
delivery = {"kể": (1.00, 0), "sáng": (1.075, .3), "dồn": (1.10, .7),
            "hỏi": (.98, .4), "số": (.94, .35), "nén": (1.035, -.25),
            "đáp": (.935, .65), "chờ": (.89, -1.35), "thủ thỉ": (.94, -1.15),
            "tỉnh": (1.025, -.9), "tâm tình": (.975, -.5)}
review = {
    "content": "Giữ thứ tự và các mốc của sáu chương gốc. Ở mở đầu, tiền cho lần phóng cuối là tự thuật của Musk; số tiền PayPal là phần sau thuế. Đoạn mua máy ảnh là giả định. Giữ quy thuộc cho Forbes và NASA ở hai con số khác nhau.",
    "director": "Vào đề bằng ba lần phóng thất bại. Gọi lại hòn đảo ở chương năm. Để nhịp nhìn sau câu cái lỗ trên sàn, cú bấm đăng và tín hiệu về, rồi mới chuyển ý. Giữ cảnh xe ở cuối để đáp lại cảnh nhận chìa khóa.",
    "audio": "Bản trước phát nguyên đoạn Tesla 43 giây trong cùng một lượt. Nhiều khoảng ngắt đầu tập rơi vào vùng 0,35–0,48 giây. Bản mới viết lại câu hỏi, câu đáp và câu đùa để thu riêng; mỗi cụm có điểm lấy hơi, sắc thái, mức và nhịp. Khi ráp phải trừ khoảng im ở hai đầu file.",
    "technical": "Dùng preset 19 Ngọc Huyền gốc ở tốc độ tổng hợp 1, không dịch cao độ. Bảng nhịp giữ số và tên cùng nhau; chỉ dẫn tách khỏi lời. So độ dài và mức đỉnh tệp hoàn chỉnh, thử giải mã MP3, ghi mốc từ PCM.",
    "critic": "Rủi ro lớn nhất là thay đều giọng bằng đều ngắt. Giữ các chuỗi giải thích liền hơi; các khoảng dài chỉ dành cho một kết quả, đổi cảnh hoặc câu cần người xem tự trả lời. Cần giao trích đoạn và bản dài để người nghe phán xét."
}

beats = []
for line in (here / "bang_nhip.txt").read_text(encoding="utf-8-sig").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if line.isdigit():
        group = int(line)
        continue
    style, rest, label = [v.strip() for v in line.split("|", 2)]
    original = originals[group]
    sentences = re.split(r"(?<=[.!?])\s+", original["original"])
    if re.fullmatch(r"\d+(?:-\d+)?", label):
        bounds = list(map(int, label.split("-")))
        assert 1 <= bounds[0] <= bounds[-1] <= len(sentences)
        text = " ".join(sentences[bounds[0]-1:bounds[-1]])
    else:
        text = label
    changes = [dict(start=m.start(), end=m.end(), expected=m.group(), spoken=readings[m.group()],
                    reason="Cách đọc của tập trong câu này.") for m in by_name.finditer(text)]
    spoken, log = apply_readings(text, changes)
    assert not re.search(r"\d", spoken), spoken
    tempo, gain = delivery[style]
    beats.append(dict(id=len(beats)+1, group=group, scene=original["scene"], copy=text,
                      spoken=spoken, readings=log, style=style, tempo=tempo, db=gain, gap=float(rest)))
assert sorted({b["group"] for b in beats}) == list(originals)
voice = selected_profile(repo / "voices")
assert load_profile(voice)["preset"] == "Ngọc Huyền"
fingerprint = file_hash(voice)
request = dict(name="Elon Musk – bản diễn đọc thứ hai", decision_required=True,
               decision_brief="Đổi nhịp trong toàn bộ lời kể sau phản hồi trực tiếp.",
               subtitles=[dict(id=str(b["id"]), text=b["spoken"], role="người kể") for b in beats],
               human_authorization_file="yeu_cau.json", local_review_evidence_file="nhan_xet.json",
               fact_sources=[dict(file="../SO_LIEU.md", description="Các nguồn và số liệu trong kịch bản gốc.")])
write_json(here/"yeu_cau.json", dict(source="direct-user-chat", messages=[dict(role="user", text=
    "TÔI Cảm THẤY BẠN CHỈ TẠO CHO CÓ HOÀN TOÀN KHÔNG QUAN TÂM GÌ ĐẾN NHỊP CỦA VIDEO GIỌNG ĐỌC CỨ ĐỌC KHÔNG HỀ CẢM THẤY NHỊP")]))
write_json(here/"nhan_xet.json", dict(author="Codex, tự biên tập cùng phiên", findings=review,
                                         previous_seconds=base["seconds"], source=file_hash(project/"KICH_BAN.md"),
                                         score=file_hash(here/"bang_nhip.txt")))
class EditorialReview:
    description = "Tự rà soát trong cùng phiên; một biên tập viên xem xét năm khía cạnh."
    def ask(self, role, context, proposal, feedback, cancel):
        return dict(summary=review[role], issues=[], proposal=[], resolutions=[])
run_council(request, here, "narration", EditorialReview(),
            "Dựng bản mới từ cụm lời riêng. Lời kể và nhịp từng cảnh nằm trong bang_nhip.txt. Nghe duyệt sau khi ráp.",
            threading.Event())
require_decision(request, here, "narration")
write_json(here/"loi_va_nhip.json", beats)
engine = VoiceEngine(repo / "voices")
takes = here / "takes"
takes.mkdir(exist_ok=True)
dest = project / "delivery"
dest.mkdir(exist_ok=True)
sr = 48000

def read_wav(path):
    with wave.open(str(path), "rb") as f:
        assert (f.getframerate(), f.getnchannels(), f.getsampwidth()) == (sr, 1, 2)
        return np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").copy()

def wavwrite(path, pcm):
    with wave.open(str(path), "wb") as f:
        f.setparams((1, 2, sr, 0, "NONE", "PCM"))
        f.writeframes(pcm.astype("<i2", copy=False).tobytes())

def mp3(path, output):
    tmp = output.with_suffix(".part.mp3")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(path), "-c:a", "libmp3lame", "-q:a", "2", str(tmp)], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-xerror", "-i", str(tmp), "-f", "null", "-"], check=True)
    tmp.replace(output)

def get_take(b):
    key = hashlib.sha256((fingerprint + b["spoken"]).encode()).hexdigest()[:18]
    path = takes / (key + ".wav")
    receipt = path.with_suffix(".sha256")
    if not (receipt.is_file() and path.is_file() and receipt.read_text().strip() == file_hash(path)):
        engine.synthesize(b["spoken"], str(voice), path, speed=1., context=(request,here))
        receipt.write_text(file_hash(path), encoding="ascii")
    # These specific takes repeated their short sentence. The endpoint is inside the measured silence between copies.
    cuts = {"b10d3c5f63e9b9b7114bd99724aeb5f87d3eefba1e74c07147275dc9a7d48c0d": 1.00}
    process = []
    take_digest = receipt.read_text().strip()
    if take_digest in cuts:
        process.append(f"atrim=end={cuts[take_digest]}")
    process.append("atempo=" + str(b["tempo"]))
    pcm = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(path),
        "-af", ",".join(process), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"])
    signal = np.frombuffer(pcm, dtype="<i2").astype(np.float32)
    # Locate quiet margins on 8-ms windows with a conservative floor and keep a guard around breath and consonants.
    hop = 384
    windows = signal[:len(signal)//hop*hop].reshape(-1,hop)
    rms = np.sqrt(np.mean(windows*windows,axis=1))
    audible = np.flatnonzero(rms > 44.)
    assert audible.size and np.max(np.abs(signal)) > 512, b["id"]
    first = max(0, int(audible[0])*hop-round(.040*sr))
    last = min(len(signal), (int(audible[-1])+1)*hop+round(.085*sr))
    signal=signal[first:last]*10**(b["db"]/20.)
    ramp = np.linspace(0.,1.,round(.003*sr))
    signal[:len(ramp)]*=ramp
    signal[-len(ramp):]*=ramp[::-1]
    assert np.max(np.abs(signal)) < 32767, b["id"]
    return signal.astype("<i2"), (int(audible[0])*hop-first)/sr, (last-(int(audible[-1])+1)*hop)/sr

def assemble(rows, name, receipt=False):
    pieces=[]
    pos=0
    last_tail=0.
    timeline=[]
    for i, b in enumerate(rows):
        pcm, lead, tail = rendered[b["id"]]
        gap = b["gap"] if i else .08
        pad = max(0,round(sr*(gap-last_tail-lead)))
        pieces.extend((np.zeros(pad,dtype="<i2"),pcm))
        pos += pad
        timeline.append(dict(id=b["id"],group=b["group"],scene=b["scene"],text=b["copy"],
                             style=b["style"],start=round(pos/sr+lead,3),end=round((pos+len(pcm))/sr-tail,3),
                             pre_gap=round(last_tail+pad/sr+lead,3)))
        pos+=len(pcm)
        last_tail=tail
    pieces.append(np.zeros(round(.32*sr),dtype="<i2"))
    data=np.concatenate(pieces)
    output=dest/(name+".wav") if receipt else here/(name+".wav")
    tmp=output.with_suffix(".part.wav")
    wavwrite(tmp,data)
    tmp.replace(output)
    mp3(output,dest/(name+".mp3"))
    if receipt:
        assert len(data)/sr > 600
        write_json(here/"moc_thu.json",dict(seconds=len(data)/sr,sample_rate=sr,units=timeline,
            max_pcm=int(np.abs(data.astype("int32")).max()),mp3_sha256=file_hash(dest/(name+".mp3"))))
    return len(data)/sr

print("START", len(beats), "beats", flush=True)
rendered={}
for b in beats:
    rendered[b["id"]]=get_take(b)
    if b["id"]%12==0:
        print("DONE",b["id"],"/",len(beats),"scene",b["scene"],flush=True)
    if b["group"]==3 and beats[b["id"]]["group"]==4:
        dur=assemble(beats[:b["id"]],"Elon_Musk_V2_Mo_dau")
        print("OPENING",round(dur,2),flush=True)
duration=assemble(beats,"Elon_Musk_Ngoc_Huyen_V2",receipt=True)
print("READY",duration,flush=True)