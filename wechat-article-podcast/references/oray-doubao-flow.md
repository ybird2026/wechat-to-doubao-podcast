# 花生壳映射与豆包转播客流程

## 目标

将本地保存的微信公众号文章 HTML 变成豆包 APP 可访问的公网 URL，方便在豆包中转换为播客。

## 推荐流程

1. 使用 `scripts/fetch_wechat_article.py` 抓取微信公众号文章，保存到 `articles/`。
2. 使用 `scripts/serve_wechat_articles.py` 启动本地文章服务。
3. 使用花生壳内网穿透将本地服务端口映射到公网。
4. 将公网文章 URL 交给豆包 APP，用于生成播客。

## 花生壳链接

花生壳内网穿透：

```text
http://url.oray.com/i/47632
```

## URL 形态

本地服务文章 URL 通常形如：

```text
http://127.0.0.1:8027/articles/260612_xxxxx.html
```

映射到公网后，URL 通常形如：

```text
https://your-domain.example/articles/260612_xxxxx.html
```

交给豆包 APP 时，应使用公网 URL，而不是 `127.0.0.1` 或 `localhost`。

## 注意事项

- 内网穿透需要映射本地服务实际监听端口。
- 如果本地服务绑定 `127.0.0.1` 无法被穿透工具访问，启动服务时改用 `--host 0.0.0.0`。
- 只分享自己有权处理的文章内容，注意版权和平台规则。
