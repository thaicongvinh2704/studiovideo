from PIL import Image
from studio.service import Service,filehash
from studio.fixture import create_fixture
from studio.contracts import Mutation,Node,uid

def m(p,data):return Mutation(expected_revision=p['revision'],actor='ui',change_reason='Kiểm chứng asset replacement',idempotency_key=uid('test'),data=data)

def test_v10_asset_replace_preserves_source_motion_and_other_spans(tmp_path):
    service=Service(tmp_path/'studio');pid=create_fixture(service)['project_id'];one=tmp_path/'one.png';two=tmp_path/'two.png'
    Image.new('RGB',(8,8),'red').save(one);Image.new('RGB',(8,8),'blue').save(two)
    p=service.store.get(pid);registered=service.register_asset(pid,m(p,{'license_record':{'source':'synthetic test pixels'}}),one)['result'];oldid=registered['asset_id']
    p=service.store.get(pid);plan=p['plan'];plan['scenes'][2]['nodes'].append(Node(id='test_image',kind='image',asset_id=oldid,x=1500,y=700,width=80,height=80,keyframes={'x':[{'sample':32*48000,'value':1500,'easing':'hold'}]}).model_dump())
    service.write_plan(pid,m(p,{'plan':plan}));p=service.store.get(pid);service.commit(pid,m(p,{}));p=service.store.get(pid);service.compile(pid,m(p,{}));p=service.store.get(pid);before=[x['dependency_hash'] for x in p['timeline']['spans']]
    oldhash=filehash(service.store.root/'projects'/pid/p['assets'][0]['path']);keyframes=p['plan']['scenes'][2]['nodes'][-1]['keyframes']
    replaced=service.replace_asset(pid,m(p,{'asset_id':oldid,'scene_ids':['scene_3'],'license_record':{'source':'synthetic test pixels'}}),two)['result']
    p=service.store.get(pid);assert p['plan']['scenes'][2]['nodes'][-1]['asset_id']==replaced['new_asset_id'];assert p['plan']['scenes'][2]['nodes'][-1]['keyframes']==keyframes
    assert filehash(service.store.root/'projects'/pid/p['assets'][0]['path'])==oldhash
    service.commit(pid,m(p,{}));p=service.store.get(pid);service.compile(pid,m(p,{}));after=[x['dependency_hash'] for x in service.store.get(pid)['timeline']['spans']]
    assert before[:2]==after[:2] and before[2]!=after[2]
