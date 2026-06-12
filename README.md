# WeChat Article To Doubao Podcast Skill

A Codex Skill for fetching WeChat public-account articles, saving them as local HTML, serving the saved pages, and preparing URLs that can be exposed through Oray/花生壳 for Doubao/豆包 podcast conversion.

## What It Does

- Fetches `https://mp.weixin.qq.com/s/...` articles and saves them as HTML.
- Serves saved HTML files from a local `articles/` directory.
- Provides a repeatable workflow for mapping the local service to a public URL with 花生壳内网穿透.
- Helps prepare article URLs that Doubao APP can consume for podcast generation.

## Skill Structure

```text
wechat-article-podcast/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── logo.png
├── references/
│   └── oray-doubao-flow.md
└── scripts/
    ├── fetch_wechat_article.py
    └── serve_wechat_articles.py
```

## Requirements

```bash
pip install -r requirements.txt
```

## Script Usage

Fetch an article:

```bash
python wechat-article-podcast/scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/..." --output-dir articles
```

Serve saved articles locally:

```bash
python wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir wechat-article-podcast/assets --host 127.0.0.1 --port 8027
```

For tunnel tools that need LAN-accessible binding:

```bash
python wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir wechat-article-podcast/assets --host 0.0.0.0 --port 8027
```

## Doubao Podcast Flow

1. Fetch the WeChat article and save it as HTML.
2. Start the local article server.
3. Use 花生壳内网穿透 to map the local service to a public URL.
4. Give the public article URL to Doubao APP for podcast conversion.

花生壳内网穿透: http://url.oray.com/i/47632

Do not give Doubao APP a `localhost` or `127.0.0.1` URL from another device. Use the mapped public URL after tunnel setup.

## License

MIT
