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

Switch 客户端已接入此目录，播客页面可刷新目录、订阅 RSS、下载和断点续播；电台同时保留 Radio Browser 发现与搜索。当前目录 117 个播客频道（80 中文、37 英文），电台 31 条、30 条默认启用。原有频道 ID 全部保留。

学习成长与经济商业优先，科技、人文随后，娱乐靠后。此次参考 AntennaPod 使用公共目录的方式，并从 Chinese-Podcasts 等公开清单和 Apple 节目索引发现发布者 RSS；没有把 RSSHub 聚合代理批量作为默认源。仅保存节目元数据，不搬运音频。

117 个频道通过主机生产 HTTP/RSS 解析检查；新增候选抽查近期三集音频地址，18 个重点频道补做 MP3/AAC 解码抽样，详见 reports/。BBC 两个频道在电脑端通过生产流读取、Range 定位与解码检查，但 Switch 上的播放问题仍未完成实机定位；目录标明海外线路，不把电脑端成功描述为设备修复。

发现清单参考：[Chinese-Podcasts](https://github.com/alaskasquirrel/Chinese-Podcasts)、[awesome-chinese-podcasts](https://github.com/fffx/awesome-chinese-podcasts)、[tidings-rss](https://github.com/fuxiaoai/tidings-rss)。目录方式参考 [AntennaPod 官方说明](https://antennapod.org/documentation/podcasters-hosters/list-podcast)。节目名称和 RSS 地址经单独核验，简介按本目录分类整理。

## 展示参考

频道页参考 Pocket Casts 的节目简介、单集筛选和操作分层，以及 AntennaPod 的继续收听、新单集与订阅分区。具体 Switch 布局见 docs/switch-channel-design.md。

## 公共目录搜索与推荐关键词

Switch 播客新增“搜索更多”：通过 Apple 公共索引找到发布者 RSS，之后直接从发布者加载单集，复用订阅、在线播放、下载和续播。无需逐个维护可搜索的节目清单。117 个精选频道仍保留。Podcast Index 适配器需要本项目自己的开发者密钥，未配置时默认使用 Apple，不借用其他应用密钥。

`catalogs/search-keywords.json` 管理推荐主题及查询词，分组顺序可更新，不是热搜统计。目前6组30词。`catalog.json` 的可选 `search_keywords` 条目包含字节数与 SHA256；客户端走 GitHub 加速与直连回退，格式或校验失败继续使用已保存/内置关键词。旧客户端忽略新增条目。推荐词只影响搜索文本，不能改写 API 地址。个人最近10次成功搜索留在设备，可以清空，不上传到本仓库。

只修改关键词时执行 `python tools/check_catalogs.py --write --manifest-only`；此方式刷新清单哈希，不重复访问未修改的117个RSS。主机端搜索到发布者RSS、订阅、播放器入口和进度保存的检查记录见 `reports/podcast-directory-search.json`；播放器为适配器，不能替代Switch解码验收。

## FM 精选扩充

新增 12 台，包括 5 个地方交通台、3 个中文音乐台和 4 个谈话／文艺台。各台经过两次主机取流检查，其中一次使用生产直播读取器，并各解码 6 秒。实机验收另计。详情见 [FM 检查报告](reports/fm-expansion-checks.json)。
