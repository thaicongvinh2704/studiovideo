from studio.store import Store,StudioError
from studio.contracts import uid
import pytest

def test_completed_job_cache_new_request_key(tmp_path):
    store=Store(tmp_path);p=store.create('Cache');j={'id':uid('job'),'project_id':p['id'],'type':'audio_analyze','idempotency_key':'a','input_hash':'same-audio-model-hash','status':'succeeded','result':{'segments':[]}}
    assert store.put_job(j,{'project_revision':1})[1]
    requested=j|{'id':uid('job'),'idempotency_key':'b','status':'queued'}
    cached,created=store.put_job(requested,{'project_revision':3})
    assert not created and cached['id']==j['id']
    changed=requested|{'input_hash':'other-audio'}
    with pytest.raises(StudioError) as e:store.put_job(changed,{})
    assert e.value.code=='IDEMPOTENCY_CONFLICT'

def test_agent_exclusive_across_projects(tmp_path):
    store=Store(tmp_path);a=store.create('A');b=store.create('B');lease=store.acquire(a['id'],'agent_a')
    with pytest.raises(StudioError) as e:store.acquire(b['id'],'agent_b')
    assert e.value.code=='AGENT_LEASE_CONFLICT'
    store.release(a['id'],lease['lease_token']);assert store.acquire(b['id'],'agent_b')['lease_token']

def test_pending_generation_coalesces_new_request_key(tmp_path):
    store=Store(tmp_path);p=store.create('Pending image');j={'id':uid('job'),'project_id':p['id'],'type':'asset_generate','idempotency_key':'first','input_hash':'full-prompt-model-references','status':'queued','result':None}
    store.put_job(j,{})
    requested=j|{'id':uid('job'),'idempotency_key':'second'}
    existing,created=store.put_job(requested,{})
    assert not created and existing['id']==j['id'] and len(store.jobs(p['id']))==1
