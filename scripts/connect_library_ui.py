from pathlib import Path
p=Path(__file__).resolve().parent.parent/'ui/src/main.tsx';text=p.read_text('utf-8')
if "from './LibraryTools'" not in text:
    text=text.replace("import './style.css';","import './style.css';\nimport {LibraryTools} from './LibraryTools';")
    marker='<section className="panel"><h2>Nhân vật có cấu trúc</h2>'
    assert text.count(marker)==1
    text=text.replace(marker,'<LibraryTools p={p} api={api} act={act} change={change}/>'+marker)
    marker="{j.status==='succeeded'&&['audio_analyze','audio_align'].includes(j.type)&&"
    assert text.count(marker)==1
    text=text.replace(marker,"{j.status==='succeeded'&&['asset_generate','tts_generate'].includes(j.type)&&<button onClick={()=>act(()=>change('assets/accept-job',{job_id:j.id},'Nhận media local vào thư viện'),'Đã đăng ký media; chưa thay audio hoặc gắn vào timeline')}>Nhận vào thư viện</button>}"+marker)
    marker='<section className="panel"><h2>Kết nối một agent</h2>'
    assert text.count(marker)==1
    text=text.replace(marker,'<section className="panel"><h2>Phục hồi backup</h2><p>Tạo dự án mới từ ZIP có checksum; dữ liệu gốc giữ nguyên.</p><input type="file" accept=".zip" onChange={e=>{const file=e.target.files?.[0];if(file)act(async()=>{const form=new FormData();form.append(\'file\',file);return api(\'/restore\',form);},\'Đã phục hồi thành dự án mới trong danh sách\');}}/></section>'+marker)
    p.write_text(text,encoding='utf-8')
print('Shared library, media acceptance and backup restore connected.')
