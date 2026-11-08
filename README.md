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

Switch 客户端已接入此目录，播客页面可刷新目录、订阅 RSS、下载和断点续播；电台同时保留 Radio Browser 发现与搜索。当前目录 117 个播客频道（80 中文、37 英文），电台 19 条、18 条默认启用。原有频道 ID 全部保留。

学习成长与经济商业优先，科技、人文随后，娱乐靠后。此次参考 AntennaPod 使用公共目录的方式，并从 Chinese-Podcasts 等公开清单和 Apple 节目索引发现发布者 RSS；没有把 RSSHub 聚合代理批量作为默认源。仅保存节目元数据，不搬运音频。

117 个频道通过主机生产 HTTP/RSS 解析检查；新增候选抽查近期三集音频地址，18 个重点频道补做 MP3/AAC 解码抽样，详见 reports/。BBC 两个频道在电脑端通过生产流读取、Range 定位与解码检查，但 Switch 上的播放问题仍未完成实机定位；目录标明海外线路，不把电脑端成功描述为设备修复。

发现清单参考：[Chinese-Podcasts](https://github.com/alaskasquirrel/Chinese-Podcasts)、[awesome-chinese-podcasts](https://github.com/fffx/awesome-chinese-podcasts)、[tidings-rss](https://github.com/fuxiaoai/tidings-rss)。目录方式参考 [AntennaPod 官方说明](https://antennapod.org/documentation/podcasters-hosters/list-podcast)。节目名称和 RSS 地址经单独核验，简介按本目录分类整理。

## 展示参考

频道页参考 Pocket Casts 的节目简介、单集筛选和操作分层，以及 AntennaPod 的继续收听、新单集与订阅分区。具体 Switch 布局见 docs/switch-channel-design.md。
