# 微信文章转豆包播客技能

这是一个用于 Codex 的技能，用来抓取微信公众号文章、保存为本地 HTML、启动本地文章服务，并为后续通过<a href="http://url.oray.com/i/47632" target="_blank" rel="noopener noreferrer">花生壳内网穿透</a>映射公网、交给豆包 APP 转成播客做准备。

## 能做什么

- 抓取 `https://mp.weixin.qq.com/s/...` 形式的微信公众号文章，并保存为 HTML。
- 从本地 `articles/` 目录提供已保存文章的访问服务。
- 提供一套可复用流程，将本地文章服务通过<a href="http://url.oray.com/i/47632" target="_blank" rel="noopener noreferrer">花生壳内网穿透</a>映射为公网 URL。
- 帮助准备豆包 APP 可访问的文章链接，用于生成播客。

## 技能目录结构

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

## 安装依赖

```bash
pip install -r requirements.txt
```

## 脚本用法

抓取一篇微信公众号文章：

```bash
python wechat-article-podcast/scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/..." --output-dir articles
```

启动本地文章服务：

```bash
python wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir wechat-article-podcast/assets --host 127.0.0.1 --port 8027
```

如果内网穿透工具需要访问局域网地址，可以绑定所有网卡：

```bash
python wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir wechat-article-podcast/assets --host 0.0.0.0 --port 8027
```

## 豆包转播客流程

1. 抓取微信公众号文章并保存为 HTML。
2. 启动本地文章服务。
3. 使用<a href="http://url.oray.com/i/47632" target="_blank" rel="noopener noreferrer">花生壳内网穿透</a>，将本地服务映射为公网 URL。
4. 将公网文章 URL 交给豆包 APP，用于转换为播客。

<a href="http://url.oray.com/i/47632" target="_blank" rel="noopener noreferrer">花生壳内网穿透</a>

不要把另一台设备无法访问的 `localhost` 或 `127.0.0.1` 链接直接交给豆包 APP。应在内网穿透配置完成后，使用映射得到的公网 URL。

## 开源协议

MIT
