from __future__ import annotations
import sqlite3, json, threading, time
from pathlib import Path
from .contracts import uid, digest, SCHEMA, Policies, OutputProfile

class StudioError(Exception):
    def __init__(self, code, message, details=None, status=400):
        self.code,self.message,self.details,self.status=code,message,details or {},status
        super().__init__(message)

class Store:
    def __init__(self,root: Path):
        self.root=root.resolve(); self.root.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock()
        self.db=sqlite3.connect(self.root/'studio.sqlite',check_same_thread=False)
        self.db.row_factory=sqlite3.Row
        version=self.db.execute('PRAGMA user_version').fetchone()[0]
        if version==1:
            backup_path=self.root/'studio.schema1.backup.sqlite'
            if not backup_path.exists():
                with sqlite3.connect(backup_path) as backup:self.db.backup(backup)
        if version>2:raise StudioError('SCHEMA_INCOMPATIBLE','DB mới hơn phiên bản core này')
        self.db.executescript('''
          PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;
          CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, revision INTEGER, state TEXT);
          CREATE TABLE IF NOT EXISTS revisions(project_id TEXT, revision INTEGER, actor TEXT, reason TEXT, state TEXT, created REAL, PRIMARY KEY(project_id,revision));
          CREATE TABLE IF NOT EXISTS mutations(project_id TEXT, key TEXT, hash TEXT, response TEXT, PRIMARY KEY(project_id,key));
          CREATE TABLE IF NOT EXISTS leases(project_id TEXT PRIMARY KEY, actor TEXT, token TEXT, expiry REAL);
          CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, project_id TEXT, type TEXT, key TEXT, input_hash TEXT, snapshot TEXT, state TEXT, UNIQUE(project_id,key));
          CREATE TABLE IF NOT EXISTS history(project_id TEXT PRIMARY KEY, summary TEXT);
          CREATE TABLE IF NOT EXISTS job_requests(project_id TEXT, key TEXT, input_hash TEXT, job_id TEXT, PRIMARY KEY(project_id,key));
          PRAGMA user_version=2;
        ''')
        self.db.commit()
        for folder in ['shared/assets','shared/profiles','models','projects']: (self.root/folder).mkdir(parents=True,exist_ok=True)

    def get(self,pid):
        with self.lock:
            row=self.db.execute('SELECT state FROM projects WHERE id=?',(pid,)).fetchone()
            if not row: raise StudioError('PROJECT_NOT_FOUND','Không tìm thấy dự án',status=404)
            return json.loads(row[0])

    def list(self):
        with self.lock:
            return [self.summary(json.loads(r['state'])) for r in self.db.execute('SELECT state FROM projects ORDER BY rowid DESC')]

    def summary(self,p):
        return {k:p[k] for k in ['id','name','revision','content_status','validation_status','output_profile','policies']} | {'audio_revision':(p.get('audio') or {}).get('id'),'scenes':len((p.get('plan') or {}).get('scenes',[])), 'assets':len(p['assets']),'issues':p['issues']}

    def create(self,name,policies=None,profile=None):
        pid=uid('project')
        p=dict(id=pid,name=name,schema_version=SCHEMA,revision=0,language='vi',content_status='imported',validation_status='not_checked',policies=Policies(**(policies or {})).model_dump(),output_profile=OutputProfile(**(profile or {})).model_dump(),source_ids=[],audio=None,utterances=[],words=[],plan=None,committed_plan=None,timeline=None,assets=[],issues=[],exports=[],channel_profile={'id':uid('channel'),'revision':1,'style_refs':[],'audience_assumption':'','tone_limits':[],'preferences_with_scope':[]})
        with self.lock,self.db:
            self.db.execute('INSERT INTO projects VALUES(?,?,?)',(pid,0,json.dumps(p,ensure_ascii=False)))
            self.db.execute('INSERT INTO revisions VALUES(?,?,?,?,?,?)',(pid,0,'ui','Tạo dự án',json.dumps(p,ensure_ascii=False),time.time()))
        for folder in ['source','working','plans','assets','cache','exports','reports']:(self.root/'projects'/pid/folder).mkdir(parents=True)
        self.snapshot(p)
        return p

    def snapshot(self,p):
        with self.lock:
            current=self.get(p['id'])
            target=self.root/'projects'/p['id']/'manifest.json'
            tmp=target.with_suffix('.tmp');tmp.write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(target)

    def check_writer(self,pid,actor,token):
        lease=self.db.execute('SELECT * FROM leases WHERE project_id=?',(pid,)).fetchone()
        if actor!='ui' and (not lease or lease['expiry']<=time.time() or lease['actor']!=actor or lease['token']!=token):
            raise StudioError('AGENT_LEASE_CONFLICT','Agent cần lease còn hiệu lực',status=409)
        if actor!='ui' and lease:
            self.db.execute('UPDATE leases SET expiry=? WHERE project_id=?',(time.time()+900,pid))

    def mutate(self,pid,m,operation,fn):
        payload_hash=digest({'operation':operation,'data':m.data,'actor':m.actor,'expected_revision':m.expected_revision,'change_reason':m.change_reason})
        with self.lock,self.db:
            self.db.execute('BEGIN IMMEDIATE')
            cached=self.db.execute('SELECT hash,response FROM mutations WHERE project_id=? AND key=?',(pid,m.idempotency_key)).fetchone()
            if cached:
                if cached['hash']!=payload_hash: raise StudioError('IDEMPOTENCY_CONFLICT','Key đã dùng với nội dung khác',status=409)
                return json.loads(cached['response'])
            p=self.get(pid)
            self.check_writer(pid,m.actor,m.lease_token)
            if p['revision']!=m.expected_revision:
                raise StudioError('REVISION_CONFLICT','Dự án đã đổi; đọc delta trước khi sửa',{'current_revision':p['revision']},409)
            result=fn(p) or {}
            p['revision']+=1
            self.db.execute('UPDATE projects SET revision=?,state=? WHERE id=?',(p['revision'],json.dumps(p,ensure_ascii=False),pid))
            self.db.execute('INSERT INTO revisions VALUES(?,?,?,?,?,?)',(pid,p['revision'],m.actor,m.change_reason,json.dumps(p,ensure_ascii=False),time.time()))
            response={'ok':True,'project_id':pid,'revision':p['revision'],'result':result,'issues':p['issues']}
            self.db.execute('INSERT INTO mutations VALUES(?,?,?,?)',(pid,m.idempotency_key,payload_hash,json.dumps(response,ensure_ascii=False)))
        self.snapshot(p)
        return response

    def acquire(self,pid,actor):
        if actor=='ui': raise StudioError('INVALID_ACTOR','Tên phiên agent phải khác ui')
        self.get(pid)
        with self.lock,self.db:
            other=self.db.execute('SELECT actor,project_id,expiry FROM leases WHERE expiry>? AND actor<>?',(time.time(),actor)).fetchone()
            if other:raise StudioError('AGENT_LEASE_CONFLICT','Studio chỉ có một phiên agent ghi tại một thời điểm',dict(other),409)
            row=self.db.execute('SELECT * FROM leases WHERE project_id=?',(pid,)).fetchone()
            if row and row['expiry']>time.time(): raise StudioError('AGENT_LEASE_CONFLICT','Có agent đang giữ quyền ghi',{'actor':row['actor'],'expiry':row['expiry']},409)
            token=uid('lease');expiry=time.time()+900
            self.db.execute('INSERT OR REPLACE INTO leases VALUES(?,?,?,?)',(pid,actor,token,expiry))
        return {'lease_token':token,'expiry':expiry,'actor':actor}

    def release(self,pid,token):
        with self.lock,self.db:
            changed=self.db.execute('DELETE FROM leases WHERE project_id=? AND token=?',(pid,token)).rowcount
        return {'released':bool(changed)}

    def changes(self,pid,since):
        p=self.get(pid)
        with self.lock:
            rows=self.db.execute('SELECT revision,actor,reason,created FROM revisions WHERE project_id=? AND revision>?',(pid,since)).fetchall()
        return {'revision':p['revision'],'changes':[dict(r) for r in rows],'issues':p['issues']}

    def put_job(self,j,snapshot):
        with self.lock,self.db:
            alias=self.db.execute('SELECT input_hash,job_id FROM job_requests WHERE project_id=? AND key=?',(j['project_id'],j['idempotency_key'])).fetchone()
            if alias:
                if alias['input_hash']!=j['input_hash']:raise StudioError('IDEMPOTENCY_CONFLICT','Job key đã dùng với input khác',status=409)
                return self.job(alias['job_id'])[0],False
            old=self.db.execute('SELECT state,input_hash FROM jobs WHERE project_id=? AND key=?',(j['project_id'],j['idempotency_key'])).fetchone()
            if old:
                if old['input_hash']!=j['input_hash']: raise StudioError('IDEMPOTENCY_CONFLICT','Job key đã dùng với input khác',status=409)
                return json.loads(old['state']),False
            candidates=self.db.execute('SELECT state FROM jobs WHERE project_id=? AND type=? AND input_hash=?',(j['project_id'],j['type'],j['input_hash'])).fetchall()
            for row in candidates:
                cached=json.loads(row[0])
                if cached['status'] in ['queued','running','succeeded','blocked','failed','interrupted','cancel_requested','cancelled']:
                    self.db.execute('INSERT INTO job_requests VALUES(?,?,?,?)',(j['project_id'],j['idempotency_key'],j['input_hash'],cached['id']))
                    return cached,False
            self.db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,?)',(j['id'],j['project_id'],j['type'],j['idempotency_key'],j['input_hash'],json.dumps(snapshot,ensure_ascii=False),json.dumps(j,ensure_ascii=False)))
            self.db.execute('INSERT INTO job_requests VALUES(?,?,?,?)',(j['project_id'],j['idempotency_key'],j['input_hash'],j['id']))
        return j,True

    def job(self,jid):
        with self.lock:
            row=self.db.execute('SELECT * FROM jobs WHERE id=?',(jid,)).fetchone()
            if not row: raise StudioError('JOB_NOT_FOUND','Không tìm thấy job',status=404)
            return json.loads(row['state']),json.loads(row['snapshot'])

    def update_job(self,j):
        with self.lock,self.db: self.db.execute('UPDATE jobs SET state=? WHERE id=?',(json.dumps(j,ensure_ascii=False),j['id']))

    def jobs(self,pid=None):
        with self.lock:
            rows=self.db.execute('SELECT state FROM jobs '+('WHERE project_id=? ' if pid else '')+'ORDER BY rowid DESC LIMIT 100',(pid,) if pid else ()).fetchall()
        return [json.loads(r[0]) for r in rows]
