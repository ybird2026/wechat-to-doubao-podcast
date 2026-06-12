#!/usr/bin/env python3
"""Serve saved WeChat article HTML files for local or tunneled access."""

from __future__ import annotations

import argparse
import http.server
import mimetypes
import os
import re
import socket
import socketserver
import urllib.parse
from pathlib import Path


def find_available_port(host: str, start_port: int, max_attempts: int = 10) -> int:
    for offset in range(max_attempts):
        port = start_port + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((host, port)) != 0:
                return port
    raise RuntimeError(f"无法找到可用端口（已尝试 {start_port} ~ {start_port + max_attempts - 1}）")


def make_handler(article_dir: Path, static_dir: Path | None):
    article_root = article_dir.resolve()
    static_root = static_dir.resolve() if static_dir else None

    class ArticleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            path = urllib.parse.unquote(parsed.path)

            if path in ("/", ""):
                self._serve_index()
                return

            if path in ("/favicon.ico", "/favicon.png") and static_root:
                self._serve_scoped_file(static_root, "logo.png")
                return

            if path.startswith("/static/") and static_root:
                self._serve_scoped_file(static_root, path[len("/static/") :])
                return

            if path.startswith("/articles/"):
                self._serve_scoped_file(article_root, path[len("/articles/") :])
                return

            legacy_name = path.lstrip("/")
            if re.match(r"^\d{6}_[a-zA-Z0-9_-]+\.html$", legacy_name):
                self.send_response(302)
                self.send_header("Location", "/articles/" + urllib.parse.quote(legacy_name))
                self.end_headers()
                return

            self.send_error(404, "File not found")

        def _serve_index(self):
            rows = []
            for file_path in sorted(article_root.glob("*.html"), reverse=True):
                name = file_path.name
                rows.append(
                    f'<li><a href="/articles/{urllib.parse.quote(name)}" target="_blank">{name}</a></li>'
                )
            body = "\n".join(rows) or "<li>暂无文章</li>"
            html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>微信文章列表</title>
  <style>
    body {{ max-width: 760px; margin: 40px auto; padding: 0 18px; font-family: sans-serif; }}
    li {{ margin: 10px 0; }}
  </style>
</head>
<body>
  <h1>微信文章列表</h1>
  <ul>{body}</ul>
</body>
</html>"""
            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _serve_scoped_file(self, root: Path, relative_path: str):
            full_path = (root / relative_path).resolve()
            if full_path != root and root not in full_path.parents:
                self.send_error(403, "Forbidden")
                return
            if not full_path.is_file():
                self.send_error(404, "File not found")
                return
            data = full_path.read_bytes()
            content_type = mimetypes.guess_type(str(full_path))[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format, *args):
            print(f"[{self.log_date_time_string()}] {args[0]}")

    return ArticleHandler


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve saved WeChat article HTML files.")
    parser.add_argument("--article-dir", default="articles", help="Directory containing saved article HTML files.")
    parser.add_argument("--static-dir", default=None, help="Optional static directory containing logo.png.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind. Use 0.0.0.0 for LAN/tunnel access.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8027")))
    args = parser.parse_args()

    article_dir = Path(args.article_dir)
    article_dir.mkdir(parents=True, exist_ok=True)
    static_dir = Path(args.static_dir) if args.static_dir else None
    port = find_available_port(args.host, args.port)
    handler = make_handler(article_dir, static_dir)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((args.host, port), handler) as httpd:
        print("微信文章服务已启动")
        print(f"文章目录: {article_dir.resolve()}")
        print(f"访问地址: http://{args.host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    raise SystemExit(main())
