> 中文维护译文，与[英文原文](../../../docs/submission.md)同步，差异以英文为准。

# 公共目录提交准备

本文件是预备材料，不证明已上传、提交、审核通过或公开。本地安装、公开 GitHub 分发、目录审核和发布分别记录，见[验证记录](verification.md)。

## 预备上架文案

| 字段 | 预备值 |
| --- | --- |
| 名称 | Vibe Dev Skills |
| 标识与版本 | `vibe-dev-skills` / `0.1.0` |
| 维护者 | `jmaxzh`；门户认证身份仍待核查 |
| 简介 | 提供开发工作流，以及文档、UI、MySQL 和 CC Connect 技能。 |
| 分类 | 开发工具，按门户实际分类映射 |
| 来源与主页 | https://github.com/jmaxzh/vibe-dev-skills |
| 支持入口 | https://github.com/jmaxzh/vibe-dev-skills/issues |
| 许可证 | MIT，各技能含固定声明 |
| 图标 | `assets/icon.png` 原创终端图形，256 × 256 PNG |
| 运行条件 | 本地编程代理；可选 CC Connect 镜像使用 Python/Unix 能力和 macOS 服务 |

描述：将功能想法转化为需求、技术方案、实现与明确验证。套件复用项目已有决策，将用户显式调用的工作流与文档、UI、MySQL、集成专项技能组合。文档任务依赖随包文档设计技能。英文是唯一运行指令版本，中文仅供开发者维护。

任务示例：

- 将功能想法转为需求和验收标准，停在技术方案之前。
- 审查 MySQL 表结构和库存扣减的完整性、并发问题。
- 检查 CC Connect 既有配置，再考虑可选桌面镜像。

## OpenAI 目录

遵循[标准提交流程](https://developers.openai.com/plugins/deploy/submission)，按 Skills-only 插件上传审阅 ZIP，无 MCP、应用映射或 hook。根 `plugin.json` 提供可移植元数据和 OpenAI 展示配置；按[桌面执行说明](https://developers.openai.com/plugins/deploy/desktop-only)，通过 `extensions.com.openai.requires_local_executor` 声明本地执行。

上传前确认账号资格、开发者或企业身份，填写真实联系信息，并确认适用的桌面提交权限；GitHub 名称不等于已认证身份。门户要求其他图标尺寸或额外字段时，补齐审阅过的资产与真实信息，不虚构隐私、法律网址或部署证据。按当前标准流程，纯技能插件无需 MCP 应用测试用例或演示录像。

分别记录上传、草稿校验、提交、审核通过和公开。审核通过后仍须明确授权的门户发布操作，本地安装不保证门户验证或审核成功。

## Anthropic 目录

遵循[插件发布文档](https://code.claude.com/docs/en/plugins/publish)，确认付费计划及组织角色后使用文档链接的开发者门户；这与进入 `claude-plugins-official` 不同。

提供包或仓库、文案、支持网址、许可证、图标和真实验证记录；提交前运行严格本地校验。核对目标产品对组件的支持，本地编程与集成套件不宣称仅浏览器即可执行。门户要求截图或额外材料时，从真实成功使用中取得，不制作虚假演示。

## 发布门槛

- 审查英文源和同步的中文维护译文。
- 校验声明、清单、来源链接、依赖处理、原生安装和归档包。
- 完成新会话的文档技能加载与缺失依赖模型检查；文件校验不能替代模型行为证据。
- 若上架文案承诺消息或桌面行为，补充目标机器实测，否则移除相应承诺。
- 在各门户确认发布者身份、提交权限和必要资产。
- 推送、上传、提交及公开须有明确授权，不自动提交反馈表单或联系维护者。

本地准备未执行市场或目录发布。MIT 权利包含所有者确认的 CC Connect 脚本，见[来源说明](provenance.md)。
