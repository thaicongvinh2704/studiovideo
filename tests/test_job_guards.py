from types import SimpleNamespace
import pytest
from studio.service import Service,StudioError
from studio.jobs import Jobs
from studio.contracts import uid

def job(p):return {'id':uid('job'),'project_id':p['id'],'type':'tts_generate','idempotency_key':uid('key'),'input_hash':uid('hash'),'status':'running','progress':0,'cursor':0,'checkpoint':{}}

def test_progress_keeps_cancel_request(tmp_path):
    s=Service(tmp_path);p=s.store.create('Cancel race');jobs=Jobs(s);j=job(p);s.store.put_job(j,{})
    try:
        jobs.cancel(j['id']);jobs.update(j,progress=.4)
        assert s.store.job(j['id'])[0]['status']=='cancel_requested'
    finally:jobs.close()

def test_v08_resource_guard_before_model_load(tmp_path,monkeypatch):
    s=Service(tmp_path);p=s.store.create('Resource guard');jobs=Jobs(s);j=job(p)
    try:
        monkeypatch.setattr('studio.jobs.psutil.virtual_memory',lambda:SimpleNamespace(available=1048576))
        with pytest.raises(StudioError) as e:jobs.execute(j,{'project':p,'worker_profile':{'min_ram_mb':1000}})
        assert e.value.code=='RESOURCE_INSUFFICIENT'
        monkeypatch.setattr('studio.jobs.psutil.virtual_memory',lambda:SimpleNamespace(available=10000*1048576))
        monkeypatch.setattr('studio.service.run',lambda *a,**kw:b'10\n')
        with pytest.raises(StudioError) as e:jobs.execute(j,{'project':p,'worker_profile':{'min_ram_mb':1000,'min_vram_mb':1000}})
        assert e.value.code=='RESOURCE_INSUFFICIENT'
    finally:jobs.close()
