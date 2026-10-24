"""Read-only localhost review server with byte ranges for seeking long audio.

No video rendering, uploads or writes. Start from any cwd; root is the repo.
"""
import argparse
from datetime import datetime, timezone
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


class ReviewHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self.remaining = None
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            return super().send_head()
        try:
            stream = path.open('rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return None
        size = path.stat().st_size
        requested = self.headers.get('Range')
        start, end = 0, size-1
        if requested:
            match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested.strip())
            if not match or not any(match.groups()):
                stream.close(); self.send_error(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE); return None
            first, last = match.groups()
            if first:
                start = int(first); end = min(int(last),size-1) if last else size-1
            else:
                start = max(0,size-int(last))
            if start >= size or start > end:
                stream.close(); self.send_response(416); self.send_header('Content-Range',f'bytes */{size}'); self.send_header('Content-Length','0'); self.end_headers(); return None
        self.send_response(206 if requested else 200)
        self.send_header('Content-Type',self.guess_type(str(path)))
        self.send_header('Accept-Ranges','bytes')
        self.send_header('Content-Length',str(max(0,end-start+1)))
        self.send_header('Last-Modified',self.date_time_string(path.stat().st_mtime))
        if requested:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.send_header('Cache-Control','no-cache')
        self.end_headers(); stream.seek(start); self.remaining=max(0,end-start+1)
        return stream

    def copyfile(self, source, outputfile):
        remaining=self.remaining
        if remaining is None:return super().copyfile(source,outputfile)
        try:
            while remaining:
                data=source.read(min(256*1024,remaining))
                if not data:break
                outputfile.write(data);remaining-=len(data)
        except (ConnectionResetError,BrokenPipeError,ConnectionAbortedError):
            pass  # Browser changed shot or canceled a preload.

    def log_message(self, fmt, *args):
        pass


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=62824);args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(ReviewHandler,directory=str(ROOT)))
    print(f'Review server: http://127.0.0.1:{args.port}/projects/mo_den_phong_than/reference_style_edit_v2/preview.html',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()
