# BoleMusic 内容目录

面向波乐音乐 Switch 客户端的公开播客与网络电台目录。

- 播客目录为发布者 RSS 与节目简介，客户端读取 RSS 更新单集。
- 网络电台目录保存公开直播入口及备用地址，Radio Browser 提供发现与搜索。
- 只保存元数据，节目音频由客户端从发布者读取。
- health.json 记录有界网络抽查结果。HTTP 可达不等于完整解码或 Switch 实机通过。

## 加载地址

入口清单采用 GitHub 加速，失败回退 GitHub 原地址。

- https://gh-proxy.com/https://raw.githubusercontent.com/shellsec/bolemusic/master/catalog.json
- https://raw.githubusercontent.com/shellsec/bolemusic/master/catalog.json

各目录地址、字节数及 SHA256 位于 catalog.json。客户端完成整份验证后再替换本地缓存。第三方加速是传输通道，校验和用于检测版本不一致，不构成发布者身份认证。

## 更新约定

固定 id 标识节目或电台。变更 RSS/直播地址时保留 id。远程目录变更保留用户订阅、收藏、下载和进度。新节目由用户选择订阅。

编辑 catalogs/podcasts.json 或 catalogs/radio.json 后执行：

    python tools/check_catalogs.py --write

检查报告包含失败记录。失败台不会自动变成可用台。发布前检查 enabled、availability 以及实际解码和设备验收状态，并同步更新 revision。

## Switch 客户端状态

当前仓库首先提供可访问的数据契约与检查结果。节目 UI、下载和续播需要客户端实现。现有 NRO 的 Radio Browser 电台搜索与此远程目录是独立入口。

## 展示参考

频道页参考 Pocket Casts 的节目简介、单集筛选和操作分层，以及 AntennaPod 的继续收听、新单集与订阅分区。具体 Switch 布局见 docs/switch-channel-design.md。
