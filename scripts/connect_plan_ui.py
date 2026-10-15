from pathlib import Path
p=Path(__file__).resolve().parent.parent/'ui/src/main.tsx';text=p.read_text('utf-8')
if "from './PlanTools'" not in text:
    text=text.replace("import './style.css';","import './style.css';\nimport {PlanTools} from './PlanTools';")
    marker='<button className="textbutton" onClick={()=>setAdvanced(!advanced)}>'
    assert text.count(marker)==1
    text=text.replace(marker,'<PlanTools p={p} act={act} change={change}/>'+marker)
    text=text.replace("['x','y','scale','rotation','opacity'].map(key=>","['x','y','scale','rotation','opacity','width','height','font_size','z'].map(key=>")
    p.write_text(text,encoding='utf-8')
print('Prompt and event forms connected to API.')
