from __future__ import annotations
from typing import Literal, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator
from fractions import Fraction
import hashlib, json, re

RATE = 48000
SCHEMA = '1.0'
ENGINE = 'sms-2d-0.2-rig-parts'

def uid(prefix: str) -> str:
    import uuid
    return f'{prefix}_{uuid.uuid4().hex[:16]}'

def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def ceil_div(a: int, b: int) -> int:
    return -(-a // b)

def frame_at(sample: int, num: int = 30, den: int = 1, rule: str = 'not_before') -> int:
    a, b = sample * num, RATE * den
    return ceil_div(a, b) if rule == 'not_before' else (2*a+b)//(2*b)

class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')

class OutputProfile(Strict):
    width: int = Field(default=1920, ge=320, le=3840)
    height: int = Field(default=1080, ge=180, le=2160)
    fps_num: int = Field(default=30, ge=1, le=120)
    fps_den: int = Field(default=1, ge=1, le=1001)
    audio_sample_rate: Literal[48000] = 48000
    video_codec: Literal['h264'] = 'h264'
    audio_codec: Literal['aac'] = 'aac'
    subtitle_mode: Literal['sidecar_srt','burn_in'] = 'sidecar_srt'
    @model_validator(mode='after')
    def even(self):
        if self.width % 2 or self.height % 2:
            raise ValueError('H.264 yêu cầu kích thước chẵn')
        return self

class Policies(Strict):
    agent_mode: Literal['one_active_agent'] = 'one_active_agent'
    paid_ai_providers: Literal['disabled'] = 'disabled'
    external_asset_search: Literal['disabled','enabled'] = 'disabled'
    narration_edits: Literal['preserve','allowed'] = 'preserve'
    tts_replacement: Literal['explicit_project_permission','allowed'] = 'explicit_project_permission'
    automatic_quality_regenerations: Literal[0] = 0
    automatic_transient_retries: Literal[1] = 1
    automatic_ab_variants: Literal[False] = False
    automatic_ai_review: Literal['off'] = 'off'
    gpu_heavy_concurrency: Literal[1] = 1
    silent_quality_downgrade: Literal[False] = False
    publish_to_youtube: Literal[False] = False

class Anchor(Strict):
    audio_revision: str
    word_id: str | None = None
    utterance_id: str | None = None
    manual_sample: int | None = Field(default=None, ge=0)
    evidence: str = ''
    edge: Literal['start','end'] = 'start'
    offset_samples: int = 0
    quantization: Literal['not_before','nearest'] = 'not_before'
    @model_validator(mode='after')
    def one(self):
        if sum(v is not None for v in (self.word_id,self.utterance_id,self.manual_sample)) != 1:
            raise ValueError('Anchor cần đúng một word_id, utterance_id hoặc manual_sample')
        if self.manual_sample is not None and not self.evidence.strip():
            raise ValueError('Mốc thủ công cần bằng chứng')
        return self

class Keyframe(Strict):
    sample: int = Field(ge=0)
    value: float
    easing: Literal['linear','smooth','hold'] = 'linear'

class Node(Strict):
    id: str
    kind: Literal['character','prop','text','image','arrow','path']
    parent_id: str | None = None
    attachment: Literal['hand_left','hand_right'] | None = None
    asset_id: str | None = None
    text: str = ''
    shape: Literal['box','stone','rope','circle'] = 'box'
    x: float = 0
    y: float = 0
    scale: float = 1
    rotation: float = 0
    opacity: float = Field(default=1, ge=0, le=1)
    pivot_x: float = 0
    pivot_y: float = 0
    z: int = 0
    width: float = 200
    height: float = 100
    color: str = '#14b8a6'
    font_size: float = 48
    pose: Literal['neutral','present','point_left','point_right','think','hold','pull'] = 'neutral'
    expression: Literal['neutral','curious','surprised','skeptical','happy'] = 'neutral'
    visible_from: int = 0
    visible_until: int | None = None
    points: list[list[float]] = Field(default_factory=list)
    keyframes: dict[Literal['x','y','scale','rotation','opacity','reveal','highlight'],list[Keyframe]] = Field(default_factory=dict)

class Event(Strict):
    id: str
    scene_id: str
    target_id: str
    action: Literal['pose_swap','expression_swap','reveal','point_at','look_at','attach','text_highlight']
    anchor: Anchor
    duration_samples: int = Field(default=1600, ge=0)
    parameters: dict[str, Any] = Field(default_factory=dict)
    dependency_ids: list[str] = Field(default_factory=list)

class Scene(Strict):
    id: str
    start_sample: int = Field(ge=0)
    end_sample: int = Field(gt=0)
    purpose: str = Field(min_length=1)
    utterance_ids: list[str]
    knowledge_before: str = Field(min_length=1)
    reveal_rules: str = Field(min_length=1)
    emotional_intent: str = Field(min_length=1)
    visual_strategy: str = Field(min_length=1)
    requirements: list[str]
    background: str = '#f5f0e7'
    transition: Literal['cut','dissolve'] = 'cut'
    transition_samples: int = Field(default=0, ge=0)
    camera: dict[Literal['x','y','scale'],list[Keyframe]] = Field(default_factory=dict)
    nodes: list[Node]

class AssetRequest(Strict):
    id: str
    scene_refs: list[str] = Field(min_length=1)
    role: str = Field(min_length=1)
    exact_details: list[str]
    forbidden_details: list[str]
    references: list[str]
    prompt: str = Field(min_length=1)
    prompt_vi: str = Field(min_length=1)
    negative_prompt: str = ''
    workflow_profile: str
    parameters: dict[str,Any]
    layer_requirements: list[str]
    output: dict[str,Any]

class EpisodePlan(Strict):
    schema_version: Literal['1.0'] = '1.0'
    audio_revision: str
    outline: list[str] = Field(min_length=1)
    open_questions: list[str]
    payoff: str = Field(min_length=1)
    narrative_approach: str = Field(min_length=1)
    distinctiveness_notes: str = Field(min_length=1)
    tone: str = 'giải thích'
    opening_promise: str = ''
    visual_balance: str = ''
    pacing_notes: str = ''
    scenes: list[Scene] = Field(min_length=1)
    events: list[Event] = Field(default_factory=list)
    asset_requests: list[AssetRequest] = Field(default_factory=list)
    claims: list[dict[str,Any]] = Field(default_factory=list)
    entities: list[dict[str,Any]] = Field(default_factory=list)

class Mutation(Strict):
    expected_revision: int = Field(ge=0)
    actor: str = 'ui'
    change_reason: str = Field(min_length=1)
    idempotency_key: str = Field(min_length=1, max_length=160)
    lease_token: str | None = None
    data: dict[str,Any] = Field(default_factory=dict)

def parse_srt(data: bytes):
    text = data.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n').strip()
    utterances = []
    pattern = re.compile(r'^(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})$')
    def stamp(raw):
        m = pattern.fullmatch(raw.strip())
        if not m:
            raise ValueError(f'Timestamp SRT không hợp lệ: {raw}')
        h,mm,s,ms = map(int,m.groups())
        if mm >= 60 or s >= 60: raise ValueError('Phút/giây SRT ngoài phạm vi')
        return ((h*3600+mm*60+s)*1000+ms)*48
    for index, block in enumerate(re.split(r'\n\s*\n',text),1):
        lines = block.split('\n')
        if len(lines)<3 or not lines[0].isdigit() or '-->' not in lines[1]:
            raise ValueError(f'Cue {index}: thiếu số, timestamp hoặc lời')
        times=lines[1].split('-->')
        if len(times)!=2: raise ValueError(f'Cue {index}: timestamp sai')
        start,end = map(stamp,times)
        if end<=start: raise ValueError(f'Cue {index}: thời điểm kết thúc phải sau bắt đầu')
        raw='\n'.join(lines[2:])
        utterances.append(dict(id=uid('utt'),source_cue_ids=[lines[0]],raw_text=raw,normalized_text=raw,text_revision=1,start_sample=start,end_sample=end,mismatch_flags=[],method='srt_unverified'))
    if not utterances: raise ValueError('SRT trống')
    return utterances
