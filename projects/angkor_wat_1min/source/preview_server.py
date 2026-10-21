"""Serve only this film and its project archive on this computer's loopback address."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import re
import argparse
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
FILM = ROOT / 'revision2'
FILES = {
    '/video.mp4': (FILM / 'Angkor_Wat_Ban_do_co_the_buoc_vao_1080p.mp4', 'video/mp4'),
    '/project.zip': (FILM / 'Du_an_Angkor_Wat_Ban_2.zip', 'application/zip'),
    '/poster.png': (FILM / 'review' / 'decoded_00.png', 'image/png'),
}
PAGE = '''<!doctype html>
<html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Angkor Wat — Bản đồ có thể bước vào · Bản 2</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#111719;color:#edf3ef;font:16px/1.6 system-ui,sans-serif}
main{max-width:1120px;padding:28px 24px;margin:auto}h1{font-size:28px;line-height:1.25;margin:0 0 8px}
p{margin:8px 0 20px;color:#c0ccc8}video{display:block;width:100%;max-height:72vh;aspect-ratio:16/9;background:#000;border-radius:12px}
nav{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}a,button{font:inherit;border:0;border-radius:8px;padding:9px 16px;background:#c7e9cb;color:#11231a;text-decoration:none;cursor:pointer}
nav a{background:#283730;color:#edf3ef}#status{font-size:14px;color:#afc1b9}small{color:#afc1b9}
</style><main>
<h1>Angkor Wat — Bản đồ có thể bước vào</h1>
<p>Bản 2 · Không có người dẫn trên hình · 60 giây · Full HD</p>
<video id="film" controls playsinline preload="auto" poster="/poster.png?v=2" aria-label="Video Angkor Wat bản 2"><source src="/video.mp4?v=2" type="video/mp4"></video>
<nav><button id="play">Phát video</button><a href="/video.mp4?download=1" download="Angkor_Wat_Ban_2_1080p.mp4">Tải video MP4</a><a href="/project.zip?download=1" download="Du_an_Angkor_Wat_Ban_2.zip">Tải project chỉnh sửa</a></nav>
<p id="status" role="status">Đang tải video…</p>
<small>Giọng đọc trong bản này: Hải Đăng (VieNeu-TTS).</small>
</main><script>
const film=document.getElementById('film'),play=document.getElementById('play'),status=document.getElementById('status');
film.addEventListener('canplay',()=>{status.textContent='Video đã sẵn sàng. Bấm Phát video để xem và nghe.'});
film.addEventListener('play',()=>{play.textContent='Tạm dừng';status.textContent='Đang phát video có âm thanh.'});
film.addEventListener('pause',()=>{play.textContent='Phát video';status.textContent='Đã tạm dừng.'});
film.addEventListener('ended',()=>{play.textContent='Xem lại';status.textContent='Đã phát hết video.'});
film.addEventListener('error',()=>{status.textContent='Trình duyệt chưa phát được video. Bạn có thể bấm Tải video MP4.'});
play.addEventListener('click',()=>{if(film.paused){film.play().catch(()=>{status.textContent='Hãy bấm nút phát trên video.'})}else{film.pause()}});
</script></html>'''.encode('utf-8')


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_content(head=True)

    def do_GET(self):
        self.send_content(head=False)

    def send_content(self, head):
        route = urlsplit(self.path).path
        if route == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(PAGE)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            if not head:
                self.wfile.write(PAGE)
            return
        if route not in FILES or not FILES[route][0].is_file():
            self.send_error(404)
            return
        path, mime = FILES[route]
        size = path.stat().st_size
        start, end = 0, size - 1
        ranged = self.headers.get('Range')
        if ranged:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', ranged)
            if not match or not any(match.groups()):
                self.send_error(416)
                return
            first, last = match.groups()
            if first:
                start = int(first)
                end = min(int(last), end) if last else end
            else:
                start = max(0, size - int(last))
            if start > end or start >= size:
                self.send_response(416)
                self.send_header('Content-Range', f'bytes */{size}')
                self.end_headers()
                return
        self.send_response(206 if ranged else 200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        if ranged:
            self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        if urlsplit(self.path).query == 'download=1':
            self.send_header('Content-Disposition', f'attachment; filename="{path.name}"')
        self.end_headers()
        if head:
            return
        try:
            with path.open('rb') as source:
                source.seek(start)
                remaining = end - start + 1
                while remaining:
                    block = source.read(min(65536, remaining))
                    if not block:
                        break
                    self.wfile.write(block)
                    remaining -= len(block)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--port', type=int, default=0)
    port = args.parse_args().port
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    url = f'http://127.0.0.1:{server.server_port}/'
    (ROOT / 'review' / 'preview_url.json').write_text(json.dumps({'url': url}), encoding='utf-8')
    print(url, flush=True)
    server.serve_forever()
