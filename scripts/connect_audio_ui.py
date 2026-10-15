from pathlib import Path
p=Path(__file__).resolve().parent.parent/'ui/src/main.tsx';text=p.read_text('utf-8')
if "from './AudioTools'" not in text:
    text=text.replace("import './style.css';","import './style.css';\nimport {AudioTools} from './AudioTools';")
    old='<section className="panel"><h2>Câu và điểm cần đối chiếu</h2>'
    assert text.count(old)==1
    text=text.replace(old,'<AudioTools p={p} doctor={doctor} act={act} change={change}/>'+old)
    p.write_text(text,encoding='utf-8')
print('Audio tools connected to existing service API.')
