# Vibe Dev Skills

**面向软件开发全生命周期的 Agent Skills——从需求、设计到实施、测试与交付。**

[English](README.md) | 简体中文

将 Vibe Coding 想法转化为清晰的需求、技术方案，以及具有明确验证要求的实现。Vibe Dev Skills 提供 SDLC 主流程，并配套 UI、MySQL、文档设计和消息平台集成等专项技能。

主流程复用已有决策与证据，补齐缺失的前置成果，连续推进至你指定的阶段。专项技能也可独立使用。

## 技能

| 技能 | 用途 | 启用方式 |
| --- | --- | --- |
| [SDLC 工作流](locales/zh-CN/sdlc-workflow/SKILL.md) | 需求、技术方案、实施、测试及知识库维护 | 显式调用；项目初始化与知识库专项审查须单独明确要求 |
| [界面与交互设计](locales/zh-CN/sdlc-ui-interaction/SKILL.md) | 桌面端、移动端与网页的界面行为和设计 | 适用的 UI 任务 |
| [MySQL 数据表与 SQL 设计](locales/zh-CN/sdlc-mysql-design/SKILL.md) | 数据建模、SQL、索引、事务与并发控制 | 任务须明确以 MySQL 为目标数据库 |
| [指令与文档设计](locales/zh-CN/sdlc-instr-doc-design/SKILL.md) | 提示词、技能、指令及面向读者的文档 | 文档产物任务，不用于普通对话 |
| [CC Connect 集成](locales/zh-CN/cc-connect-integration/SKILL.md) | 消息平台接入本机编程工具的部署与维护，可选 Codex 桌面副本 | CC Connect 集成任务 |

## 安装

使用支持 `SKILL.md` 技能的编程代理。本仓库包含指令与参考资料，不是独立应用；技能发现方式和安装路径由所用工具决定，请使用该工具文档指定的技能目录。

1. 将仓库克隆到代理自动发现技能的目录之外：

   ```sh
   git clone https://github.com/jmaxzh/vibe-dev-skills.git
   cd vibe-dev-skills
   ```

2. 选择**一种**指令语言。默认使用英文；如需中文，采用下列设置：

   ```sh
   skill_source_dir="locales/zh-CN"
   # 如需默认英文版：
   # skill_source_dir="."
   ```

3. 将目标路径替换为所用工具的实际技能目录。替换已有安装前先备份；以下命令发现任一同名技能已存在时会停止。

   ```sh
   skill_target_dir="/absolute/path/to/your/agent/skills"
   mkdir -p "$skill_target_dir"

   for skill_name in sdlc-workflow sdlc-ui-interaction sdlc-mysql-design sdlc-instr-doc-design cc-connect-integration; do
     if [ -e "$skill_target_dir/$skill_name" ] || [ -L "$skill_target_dir/$skill_name" ]; then
       echo "Skill already exists: $skill_target_dir/$skill_name" >&2
       exit 1
     fi
   done

   for skill_name in sdlc-workflow sdlc-ui-interaction sdlc-mysql-design sdlc-instr-doc-design cc-connect-integration; do
     cp -R "$skill_source_dir/$skill_name" "$skill_target_dir/"
   done
   ```

4. 按所用代理的要求重新加载技能，确认五个技能名称均可用。

五个技能目录应并列安装，以保持跨技能引用有效。不要递归安装整个仓库，也不要同时安装两种语言：两个版本使用相同技能名称。复制时包含 `references/` 及 CC Connect 的 `scripts/`，不要只复制 `SKILL.md`。

## 使用示例

使用所用代理支持的语法显式调用主流程，或在请求中写出技能名称：

> 使用 sdlc-workflow。我想开发一个小型问题跟踪工具。先明确需求，再设计技术方案，最后实施并完成适当的测试。复用项目已有决策，遇到阻塞后续工作的未决事项时暂停受影响部分。

只推进到指定阶段：

> 使用 sdlc-workflow，将这个功能想法整理为需求和验收标准。停在技术方案阶段之前。

独立使用专项技能：

> 使用 sdlc-mysql-design，审查这份 MySQL 订单表结构和库存扣减 SQL。说明完整性与并发风险，区分项目约定和 MySQL 功能限制。

消息平台集成：

> 使用 cc-connect-integration，检查我现有的 CC Connect 部署，为选定的消息平台制定调整方案。先验证消息主链路，再考虑可选的桌面镜像。

以上内容是请求示例，不是已完成部署的记录或性能测试结果。

## 语言与维护

- 根目录技能为默认英文版。[中文版](locales/zh-CN/)包含全部五项技能、参考文档及相同的 CC Connect 脚本。
- 指令语言不强制决定对话或交付产物的语言；可在请求中明确你的偏好。
- 修改行为、条件、示例或链接时，同步维护对应翻译。技能名称、配置键和协议标识在两种语言中保持一致。
- 贡献技能或相关文档时，遵循[技能维护规则](locales/zh-CN/AGENTS.md)及其引用的设计原则。

## 能力边界

- 技能为代理提供执行指导；实际完成能力取决于工具权限、可用集成和验证结果。技能本身不提供托管、CI 或自动部署服务。
- MySQL 技能包含特定项目约定，例如显式事务内禁止查询、禁止外键、`CHECK` 和存储过程。采用前请阅读技能正文。
- CC Connect 桌面镜像为可选的只读副本功能。随包 Codex 适配器针对文档所述的 legacy 会话格式及 IPC v11；提供的部署方式为 macOS。兼容性、真实消息收发和桌面显示需要在目标机器验证。
- CC Connect 脚本在两个版本中保持相同行为，包括中文标题处理规则与测试数据。文档翻译不修改运行时文案，也不新增运行时语言选择器。
