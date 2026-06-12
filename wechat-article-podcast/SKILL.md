---
name: wechat-article-podcast
description: 抓取微信公众号文章并保存为本地 HTML，启动本地文章服务，并为后续通过花生壳内网穿透映射公网、交给豆包 APP 转成播客做准备。适用于用户要求抓取微信公众号文章、保存 mp.weixin.qq.com 文章、本地生成可访问 HTML 链接、通过花生壳暴露本地文章页面，或准备给豆包生成播客使用的文章 URL。
---

# 微信文章转豆包播客

## 核心流程

1. 确认输入是微信公众号文章 URL，通常形如 `https://mp.weixin.qq.com/s/...`。
2. 使用 `scripts/fetch_wechat_article.py` 抓取文章，并保存为本地 HTML。
3. 当用户需要可访问链接时，使用 `scripts/serve_wechat_articles.py` 启动本地文章服务。
4. 如果用户需要交给豆包 APP 转播客，说明本地 URL 需要先通过花生壳或其他内网穿透工具映射为公网 URL。
5. 交付保存路径和文章访问 URL；如果还没有配置公网映射，交付本地 URL，并明确说明还需要完成内网穿透映射。

## 抓取文章

在目标项目或工作目录中运行：

```bash
python path/to/wechat-article-podcast/scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/..." --output-dir articles
```

脚本会输出 JSON，包含：

- `success`：是否成功
- `title`：文章标题
- `filename`：保存后的文件名
- `path`：本地完整路径

使用输出的 `filename` 拼接本地服务文章 URL：

```text
http://127.0.0.1:8027/articles/<filename>
```

## 启动文章服务

运行：

```bash
python path/to/wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir path/to/wechat-article-podcast/assets --host 127.0.0.1 --port 8027
```

如果局域网设备或内网穿透工具无法访问 `127.0.0.1`，改为绑定所有网卡：

```bash
python path/to/wechat-article-podcast/scripts/serve_wechat_articles.py --article-dir articles --static-dir path/to/wechat-article-podcast/assets --host 0.0.0.0 --port 8027
```

如果指定端口已被占用，服务脚本会自动尝试后续端口。

## 花生壳与豆包

当用户询问如何让豆包 APP 访问本地文章、花生壳内网穿透在流程中如何使用，或应该给豆包什么 URL 时，读取 `references/oray-doubao-flow.md`。

默认花生壳链接：

```text
http://url.oray.com/i/47632
```

## 交付要求

完成任务时，需要说明：

- 保存后的 HTML 路径
- 本地文章访问 URL
- 本地服务是否已启动，以及对应主机和端口
- 如适用，说明豆包 APP 访问前还需要完成花生壳或其他公网映射

不要声称豆包 APP 可以直接访问另一台设备上的 `localhost` 或 `127.0.0.1`。如果要让豆包访问文章，应使用内网穿透后的公网 URL。
