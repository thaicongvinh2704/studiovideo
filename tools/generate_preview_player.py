"""Generate an interactive HTML preview player for Phong Thần video.
Allows the user to play, scrub, pause, view chapter markers, live subtitle sync, and inspect every scene with real audio!
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "projects" / "mo_den_phong_than"
PROJECT_FILE = PROJECT_DIR / "project.json"

p = json.load(open(PROJECT_FILE, 'r', encoding='utf-8'))
scenes = p['scenes']

# Prepare scene list for JS
scene_data = []
for i, sc in enumerate(scenes):
    ed = sc.get('editorial', {})
    scene_data.append({
        'index': i,
        'id': sc['id'],
        'name': sc['name'],
        'start': sc['start'],
        'end': sc['start'] + sc['duration'],
        'duration': sc['duration'],
        'section': ed.get('section', 1),
        'chapter': ed.get('chapter', ''),
        'asset_id': ed.get('asset_id', ''),
        'asset_name': ed.get('asset_name', ''),
        'layout': ed.get('layout', ''),
        'text': ed.get('voice_text', ''),
        'image': f"review/shot_{i:03d}.jpg"
    })

chapters = [
    {"num": 1, "name": "Hai mệnh lệnh", "time": 0.0},
    {"num": 2, "name": "Người đọc danh sách", "time": 58.66},
    {"num": 3, "name": "Văn Trọng chưa chịu cúi đầu", "time": 140.92},
    {"num": 4, "name": "Có thần vị, tội vẫn còn", "time": 254.84},
    {"num": 5, "name": "Kẻ cản đường thành hình danh sách", "time": 331.55},
    {"num": 6, "name": "Một chức thần đổi lấy điều gì?", "time": 429.76},
    {"num": 7, "name": "Đứng dưới quyền người từng giết mình", "time": 578.20},
    {"num": 8, "name": "Người phong thần đi về đâu?", "time": 716.18},
    {"num": 9, "name": "Trở lại trước đàn", "time": 809.70},
    {"num": 10, "name": "Kết phim (Tử Nha nhìn núi)", "time": 895.53}
]

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Trình xem trước bản dựng: Phong Thần Diễn Nghĩa (Mỏ Đen)</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0f141c; color: #e2e8f0; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}
  header {{ background: #18202c; padding: 10px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #2d3748; }}
  h1 {{ font-size: 17px; font-weight: 600; color: #f6c945; }}
  .badge {{ background: #2b394e; color: #90cdf4; font-size: 12px; padding: 3px 8px; border-radius: 4px; }}
  main {{ display: flex; flex: 1; overflow: hidden; }}
  .player-section {{ flex: 3; display: flex; flex-direction: column; background: #000; position: relative; }}
  .canvas-container {{ flex: 1; position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
  .preview-img {{ max-width: 100%; max-height: 100%; object-fit: contain; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }}
  .subtitle-overlay {{ position: absolute; bottom: 30px; left: 5%; right: 5%; text-align: center; pointer-events: none; }}
  .subtitle-text {{ display: inline-block; background: rgba(15, 23, 42, 0.88); color: #fff; padding: 8px 18px; border-radius: 6px; font-size: 20px; font-weight: 500; line-height: 1.4; max-width: 900px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
  .shot-tag {{ position: absolute; top: 15px; left: 15px; background: rgba(0,0,0,0.75); color: #f6c945; font-size: 13px; font-family: monospace; padding: 4px 10px; border-radius: 4px; border: 1px solid #4a5568; }}
  
  .controls-bar {{ background: #18202c; padding: 12px 20px; border-top: 1px solid #2d3748; display: flex; flex-direction: column; gap: 8px; }}
  .timeline-row {{ display: flex; align-items: center; gap: 12px; }}
  .time-slider {{ flex: 1; accent-color: #f6c945; cursor: pointer; height: 8px; }}
  .time-display {{ font-family: monospace; font-size: 14px; min-width: 110px; color: #cbd5e0; }}
  
  .buttons-row {{ display: flex; align-items: center; justify-content: space-between; }}
  .btn-group {{ display: flex; gap: 8px; }}
  button {{ background: #2d3748; color: #fff; border: 1px solid #4a5568; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.2s; }}
  button:hover {{ background: #4a5568; }}
  button.primary {{ background: #d97706; border-color: #f59e0b; color: #fff; }}
  button.primary:hover {{ background: #b45309; }}

  .sidebar {{ flex: 1.4; background: #131923; border-left: 1px solid #2d3748; display: flex; flex-direction: column; overflow: hidden; }}
  .sidebar-header {{ padding: 12px 16px; background: #1a2230; font-weight: 600; font-size: 14px; border-bottom: 1px solid #2d3748; color: #cbd5e0; }}
  .chapter-list {{ display: flex; flex-wrap: wrap; gap: 4px; padding: 10px; background: #161e2a; border-bottom: 1px solid #2d3748; max-height: 120px; overflow-y: auto; }}
  .chapter-btn {{ font-size: 11px; padding: 4px 8px; background: #243042; border: 1px solid #3b4b62; border-radius: 3px; color: #e2e8f0; }}
  .chapter-btn:hover {{ background: #3b4b62; }}
  
  .scene-list {{ flex: 1; overflow-y: auto; padding: 8px; display: flex; flex-direction: column; gap: 6px; }}
  .scene-card {{ padding: 8px 10px; background: #1c2534; border-radius: 4px; border: 1px solid #2d3748; cursor: pointer; font-size: 12px; transition: all 0.15s; }}
  .scene-card:hover {{ background: #273448; border-color: #4a5568; }}
  .scene-card.active {{ background: #2b3c54; border-color: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.4); }}
  .card-top {{ display: flex; justify-content: space-between; margin-bottom: 4px; color: #f6c945; font-weight: 600; }}
  .card-asset {{ color: #90cdf4; font-size: 11px; }}
  .card-text {{ color: #a0aec0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
</style>
</head>
<body>

<header>
  <h1>Stickman Animation Studio · Bản Dựng Xem Trước (Preview Timeline)</h1>
  <div style="display: flex; gap: 10px; align-items: center;">
    <span class="badge">102 Cảnh (15m05s)</span>
    <span class="badge" style="background: #234e35; color: #6ee7b7;">Voice H 1.25x (892s)</span>
    <span class="badge" style="background: #4c1d24; color: #fca5a5;">CHƯA RENDER FINAL</span>
  </div>
</header>

<main>
  <div class="player-section">
    <div class="canvas-container">
      <img id="previewImg" class="preview-img" src="review/shot_000.jpg" alt="Preview Frame">
      <div id="shotTag" class="shot-tag">Shot #000 · Mở đầu</div>
      <div class="subtitle-overlay">
        <div id="subText" class="subtitle-text">VÌ SAO KẺ ĐỊCH CỦA KHƯƠNG TỬ NHA VẪN ĐƯỢC PHONG THẦN?</div>
      </div>
    </div>
    
    <div class="controls-bar">
      <div class="timeline-row">
        <input type="range" id="timeSlider" class="time-slider" min="0" max="905" step="0.1" value="0">
        <span id="timeDisplay" class="time-display">00:00 / 15:05</span>
      </div>
      
      <div class="buttons-row">
        <div class="btn-group">
          <button id="playBtn" class="primary">▶ Phát (Play)</button>
          <button id="prevBtn">⏮ Cảnh trước</button>
          <button id="nextBtn">⏭ Cảnh kế</button>
          <button id="nudgeBackBtn">↶ -5s</button>
          <button id="nudgeFwdBtn">↷ +5s</button>
        </div>
        <div style="font-size: 12px; color: #a0aec0;">
          Dùng phím <kbd>Space</kbd> để Play/Pause, phím <kbd>←</kbd> / <kbd>→</kbd> để tua cảnh
        </div>
      </div>
    </div>
    <audio id="audioTrack" src="voice_direction/Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.mp3" preload="auto"></audio>
  </div>

  <div class="sidebar">
    <div class="sidebar-header">Mục lục 9 Chương & 102 Phân cảnh</div>
    <div class="chapter-list">
      {' '.join(f'<button class="chapter-btn" onclick="seekTo({c["time"]})">{c["num"]}. {c["name"]}</button>' for c in chapters)}
    </div>
    <div id="sceneList" class="scene-list"></div>
  </div>
</main>

<script>
  const scenes = {json.dumps(scene_data, ensure_ascii=False)};
  const audio = document.getElementById('audioTrack');
  const slider = document.getElementById('timeSlider');
  const timeDisplay = document.getElementById('timeDisplay');
  const previewImg = document.getElementById('previewImg');
  const shotTag = document.getElementById('shotTag');
  const subText = document.getElementById('subText');
  const playBtn = document.getElementById('playBtn');
  const sceneList = document.getElementById('sceneList');
  const AUDIO_OFFSET = 4.0;
  
  let currentSceneIdx = -1;
  let isPlaying = false;
  let animFrameId = null;

  // Build Scene List UI
  scenes.forEach((sc, i) => {{
    const card = document.createElement('div');
    card.className = 'scene-card';
    card.id = 'scene-card-' + i;
    card.onclick = () => seekTo(sc.start);
    card.innerHTML = `
      <div class="card-top">
        <span>#${{String(sc.index).padStart(3, '0')}} · ${{formatTime(sc.start)}}</span>
        <span class="card-asset">${{sc.asset_id}}</span>
      </div>
      <div style="font-weight: 500; margin-bottom: 2px;">${{sc.name.split('·')[1] || sc.name}}</div>
      <div class="card-text">${{sc.text || sc.layout}}</div>
    `;
    sceneList.appendChild(card);
  }});

  function formatTime(sec) {{
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${{String(m).padStart(2, '0')}}:${{String(s).padStart(2, '0')}}`;
  }}

  function updateTimeline() {{
    const t = getEffectiveTime();
    slider.value = t;
    timeDisplay.textContent = `${{formatTime(t)}} / 15:05`;
    
    // Find active scene
    let activeIdx = 0;
    for (let i = 0; i < scenes.length; i++) {{
      if (t >= scenes[i].start && t < scenes[i].end) {{
        activeIdx = i;
        break;
      }}
      if (t >= scenes[scenes.length - 1].start) {{
        activeIdx = scenes.length - 1;
      }}
    }}
    
    if (activeIdx !== currentSceneIdx) {{
      currentSceneIdx = activeIdx;
      const sc = scenes[activeIdx];
      previewImg.src = sc.image;
      shotTag.textContent = `#${{String(sc.index).padStart(3, '0')}} · Phần ${{sc.section}} · ${{sc.asset_id}}`;
      subText.textContent = sc.text || sc.name;
      subText.style.display = sc.text || sc.name ? 'inline-block' : 'none';
      
      // Update sidebar highlight
      document.querySelectorAll('.scene-card').forEach(c => c.classList.remove('active'));
      const activeCard = document.getElementById('scene-card-' + activeIdx);
      if (activeCard) {{
        activeCard.classList.add('active');
        activeCard.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
      }}
    }}

    if (isPlaying) {{
      animFrameId = requestAnimationFrame(updateTimeline);
    }}
  }}

  function getEffectiveTime() {{
    if (audio.paused && !isPlaying) {{
      return parseFloat(slider.value);
    }}
    if (audio.currentTime > 0) {{
      return audio.currentTime + AUDIO_OFFSET;
    }}
    return parseFloat(slider.value);
  }}

  function seekTo(targetTime) {{
    targetTime = Math.max(0, Math.min(905, targetTime));
    slider.value = targetTime;
    if (targetTime >= AUDIO_OFFSET && targetTime < AUDIO_OFFSET + audio.duration) {{
      audio.currentTime = targetTime - AUDIO_OFFSET;
    }} else {{
      audio.pause();
    }}
    updateTimeline();
  }}

  function togglePlay() {{
    if (isPlaying) {{
      pause();
    }} else {{
      play();
    }}
  }}

  function play() {{
    const t = parseFloat(slider.value);
    if (t >= AUDIO_OFFSET && t < AUDIO_OFFSET + (audio.duration || 892)) {{
      audio.currentTime = t - AUDIO_OFFSET;
      audio.play().catch(e => console.log('Audio autoplay prevented:', e));
    }}
    isPlaying = true;
    playBtn.textContent = '⏸ Tạm dừng (Pause)';
    playBtn.classList.remove('primary');
    animFrameId = requestAnimationFrame(updateTimeline);
  }}

  function pause() {{
    audio.pause();
    isPlaying = false;
    playBtn.textContent = '▶ Phát (Play)';
    playBtn.classList.add('primary');
    if (animFrameId) cancelAnimationFrame(animFrameId);
  }}

  playBtn.onclick = togglePlay;
  slider.oninput = (e) => seekTo(parseFloat(e.target.value));

  document.getElementById('prevBtn').onclick = () => {{
    if (currentSceneIdx > 0) seekTo(scenes[currentSceneIdx - 1].start);
  }};
  document.getElementById('nextBtn').onclick = () => {{
    if (currentSceneIdx < scenes.length - 1) seekTo(scenes[currentSceneIdx + 1].start);
  }};
  document.getElementById('nudgeBackBtn').onclick = () => seekTo(parseFloat(slider.value) - 5);
  document.getElementById('nudgeFwdBtn').onclick = () => seekTo(parseFloat(slider.value) + 5);

  window.addEventListener('keydown', (e) => {{
    if (e.code === 'Space') {{ e.preventDefault(); togglePlay(); }}
    if (e.code === 'ArrowLeft') {{ e.preventDefault(); seekTo(parseFloat(slider.value) - 3); }}
    if (e.code === 'ArrowRight') {{ e.preventDefault(); seekTo(parseFloat(slider.value) + 3); }}
  }});

  // Initial update
  seekTo(0);
</script>
</body>
</html>
"""

out_player = PROJECT_DIR / "preview_player.html"
with open(out_player, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"Generated Interactive Preview Player: {out_player} ({out_player.stat().st_size / 1024:.1f} KB)")
