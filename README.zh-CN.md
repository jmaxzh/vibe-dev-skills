# Vibe Dev Skills

**面向软件开发生命周期的 Agent Skills——从需求、设计到实施、测试与交付。**

[English](README.md) | 简体中文

将 Vibe Coding 想法转化为需求、技术方案和具有明确验证要求的实现。套件包含开发工作流，以及文档、UI、MySQL 和 CC Connect 专项技能。

## 技能

| 技能 | 用途 | 启用与依赖 |
| --- | --- | --- |
| [SDLC 工作流](translations/zh-CN/skills/sdlc-workflow/SKILL.zh-CN.md) | 需求、技术方案、实施、验证与知识库维护 | 显式调用；文档任务需要 `sdlc-instr-doc-design` |
| [指令与文档设计](translations/zh-CN/skills/sdlc-instr-doc-design/SKILL.zh-CN.md) | 指令、提示词、技能及面向读者的文档 | 文档产物任务，可独立使用 |
| [界面与交互设计](translations/zh-CN/skills/sdlc-ui-interaction/SKILL.zh-CN.md) | 桌面、移动与网页设计和行为 | 适用的 UI 任务 |
| [MySQL 数据表与 SQL 设计](translations/zh-CN/skills/sdlc-mysql-design/SKILL.zh-CN.md) | 建模、SQL、索引、事务与并发 | 必须已明确以 MySQL 为目标数据库 |
| [CC Connect 集成](translations/zh-CN/skills/cc-connect-integration/SKILL.zh-CN.md) | 消息平台接入本地代理及可选桌面副本 | CC Connect 集成任务 |

默认安装完整套件，但不会为每项任务启用全部技能。项目初始化和知识库专项审查仍须明确要求。

## 安装

下列 GitHub 命令需要先将分发改动发布到仓库。测试尚未发布的检出目录时，使用其实际绝对路径作为来源，见[本地验证与分发](translations/zh-CN/docs/distribution.md)。

### Codex

```sh
codex plugin marketplace add jmaxzh/vibe-dev-skills
```

在受支持的插件界面中，从已配置市场安装 **Vibe Dev Skills**。提供 `plugin add` 的 CLI 版本还支持：

```sh
codex plugin add vibe-dev-skills@vibe-dev-skills
```

### Claude Code

```sh
claude plugin marketplace add jmaxzh/vibe-dev-skills
claude plugin install vibe-dev-skills@vibe-dev-skills
```

### skills CLI

安装全部五项英文技能，并选择受支持的代理：

```sh
npx skills add jmaxzh/vibe-dev-skills --skill '*'
```

工作流的最小完整组合为：

```sh
npx skills add jmaxzh/vibe-dev-skills \
  --skill sdlc-workflow \
  --skill sdlc-instr-doc-design
```

其余四项技能可单独安装。不要把只安装工作流视为文档任务的完整安装；每项技能均保留 MIT 声明。

### 手动安装

将 `skills/` 中五个目录并列复制到代理文档指定的技能目录，保留 `references/`、CC Connect 的 `scripts/` 和许可证。替换既有安装前先备份。不要将仓库根目录或维护译文复制到自动发现技能的目录。

## 使用

通过代理实际注册的名称或命名空间调用工作流：

> 使用 sdlc-workflow。开发一个小型问题跟踪工具：先明确需求，再设计方案，然后实施并完成适当测试。复用现有决策，仅暂停被未决事项阻塞的工作。

只推进到指定阶段：

> 使用 sdlc-workflow，将这个功能想法整理为需求和验收标准。停在技术方案阶段之前。

专项任务：

> 使用 sdlc-mysql-design，审查这份 MySQL 订单表结构与库存扣减 SQL。说明完整性、并发风险，并区分项目约定和 MySQL 功能限制。

集成任务：

> 使用 cc-connect-integration，检查既有配置。先验证消息主链路，再考虑可选桌面镜像。

工作流按需通过运行环境实际名称和命名空间加载已安装的文档设计技能。缺少必需资料时暂停依赖部分，不静默跳过规则或自动安装依赖。以上是请求示例，不是已完成部署记录。

## 语言与维护

英文是唯一安装指令版本和规范性来源。[中文译文](translations/zh-CN/README.md)用于开发者理解与维护，不作为运行技能；英文指令不强制决定用户对话或交付产物的语言。

同一次变更中同步对应译文。运行脚本及测试只在所属英文技能目录维护一份。遵循[维护规则](translations/zh-CN/AGENTS.zh-CN.md)。

## 分发与许可证

Codex 与 Claude Code 使用同一个五技能插件；skills.sh 支持 GitHub 安装与发现，SkillsMP 索引公开源技能。市场安装不等于公共目录审核通过。见[分发说明](translations/zh-CN/docs/distribution.md)、[提交准备](translations/zh-CN/docs/submission.md)及[验证记录](translations/zh-CN/docs/verification.md)。

采用 [MIT](LICENSE)。所有者已确认改编的 CC Connect 镜像脚本也可按 MIT 分发，见[来源与许可说明](translations/zh-CN/docs/provenance.md)。

## 能力边界

- 技能提供执行指导，实际结果取决于权限、集成与验证；本身不提供托管、CI 服务或自动部署。
- MySQL 规则包含项目约定：显式事务内禁止查询，禁止外键、`CHECK` 和存储过程；采用前先阅读正文。
- CC Connect 镜像为可选只读副本，随包 Codex 适配器针对 legacy 会话和 IPC v11，服务部署方式为 macOS。真实消息收发、桌面显示、登录恢复和兼容性须在目标机器验证。
- 脚本保留既有中文标题处理和测试数据，英文技能指令不改变运行文案。
