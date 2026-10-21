"""Collect delivered-file evidence after integration and frozen checks complete."""
import hashlib,json,subprocess,sys,wave
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from studio.exporter import binary,FLAGS

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs'/'explainer_v3'
report=json.loads((OUT/'verification.json').read_text(encoding='utf-8'))
assert report['status']=='PASS','Long integration run is not complete'
frozen=json.loads((OUT/'frozen_check'/'runtime_check.json').read_text(encoding='utf-8'))
assert frozen['status']=='PASS' and frozen['frozen']
units=(OUT/'unit_tests.log').read_text(encoding='utf-8');assert 'Ran 33 tests' in units and '\nOK' in units

def probe(path):
    return json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(path)],creationflags=FLAGS))

video=OUT/'history_explainer_1080p.mp4';report['showcase_probe']=probe(video)
report['showcase_sha256']=hashlib.sha256(video.read_bytes()).hexdigest();report['frozen']=frozen
report['unit_tests']=33

def long_audio_spots():
    import numpy as np
    source=ROOT/'examples'/'explainer_showcase'/'assets'/'narration.wav'
    with wave.open(str(source),'rb') as wav:
        rate=wav.getframerate();data=np.frombuffer(wav.readframes(wav.getnframes()),dtype=np.int16).astype(float)
    reference=data[10*rate:11*rate];reference-=reference.mean();errors=[]
    for repeat in (0,9,18):
        t=repeat*68.6+10
        raw=subprocess.check_output([binary('ffmpeg'),'-v','error','-ss',f'{t-.12:.9f}','-i',str(OUT/'long_21min_1080p.mp4'),
            '-t','1.24','-vn','-ar',str(rate),'-ac','1','-f','s16le','pipe:1'],creationflags=FLAGS)
        actual=np.frombuffer(raw,dtype=np.int16).astype(float);actual-=actual.mean()
        n=1<<(len(actual)+len(reference)-2).bit_length()
        corr=np.fft.irfft(np.fft.rfft(actual,n)*np.fft.rfft(reference[::-1],n),n)
        index=int(np.argmax(corr[len(reference)-1:len(actual)]))
        error=index/rate-.12;errors.append(dict(time=t,offset_seconds=error))
        assert abs(error)<.015,errors
    return errors

report['long_audio_spots']=long_audio_spots()
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
old=(ROOT/'TEST_RESULTS.md').read_text(encoding='utf-8')
if not old.startswith('# Kiểm thử Video minh họa V3'):
    summary='''# Kiểm thử Video minh họa V3 — 18/10/2026

- **33/33 unit tests PASS**; log: `outputs/explainer_v3/unit_tests.log`.
- Native UI: biên tập storyboard, chữ, kéo nhóm, cắt lớp, undo, nhân bản/đổi cảnh kèm voice/SRT; playback theo đồng hồ thực đã chạy.
- Thành phẩm mới: **68,6 giây, 1920×1080, 30 FPS, đúng 2.058 frame**, H.264/AAC, audio stereo 48 kHz. Đã giải mã toàn file và kiểm tra các frame trích ra.
- 4K: đoạn thật **3840×2160, 30 FPS, 2 giây, 60 frame**, xuất và ffprobe thành công.
- Bài tải dài: **1.303,4 giây, 21:43,4, 1080p/30 FPS, 39.102 frame**. Dùng 19 lần bộ 8 cảnh, 152 cảnh tổng cộng; đã render và giải mã toàn file. Đây là bài tải lặp, không phải tác phẩm mới dài 21 phút.
- Đồng bộ: 8 tín hiệu âm thanh qua các điểm cắt không trùng frame; stereo tách kênh đúng; nhịp timestamp video đều. Đối chiếu audio đầu/giữa/cuối bài tải dài với voice nguồn bằng tương quan tín hiệu; sai lệch dưới 15 ms.
- Bản **EXE frozen PASS, exit 0**: startup, Piper Việt, save/load, SVG trong project mặc định, FFmpeg export. CLI frozen đã biên dịch storyboard thành 8 cảnh và xác nhận có mã pose mới.
- CLI source đã tạo project portable từ storyboard. Source ZIP phải được đối chiếu sau đóng gói bằng bản nguồn hiện tại.
- Bằng chứng và số đo chi tiết ở `outputs/explainer_v3/verification.json`; screenshot native/frozen, contact sheet và decoded frames cùng thư mục. Thời gian render có thể dùng lại scene cache, không dùng các số này làm cam kết tốc độ cho máy khác.
- Các kiểm tra kỹ thuật không thay thế đánh giá mỹ thuật. Chưa có nhận dạng voice/forced alignment hoặc sinh mọi minh họa từ kịch bản; TXT chia thời gian ước lượng, cần căn theo voice/SRT và biên tập.

---

Các kết quả V2 dưới đây được giữ làm lịch sử của bản cũ.

'''
    (ROOT/'TEST_RESULTS.md').write_text(summary+old,encoding='utf-8')
print('Release evidence complete:',report['long_audio_spots'])
