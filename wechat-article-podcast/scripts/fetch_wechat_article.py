#!/usr/bin/env python3
"""Fetch a WeChat article URL and save it as local HTML."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests


WECHAT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://mp.weixin.qq.com/",
}


def extract_title(content: str) -> str:
    patterns = [
        r"<title>(.*?)</title>",
        r'"title":"(.*?)"',
        r'<meta property="og:title" content="(.*?)"',
        r"<h1[^>]*>(.*?)</h1>",
    ]
    for pattern in patterns:
        match = re.search(pattern, content, re.S)
        if match:
            title = re.sub(r"<[^>]+>", "", match.group(1)).strip()
            title = html.unescape(title)
            if title:
                return title
    return "微信文章"


def extract_article_content(content: str) -> str:
    content_start = content.find('id="js_content"')
    if content_start == -1:
        return content

    div_start = content.rfind("<div", 0, content_start)
    if div_start == -1:
        div_start = content_start

    content_end = content.find("</div>", content_start)
    if content_end == -1:
        return content[div_start:]

    return content[div_start : content_end + 6]


def article_id_from_url(url: str) -> str:
    match = re.search(r"/s/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    return "unknown"


def build_html(title: str, article_content: str) -> str:
    escaped_title = html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escaped_title}</title>
  <style>
    body {{
      max-width: 680px;
      margin: 0 auto;
      padding: 20px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.8;
      color: #333;
    }}
    img {{
      max-width: 100%;
      height: auto;
    }}
    p {{
      margin: 1em 0;
    }}
  </style>
</head>
<body>
  <article class="rich_media_content">
    {article_content}
  </article>
</body>
</html>"""


def fetch_wechat_article(url: str, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, headers=WECHAT_HEADERS, timeout=30)
    response.encoding = "utf-8"
    if response.status_code != 200:
        raise RuntimeError(f"请求失败，状态码: {response.status_code}")

    content = response.text
    title = extract_title(content)
    article_content = extract_article_content(content)
    article_id = article_id_from_url(url)
    filename = f"{datetime.now().strftime('%y%m%d')}_{article_id}.html"
    output_path = output_dir / filename
    output_path.write_text(build_html(title, article_content), encoding="utf-8")

    return {
        "success": True,
        "title": title,
        "filename": filename,
        "path": str(output_path.resolve()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a WeChat article and save it as HTML.")
    parser.add_argument("url", help="WeChat article URL, for example https://mp.weixin.qq.com/s/...")
    parser.add_argument("--output-dir", default="articles", help="Directory for saved HTML files.")
    args = parser.parse_args()

    try:
        result = fetch_wechat_article(args.url, Path(args.output_dir))
    except Exception as exc:
        result = {"success": False, "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
