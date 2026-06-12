---
name: wechat-article-podcast
description: 抓取微信公众号文章并保存为本地 HTML，启动本地文章服务，并为后续通过花生壳内网穿透映射公网、交给豆包 APP 转成播客做准备。Use when the user asks to fetch WeChat/微信公众号/mp.weixin.qq.com articles, save articles locally, create accessible HTML links, expose local article pages through Oray/花生壳, or prepare article URLs for Doubao/豆包 podcast conversion.
---

# 微信文章转豆包播客

## Core Workflow

1. Confirm the input is a微信公众号文章 URL, usually `https://mp.weixin.qq.com/s/...`.
2. Fetch and save the article as HTML with `scripts/fetch_wechat_article.py`.
3. Serve the saved article directory with `scripts/serve_wechat_articles.py` when the user needs a browser-accessible URL.
4. If the user needs 豆包 APP podcast conversion, explain that local URLs must be mapped to a public URL through 花生壳 or another tunnel.
5. Return the saved file path and the article URL. If public mapping is not configured, return the local URL and state that it still needs tunnel mapping.

## Fetch An Article

Run from the target project/work directory:

```bash
python path/to/wechat-article-podcast/scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/..." --output-dir articles
```

The script prints JSON containing:

- `success`
- `title`
- `filename`
- `path`

Use the printed filename to build the served article URL:

```text
http://127.0.0.1:8027/articles/<filename>
```

## Serve Saved Articles

Run:

```bash
python path/to/wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir path/to/wechat-article-podcast/assets --host 127.0.0.1 --port 8027
```

For LAN or tunnel tools that cannot reach `127.0.0.1`, bind to all interfaces:

```bash
python path/to/wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir path/to/wechat-article-podcast/assets --host 0.0.0.0 --port 8027
```

The server automatically tries later ports if the requested port is occupied.

## 花生壳 And 豆包

Read `references/oray-doubao-flow.md` when the user asks how to expose the local article for 豆包 APP, how 花生壳内网穿透 fits into the workflow, or what public URL should be given to 豆包.

Default 花生壳 link:

```text
http://url.oray.com/i/47632
```

## Output Contract

When completing a task, report:

- Saved HTML path
- Local article URL
- Whether a local server is running, including host and port
- If applicable, the 花生壳/public URL step that remains before 豆包 APP can access the article

Do not claim that 豆包 can access `localhost` or `127.0.0.1` directly from another device. Tell the user to use the mapped public URL after tunnel setup.
