# Hợp đồng dữ liệu, timeline và công cụ agent

Phiên bản 1.0 — 14/10/2026. Đây là thiết kế để triển khai, không phải API đã tồn tại. Tên lệnh dưới đây là giao diện mục tiêu của studio; không phải lệnh tích hợp sẵn của Codex/Antigravity.

## 1. Nguyên tắc chung

- ID ổn định cho mọi project, utterance, word, scene, asset, event và job. Không dùng nội dung câu làm khóa duy nhất.
- Thời gian thực thi dùng sample/frame nguyên; dữ liệu UI đổi sang giây để đọc. FPS là cặp tử/mẫu, không số thực gần đúng.
- Core là nguồn ghi duy nhất. UI, CLI và MCP gọi chung service layer. Manifest JSON là snapshot; import phải qua validate/transaction.
- Mỗi thay đổi ghi expected_revision, actor và change_reason; xung đột trả về lỗi, không last-write-wins.
- Raw inputs bất biến. Kết quả sinh mới là artifact mới, không ghi đè nguồn.
- Mỗi job đọc snapshot cố định. Thay đổi giữa lúc job chạy không thay nội dung job đó.
- Text lấy từ SRT, nguồn web hoặc metadata là dữ liệu, không được diễn giải thành chỉ dẫn điều khiển agent hay lệnh shell.

## 2. Layout dự án mục tiêu

| Vùng | Nội dung | Chính sách |
|---|---|---|
| `projects/<id>/source/` | Audio, SRT, file nhập | Bất biến, có hash |
| `projects/<id>/working/` | Audio đã xử lý, alignment, edits | Có revision và time map |
| `projects/<id>/plans/` | Outline, scene briefs, asset requests, timeline snapshots | JSON có schema_version |
| `projects/<id>/assets/` | Asset riêng của tập | Hash + provenance, có thể tham chiếu shared |
| `shared/assets/` | Nhân vật, pose, đạo cụ, nhạc đã đăng ký | Không sửa đè asset được dự án pin |
| `shared/profiles/` | Style, model, workflow, export profiles | Versioned |
| `projects/<id>/cache/` | Preview, render spans, proxy | Có thể dọn theo policy, không dọn file đang dùng |
| `projects/<id>/exports/` | MP4/SRT và manifest đầu ra | Pin theo export job |
| `projects/<id>/reports/` | Issues, phạm vi kiểm tra, thống kê job | Báo trạng thái trung thực |
| `models/` | Models dùng chung hoặc registry trỏ tới đường dẫn khác | Không copy vào mỗi project |
| `studio.sqlite` | Index, revision, job, history, leases | Transaction, migration có backup |

Đường dẫn là quy ước triển khai, không yêu cầu đúng ổ đĩa. Hỗ trợ đường dẫn có khoảng trắng và tiếng Việt, tránh shell interpolation. Backup có manifest/checksum và có thể mở lại mà không phụ thuộc đường dẫn tuyệt đối máy cũ.

## 3. Những object bắt buộc

| Object | Trường chính | Bất biến cần giữ |
|---|---|---|
| Project | id, schema_version, revision, language, output_profile, source_ids, policies, channel_profile_id | Revision tăng khi semantic state đổi |
| AudioRevision | id, source_hash, pcm_hash, sample_rate, sample_count, edit_map, parent_id | Anchors và alignment phải trỏ đúng audio này |
| Utterance | id, source_cue_ids, raw_text, normalized_text, text_revision, start_sample, end_sample, mismatch_flags | Giữ raw_text; không mất dấu phủ định/đơn vị khi normalize |
| WordAnchor | id, utterance_id, token_index, text, start_sample, end_sample, method, evidence_status, audio_revision | Token lặp vẫn có ID riêng; từ không căn được không có timestamp giả |
| Claim | id, utterance_ids, assertion, certainty_type, source_refs, verification_status | Phân biệt verified, unverified, disputed; không suy từ confidence AI |
| Entity | id, names, role, period, appearance_ref, pronunciation_note | Phân biệt người kể/nhân vật/đối tượng được nhắc |
| ChannelProfile | id, revision, style_refs, audience_assumption, tone_limits, preferences_with_scope | Gu của một video không tự thành quy tắc cả kênh |
| EpisodePlan | revision, audio_revision, outline, open_questions, payoff, narrative_approach, distinctiveness_notes | Một kế hoạch toàn bài dẫn hướng các chương |
| SceneBrief | id, purpose, utterance_ids, knowledge_before, reveal_rules, emotional_intent, visual_strategy, requirements | Có ý nghĩa kể chuyện trước khi có prompt |
| AssetRequest | id, scene_refs, role, exact_details, references, prompt, workflow_profile, parameters, layer_requirements | Chỉ chạy khi preflight hợp lệ; không dùng default ngầm cho ràng buộc quan trọng |
| Asset | id, content_hash, media_type, dimensions, alpha_status, source, license_record, generation_record, revision | Không coi checkerboard/nền trắng là alpha |
| CharacterRig | id, revision, parts, pivots, attachments, poses, expressions, supported_actions | Mỗi action phải được capability check |
| TimelineEvent | id, target_id, action, anchor, duration, parameters, dependency_ids | Resolve ra sample/frame theo một quy tắc thống nhất |
| RenderSpan | id, start_frame, end_frame, dependency_hash, render_profile_hash, status, output_hash | Khoảng nửa mở; không lặp/thiếu frame |
| Job | id, type, input_revision, input_hash, idempotency_key, status, checkpoint, resource_profile, attempts | Gọi lặp không sinh thêm job logic |
| Issue | id, severity, object_ids, time_range, evidence, proposed_action, status, source | Bằng chứng và phạm vi rõ; không chỉ ghi “quality low” |
| EpisodeHistory | project_id, summary, approach, notable_layouts, actions, opening, ending, feedback_scope | Tóm tắt gọn; không đưa mọi media vào context |

## 4. Chính sách mặc định cần thể hiện trong dữ liệu

Ví dụ cấu hình đề xuất, không phải code của ứng dụng:

```json
{
  "schema_version": "1.0",
  "policies": {
    "agent_mode": "one_active_agent",
    "paid_ai_providers": "disabled",
    "external_asset_search": "disabled",
    "narration_edits": "preserve",
    "tts_replacement": "explicit_project_permission",
    "automatic_quality_regenerations": 0,
    "automatic_transient_retries": 1,
    "automatic_ab_variants": false,
    "automatic_ai_review": "off",
    "gpu_heavy_concurrency": 1,
    "silent_quality_downgrade": false,
    "publish_to_youtube": false
  },
  "output_profile": {
    "width": 1920,
    "height": 1080,
    "fps_num": 30,
    "fps_den": 1,
    "audio_sample_rate": 48000,
    "video_codec": "h264",
    "audio_codec": "aac",
    "subtitle_mode": "sidecar_srt"
  }
}
```

Quyền narrative_edits có thể đổi cho từng project sau chỉ dẫn người dùng; không tự suy từ việc họ muốn “video hay hơn”. Các giá trị phải được validation và UI hiển thị có nghĩa. Model cục bộ không được cấu hình endpoint ngoài máy dưới nhãn “local”.

## 5. Đồng hồ và anchor

### 5.1 Định nghĩa

- Working audio mặc định 48 kHz; sample index toàn bài là chuẩn logic sau các chỉnh sửa đã commit.
- Frame export `k` được đánh giá ở thời gian `k * fps_den / fps_num` giây.
- Một event cần không sớm hơn anchor được lượng tử hóa bằng ceil sang frame; một event gần nhất có thể dùng round. Lựa chọn lưu trong event, không thay tùy renderer.
- Ở 48 kHz và 30 fps, `samples_per_frame = 1600`. Khi FPS khác, dùng số hữu tỉ, không cộng từng float duration.
- RenderSpan là `[start_frame, end_frame)`. Số frame toàn bài là ceil(audio_duration × fps), trừ khi có outro/hold được khai báo rõ.
- Word alignment có độ bất định riêng. Sai số lượng tử dưới một frame không đồng nghĩa timestamp của ASR chính xác dưới một frame.

### 5.2 Ví dụ có số liệu minh họa

Đây là dữ liệu giả để giải thích hợp đồng, không phải mốc đo từ video mẫu. Từ “đứt” bắt đầu ở sample 672000, tức 14 giây. Hình dây đứt bám vào từ đó; trước mốc này không được hiển thị trạng thái dây đã đứt.

```json
{
  "id": "evt_rope_break",
  "scene_id": "scene_pull_stone",
  "target_id": "rope_main",
  "action": "pose_swap",
  "anchor": {
    "audio_revision": "audio_r3",
    "word_id": "utt_12_word_09",
    "edge": "start",
    "offset_samples": 0,
    "quantization": "not_before"
  },
  "duration_samples": 1600,
  "parameters": {
    "from_pose": "intact",
    "to_pose": "broken"
  },
  "dependency_ids": ["rig_rope_r2", "audio_r3"]
}
```

Anchor resolver đọc WordAnchor đã pin, không tin giá trị thời gian do LLM tự đoán. Event state phải tính đúng khi seek thẳng tới frame sau sự kiện; không phụ thuộc việc callback “đứt dây” đã chạy trước đó.

### 5.3 Sửa audio

Mỗi edit lưu khoảng nguồn và khoảng đích. Giữ lineage của utterance/word ở vùng không đổi, nhưng tạo audio revision mới. Sau đổi thời lượng: ánh xạ anchors vùng giữ nguyên, căn lại vùng chỉnh khi cần, invalidation mọi span có timing/output thay đổi kể cả phía sau điểm cắt. Không giả rằng chỉ scene chứa câu sửa bị ảnh hưởng nếu cả phần sau dịch thời gian.

Khi nội dung từ thay đổi, giữ liên kết cũ ở trạng thái unresolved cho đến khi match hoặc được gắn lại; không tự bám vào từ giống chữ ở câu khác. Sửa chỉ gain không đổi thời gian: cập nhật audio dependency/mix; không phải tạo lại ảnh hoặc render video nếu frame content không đổi.

## 6. Scene graph và chuyển động

Node gồm transform, pivot, parent, z-order, opacity, mask, asset_ref và visibility_range. Keyframe gồm thời điểm, giá trị, easing và đơn vị. Camera transform riêng, không phá tọa độ rig. Một node không được có nhiều action ghi cùng property ở cùng khoảng nếu không có quy tắc blend/priority rõ.

Các khả năng tối thiểu cần có trong capability manifest:

- position/scale/rotation/opacity keyframes; reveal và hold.
- pose swap, expression swap, point_at và look_at dựa trên rig hỗ trợ.
- attachment cho tay–đạo cụ; chuyển động nhóm, thứ tự lớp.
- camera pan/zoom có mục đích, text reveal/highlight, arrow/path reveal.
- cut, dissolve và transition có duration rõ; không ngầm kéo dài tổng timeline.
- asset video playback theo source in/out và timestamp, nếu được hỗ trợ ở giai đoạn tương ứng.

Đi bộ, kéo vật, chèo hoặc mang vật chỉ được công bố khi có recipe/rig cụ thể; không khai capability “arbitrary animation”. V1 cần ít nhất một tương tác thực giữa nhân vật và đạo cụ trong đoạn tích hợp. Chưa yêu cầu mô phỏng vật lý, full IK hoặc tự tách layer từ ảnh bất kỳ.

Mỗi action recipe ghi prerequisites, properties bị tác động, đơn vị, ràng buộc và cách xử lý kết thúc. Renderer kiểm tra mất asset/pivot/pose trước khi render. Bố cục chữ dùng font thực có dấu Việt; không giao model ảnh vẽ chữ quan trọng.

## 7. Giao diện công cụ MCP mục tiêu

Có thể gom những operation gần nhau nếu client giới hạn tool count, nhưng không tạo một tool shell tùy ý thay cho hợp đồng rõ ràng. Dưới đây là tập operation cần đáp ứng.

| Nhóm operation | Input chính | Output gọn | Side effect |
|---|---|---|---|
| `studio_capabilities` | optional profile | action/worker support, schema versions, active agent | Không |
| `studio_health` | scope | readiness, RAM/VRAM, blockers | Không tải model chỉ để kiểm tra |
| `project_create`, `project_import` | source refs, policies | project_id, revision | Có |
| `project_summary`, `project_changes` | id, since_revision | summary/delta/issues | Không |
| `agent_acquire`, `agent_release` | project/session | lease và expiry | Có |
| `audio_analyze` | source/audio revision, profile | job_id hoặc cache hit | Job local |
| `audio_apply_edits` | edit list, expected revision, permission | new revision, affected IDs | Có |
| `audio_align` | audio/transcript revision | job_id/cache hit | Job local |
| `plan_write`, `plan_patch` | validated plan/patch, expected revision | new revision, touched objects | Có |
| `plan_preflight`, `plan_commit` | plan revision | errors/warnings hoặc immutable snapshot | Commit có |
| `asset_search`, `asset_register` | query hoặc local file/provenance | IDs và metadata | Register có |
| `asset_generate` | committed asset request ID | job_id/cache hit | Job local |
| `asset_patch` | asset/part ID, change request | job_id hoặc new asset version | Có, không overwrite |
| `tts_generate` | text, voice/profile, permission | job_id | Job local, không tự ghép vào audio |
| `timeline_compile` | plan snapshot, audio revision | timeline hash, dependencies | Có |
| `render_submit` | timeline hash, spans, profile | job_id/cache hit | Job local |
| `job_status`, `job_cancel`, `job_resume` | job ID, cursor | delta, progress, error code | Cancel/resume có |
| `issues_list`, `issue_resolve` | scope hoặc evidence/action | issue delta | Resolve có |
| `artifact_get` | id, requested representation | local ref hoặc image/audio hợp lệ khi yêu cầu | Không |
| `export_finalize` | compatible span IDs, audio revision | job_id/final refs | Job local |
| `project_checkpoint`, `project_backup` | revision | checkpoint/export ref | Có |

Những operation đặt tên trong bảng là yêu cầu thiết kế. Implementer phải tạo schema/tool description đúng SDK đang dùng, không giả các operation này là API sẵn có của ComfyUI hoặc FFmpeg.

### Response và job contract

- Mọi response: `ok`, `project_id`, `revision`, `result` hoặc `error`; `issues` là danh sách gọn có ID; `next_action` nếu bị chặn.
- Mutation có `expected_revision`, `idempotency_key` và lease token nếu cần.
- Job dài trả job_id ngay; không giữ MCP request chờ render nhiều phút.
- Progress chi tiết qua SSE/WebSocket cho UI; agent đọc summary khi cần, không poll mỗi giây.
- Chỉ gửi log tail đã lọc khi lỗi. Không nhét transcript/ảnh/JSON toàn bài vào mọi response.
- Các provider như ComfyUI phải lưu provider_job_id để tra lại history trước khi retry một submit chưa rõ kết quả.

## 8. Trạng thái và lỗi

Job: `queued → running → succeeded`; có các nhánh `blocked`, `failed`, `cancel_requested → cancelled`, `interrupted`. Checkpoint độc lập với trạng thái; resume không tăng revision nội dung nếu chỉ tiếp tục đúng job.

Project content: `imported`, `audio_ready`, `planning`, `plan_committed`, `assets_ready`, `timeline_ready`, `rendered`. Validation status là trường riêng, không ép mọi trạng thái đi tuyến tính khi một scene được sửa.

| Code lỗi mục tiêu | Hành vi |
|---|---|
| `REVISION_CONFLICT`, `AGENT_LEASE_CONFLICT` | Đọc delta, không ghi đè; không tự chiếm phiên còn hoạt động |
| `AUDIO_TEXT_MISMATCH`, `ANCHOR_UNRESOLVED` | Trả đoạn và evidence; không tạo timing giả |
| `ASSET_MISSING`, `POSE_UNSUPPORTED`, `WORKFLOW_INCOMPATIBLE` | Chặn job phụ thuộc; đề xuất asset/request cần bổ sung |
| `MODEL_NOT_INSTALLED`, `LICENSE_UNRESOLVED` | Chỉ rõ dependency, nguồn và dung lượng khi biết; không mua dịch vụ thay thế |
| `RESOURCE_INSUFFICIENT`, `GPU_OOM`, `DISK_FULL` | Giữ kết quả đã có, release worker; không lặp vô hạn |
| `PROVIDER_SUBMIT_UNKNOWN` | Tra job provider bằng ID/idempotency trước khi gửi mới |
| `STALE_DEPENDENCY` | Recompile/invalidate phạm vi cần thiết; không dùng output cũ |
| `OUTPUT_INVALID` | Giữ artifact lỗi để chẩn đoán, không gắn nhãn final-ready |

## 9. Cache và invalidation

| Loại kết quả | Cache key cần bao gồm |
|---|---|
| ASR/alignment | Audio hash, language, transcript hash khi applicable, model hash, adapter/version, config |
| Asset sinh | Prompt đầy đủ, references hashes, model/workflow versions, seed, parameters, output spec |
| Rig | Parts/poses/pivots/attachments và revision |
| Render span | Timeline frame range, tất cả asset/rig/font/camera/transition liên quan, render engine và output profile |
| Audio mix | Audio revisions, offsets, gain/fades, SFX/music hashes, sample rate và encoder settings |
| Final export | Ordered video spans, audio mix hash, subtitles, mux profile |

Không cache theo tên file hoặc prompt rút gọn. Cùng seed không đảm bảo pixel identical qua runtime khác; hash runtime/config phục vụ truy nguyên, không hứa bitwise reproducibility toàn máy.

Sửa pose chỉ invalidate spans dùng pose đó và transitions phụ thuộc; không ASR lại. Sửa gain chỉ invalidate mix/final mux. Sửa tỉ lệ khung hình invalidate bố cục và video spans nhưng giữ audio/asset nếu còn phù hợp. Đổi style toàn bài là thay đổi phạm vi lớn cần báo trước lượng công việc, không giả là sửa nhỏ.

## 10. Kết nối Codex và Antigravity

Implementer tạo launcher MCP tuyệt đối và cấu hình mẫu cho hai client từ tài liệu chính thức ở thời điểm cài. Không hard-code đường dẫn người dùng khác. Codex/Antigravity cần chạy trong môi trường truy cập máy local hoặc đã được người dùng kết nối hợp lệ. Không đưa API key AI vào studio.

Bridge STDIO chỉ phục vụ giao thức; log ra stderr, không lẫn stdout protocol. Bridge gọi core đang chạy, có health check; mất agent không giết render worker đang làm việc hợp lệ. Server lease bảo vệ writer; UI patch cùng dùng expected_revision.

Capability matrix của client ghi có thể gửi ảnh/audio/video trực tiếp hay chỉ tham chiếu. Nếu không nghe/xem media được thì không khai kiểm tra đó đã xảy ra. Không cần bổ sung VLM local chỉ để lấp chỗ trống ở bản đầu.
