import React,{useEffect,useState} from 'react';
export function LibraryTools({p,api,act,change}:any){
 const [shared,setShared]=useState<any[]>([]);
 const refresh=()=>api('/shared/assets').then((r:any)=>setShared(r.result));
 useEffect(()=>{refresh();},[p.id,p.revision]);
 return <section className="panel"><h2>Thư viện dùng chung</h2><p>Tài nguyên được copy theo hash cùng provenance; dự án giữ phiên bản đã đăng ký.</p>{p.assets.length>0&&<details><summary>Đưa một tài nguyên vào thư viện</summary>{p.assets.map((a:any)=><div className="worker" key={a.id}><span>{a.name}</span><button onClick={()=>act(async()=>{await change('assets/share',{asset_id:a.id},'Đưa asset vào thư viện dùng chung');await refresh();},'Đã lưu vào thư viện')}>Lưu dùng chung</button></div>)}</details>}{shared.map((a:any)=><div className="worker" key={a.shared_id}><span>{a.name} · {a.alpha_status}</span><button onClick={()=>act(()=>change('assets/reuse',{shared_id:a.shared_id},'Dùng lại asset đã đăng ký'),'Đã nhập bản pin vào dự án')}>Dùng trong dự án này</button></div>)}{!shared.length&&<p>Chưa có tài nguyên dùng chung.</p>}</section>;
}
