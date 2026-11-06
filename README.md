# 健身器械双语图鉴

这是一个面向健身新手和自媒体整理工作的可搜索器械图鉴：

- 63 张通用器械示意图，按 8 个类别分组
- 每张图同时提供中文名、英文名和“看哪里能认出来”的提示
- 每张器械图可以直接下载 SVG，方便在 Figma、Canva、Illustrator 或剪辑软件中继续编辑
- 动作区精选 34 个常见动作，提供 JPG、GIF、英文名、器械字段和原始链接
- 通过“来源与使用”页进入完整的 `hasaneyldrm/exercises-dataset` 动作库

## 素材边界

器械图是通用类型示意图，适合先认类别和名称；它们不是某个厂家的产品照片，也不应被当成所有品牌的统一外观。

动作 JPG/GIF 来自 [hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset) 的仓库媒体。该仓库说明：媒体归属于 Gym visual，使用时应保留 `© Gym visual — https://gymvisual.com/` 并遵守其媒体条款；仓库中的名称、分类与说明数据另按 MIT 许可发布。

## 运行与发布

`dist/` 是可直接部署的静态站点目录。站点不依赖后端；发布到 GitHub Pages、Netlify 或 Vercel 静态托管即可在线使用。`tools/` 内的脚本用于重新生成器械 SVG、拉取动作数据和生成精选动作目录。

完整动作原始项目：<https://github.com/hasaneyldrm/exercises-dataset>
