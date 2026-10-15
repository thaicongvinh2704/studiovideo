import json,hashlib,threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pytest
from studio.service import Service,StudioError,filehash
from studio.contracts import Mutation,parse_srt,frame_at,RATE,uid
from studio.fixture import create_fixture

def mutation(p,data=None,key=None):return Mutation(expected_revision=p['revision'],actor='ui',change_reason='Kiểm chứng nền tảng',idempotency_key=key or uid('test'),data=data or {})

@pytest.fixture(scope='module')
def project(tmp_path_factory):
    service=Service(tmp_path_factory.mktemp('Dự án Unicode có khoảng trắng'))
    result=create_fixture(service)
    return service,result['project_id']

def test_v01_source_unicode_and_invalid_srt(project):
    s,pid=project;p=s.store.get(pid)
    for src in p['source_ids']:assert filehash(s.store.root/'projects'/pid/src['path'])==src['content_hash']
    assert 'không' in p['utterances'][0]['raw_text']
    assert 'An' in p['utterances'][0]['raw_text']
    with pytest.raises(ValueError,match='Cue 1'):parse_srt(b'1\ninvalid\nhello')
    with pytest.raises(ValueError,match='kết thúc'):parse_srt('1\n00:00:03,000 --> 00:00:02,000\nkhông'.encode())

def test_v02_clock_long_and_rational():
    for num,den in [(30,1),(30000,1001),(24,1)]:
        for sample in [0,1,672000,450*RATE+131,900*RATE-1]:
            k=frame_at(sample,num,den)
            assert k*RATE*den>=sample*num
            assert (k-1)*RATE*den<sample*num
            assert k*RATE*den-sample*num<RATE*den
    assert frame_at(672000)==420

def test_v04_coverage_and_transition(project):
    s,pid=project;t=s.store.get(pid)['timeline'];spans=t['spans']
    assert spans[0]['start_frame']==0 and spans[-1]['end_frame']==1440
    assert all(a['end_frame']==b['start_frame'] for a,b in zip(spans,spans[1:]))
    assert sum(x['end_frame']-x['start_frame'] for x in spans)==t['frame_count']

def test_v07_revision_conflict_and_one_agent(tmp_path):
    s=Service(tmp_path);p=s.store.create('Conflict fixture');lease=s.store.acquire(p['id'],'agent_a')
    with pytest.raises(StudioError) as e:s.store.acquire(p['id'],'agent_b')
    assert e.value.code=='AGENT_LEASE_CONFLICT'
    barrier=threading.Barrier(2)
    def change(n):
        barrier.wait()
        try:return s.store.mutate(p['id'],mutation(p,{'name':str(n)}),'rename',lambda x:x.update(name=str(n)))['ok']
        except StudioError as e:return e.code
    with ThreadPoolExecutor(2) as pool:results=list(pool.map(change,[1,2]))
    assert results.count(True)==1 and results.count('REVISION_CONFLICT')==1
    assert s.store.release(p['id'],lease['lease_token'])['released']

def test_v06_mutation_idempotency(tmp_path):
    s=Service(tmp_path);p=s.store.create('Idempotency');m=mutation(p,{'name':'new'},'same-key')
    a=s.store.mutate(p['id'],m,'rename',lambda x:x.update(name='new'))
    b=s.store.mutate(p['id'],m,'rename',lambda x:x.update(name='wrong'))
    assert a==b and s.store.get(p['id'])['name']=='new' and s.store.get(p['id'])['revision']==1
    with pytest.raises(StudioError) as e:s.store.mutate(p['id'],mutation(p,{'different':True},'same-key'),'rename',lambda x:None)
    assert e.value.code=='IDEMPOTENCY_CONFLICT'

def test_v05_gain_preserves_video_duration_invalidates(project,tmp_path):
    original,pid=project;backup=original.backup(pid);s=Service(tmp_path);restored=s.restore(backup['path']);pid=restored['project_id'];p=s.store.get(pid)
    s.store.mutate(pid,mutation(p),'permission',lambda x:x['policies'].update(narration_edits='allowed'))
    p=s.store.get(pid);spans=p['timeline']['spans'];sha=p['audio']['pcm_hash']
    s.audio_edits(pid,mutation(p,{'kind':'gain','gain_db':-3}));p=s.store.get(pid)
    assert p['audio']['pcm_hash']!=sha and p['timeline']['spans']==spans
    s.audio_edits(pid,mutation(p,{'kind':'trim','start_sample':2*RATE,'end_sample':3*RATE}));p=s.store.get(pid)
    assert p['timeline'] is None and p['committed_plan'] is None
    assert p['audio']['sample_count']==47*RATE and p['utterances'][1]['start_sample']==15*RATE

def test_v10_restore_and_selective_patch(project,tmp_path):
    s,pid=project;old=s.store.get(pid);backup=s.backup(pid);target=Service(tmp_path);pid=target.restore(backup['path'])['project_id'];p=target.store.get(pid)
    assert p['audio']['pcm_hash']==old['audio']['pcm_hash']
    before=[x['dependency_hash'] for x in p['timeline']['spans']]
    sc=p['plan']['scenes'][2];nodes=sc['nodes'];nodes[0]['text']='Chữ thay đổi cục bộ'
    target.patch_plan(pid,mutation(p,{'patches':[{'collection':'scenes','id':sc['id'],'changes':{'nodes':nodes}}]}))
    p=target.store.get(pid);target.commit(pid,mutation(p));p=target.store.get(pid);target.compile(pid,mutation(p));after=[x['dependency_hash'] for x in target.store.get(pid)['timeline']['spans']]
    assert before[:2]==after[:2] and before[2]!=after[2]
    reopened=Service(tmp_path).store.get(pid);assert reopened['timeline']['hash']==target.store.get(pid)['timeline']['hash']

def test_v08_policy_and_missing_models(project):
    from studio.jobs import Jobs
    s,pid=project;jobs=Jobs(s);p=s.store.get(pid)
    try:
        with pytest.raises(StudioError) as e:jobs.submit(pid,mutation(p,{'profile':'vieneu-turbo-cpu','text':'Xin chào'}),'tts_generate')
        assert e.value.code in ['MODEL_NOT_INSTALLED','POLICY_BLOCKED']
        with pytest.raises(StudioError) as e:jobs.submit(pid,mutation(p,{'profile':'sd15-local','request_id':'missing'}),'asset_generate')
        assert e.value.code in ['MODEL_NOT_INSTALLED','PLAN_NOT_COMMITTED','REFERENCE_MISSING']
    finally:jobs.close()
