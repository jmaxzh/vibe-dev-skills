> 中文维护译文，仅供开发者对照，不是技能安装或执行入口。与[英文原文](../../../../../skills/cc-connect-integration/references/codex-mirror-example.md)同步，差异以英文为准。

# Codex 镜像实现

## 能力与适用范围

随包实现基于用户提供的 CC Connect → Codex 桌面镜像脚本包改造。CC Connect 负责消息收发和调用编程工具；随包脚本只将 Codex 源会话中已完成的文本问答同步为桌面副本，不调用模型生成回答。

```text
消息平台 → CC Connect → 独立执行环境中的 Codex 源会话
                │
                └─ 已完成问答 → 同步服务 → 桌面端会话副本
                                  │
                                  └─ 连接服务 → 桌面订阅更新
```

| 脚本 | 职责 |
| --- | --- |
| `service.py` | 持久化会话映射及问答、去重、标题、投影、列表索引及归档处理 |
| `broker.py` | 长驻桌面订阅连接及运行目录内的本地 broker socket |
| `mirror_ipc.py` | 桌面内部 IPC 帧、订阅通知及显示状态适配 |
| `codex_rpc.py` | 启动 App Server，调用项目和会话接口 |
| `titles.py` | 优先明确会话名，否则提取首条实质请求；标题稳定、重名加会话标识 |
| `config.py` | 加载统一配置、检查路径、源记录、数据库及副本格式 |
| `compatibility.py` | 检查 API schema、原生项目 ID 及桌面 IPC 初始化 |
| `prepare.py` | 查询项目或生成部署包与可选 macOS 用户服务文件，不安装服务 |
| `test_*.py` | 在临时目录和模拟接口中验证同步、归档及配置行为 |

实现使用 Python 标准库、Unix socket 和 `fcntl`。已提供的部署方式为 macOS 用户服务；其他操作系统未验证，不应把生成器或同步脚本视为已有跨平台实现。选择具备所用标准库 API 的 Python，通过随包测试验证，不绑定某个解释器安装位置。

`codex-legacy-ipc-v11` 是实现支持的协议和会话格式标识，不是需要安装的 Codex 版本号。实现依赖实验性 App Server API、legacy rollout、桌面内部 IPC v11、包含所需字段的 `threads` 表及桌面写锁机制。这些依赖不能通过修改配置值适配其他协议；检查失败时先适配代码和测试，不猜测数据库或协议结构。

不包含附件、工具过程镜像和双向续聊。其他编程工具需要独立的存储及订阅适配。原包报告的 15 项历史测试和实机验证仅说明其当时环境，不能替代此版本及目标机器验收。

## 统一配置

脚本仅在[英文技能的 `scripts/` 目录](../../../../../skills/cc-connect-integration/scripts)维护。本文命令从该目录执行，或使用脚本的实际完整路径。以下 JSON 中每个值都必须替换；它展示字段含义，不代表实际机器配置：

```json
{
  "codex_bin": "/example/tools/codex",
  "desktop_home": "/example/data/desktop",
  "execution_home": "/example/data/executor",
  "work_dir": "/example/projects/project-a",
  "project_id": "native-project-id-from-this-desktop",
  "sessions": "/example/connect/sessions/actual-project.json",
  "runtime_dir": "/example/mirror/project-a",
  "database": "/example/data/desktop/actual-state.sqlite",
  "ipc_socket": "/example/data/desktop/ipc/actual.sock",
  "python_bin": "/example/tools/python3",
  "cc_bin": "/example/tools/cc-connect",
  "cc_config": "/example/connect/config.toml",
  "service_prefix": "org.example.project-a.mirror",
  "model": "available-model-selected-for-this-project",
  "reasoning_effort": "effort-supported-by-the-selected-model",
  "source_label": "消息平台名称",
  "adapter": "codex-legacy-ipc-v11"
}
```

- 路径展开 `~` 并规范化为绝对路径；相对路径、未知字段及缺失必填字段会被拒绝。可执行文件和已有输入必须真实存在。
- `desktop_home` 是接收副本的桌面数据目录；`execution_home` 是 CC Connect 的独立 Codex 环境，两者不能相同或嵌套。认证共享另按认证后端配置，生成器不会修改凭证。
- `database` 必须是所选桌面目录内实际使用的数据库文件，不根据固定文件名或“最大版本号”猜测。检查 `threads` 结构和桌面实际配置后明确选择；不创建或迁移数据库。
- `ipc_socket` 是该桌面实例的实际 socket，区别于自动生成的 `runtime_dir/broker.sock`。
- `runtime_dir` 与两份会话环境分开，路径需足够短以满足 macOS Unix socket 长度限制。每套实例使用不同运行目录、服务前缀和源映射；同一源文件不要交给两个实例重复同步。
- 模型、推理强度影响副本元数据，不会自动改变 CC Connect 执行端模型；两边应按需要分别配置。来源标签用于副本标题，不限定飞书。
- 一套配置处理一个原生项目与一个源 sessions 文件；多项目采用独立配置及运行目录。已有日志只能用于原来的源映射和桌面目标，切换目标需要单独迁移。

## 查询与生成

下列命令中的大写 shell 变量均需在运行相应命令前赋值：可执行文件和数据目录来自实机发现，配置文件及部署包目录按本次部署选择。`SCRIPTS_DIR` 指英文技能 `skills/cc-connect-integration/scripts/` 的实际绝对路径。

先验收 CC Connect 主链路，在桌面端打开接收副本的项目。确认该桌面使用的 CLI，再以实际路径查询原生项目 ID：

```sh
"$PYTHON_BIN" prepare.py --list-projects \
  --codex-bin "$CODEX_BIN" --desktop-home "$DESKTOP_HOME"
```

`project/list` 查询的是该桌面的原生项目 ID，不使用其他应用管理接口返回的另一类 ID。源 sessions 文件从真实运行记录确认，不猜测文件名。

将替换示例值后的 JSON 保存到 `CONFIG_FILE` 指定的文件，再生成部署包：

```sh
"$PYTHON_BIN" prepare.py --config "$CONFIG_FILE" --output "$BUNDLE_DIR" --launchd
```

`--launchd` 仅在 macOS CLI 中允许；不传时只生成脚本及部署配置。包装器需要额外运行时目录时使用可重复的 `--path-entry "$EXTRA_BIN_DIR"`；后台 PATH 不继承终端初始化文件。

输出目录必须不存在。输出包含 `bin/`、规范化后的 `deployment.json` 和可选 `LaunchAgents/`，不含凭证内容。生成器检查文件、数据库字段和源记录，但不启动模型、安装文件、创建运行目录或修改已安装服务。

## 检查、安装与启动

先在准备好的包中执行：

```sh
"$PYTHON_BIN" "$BUNDLE_DIR/bin/service.py" \
  --config "$BUNDLE_DIR/deployment.json" --check
```

完整检查会读取源文件与数据库、在临时 `CODEX_HOME` 导出当前 CLI 的实验性 API schema、以桌面目录启动短暂 App Server 查询项目，以及连接真实桌面 IPC 做初始化。它不创建副本或模型回合；App Server 自身可能产生运行日志。执行前须打开桌面应用；该命令包含运行时接口探测，不能视为无副作用的静态检查。

检查只证明所需 API 字段、legacy 枚举、项目和 IPC 初始化可用；IPC 初始化不能证明全部 v11 订阅语义，仍需目标环境实测。API schema 导出行为以 [OpenAI App Server 文档](https://learn.chatgpt.com/docs/app-server)为入口，实验性项目字段及桌面内部协议以实际 CLI 和目标环境为准。

确认没有重复服务后安装生成文件。首次部署创建权限受限的 `runtime_dir`，把 `bin/` 和 `deployment.json` 放到该目录；将生成的 plist 放到实际用户 LaunchAgents 目录。已有部署先备份状态并停止受影响服务，再有选择地更新这些文件，保留 `mirror-*.json`。

检查 plist：`connect` 使用配置中的执行端目录，`broker` 和 `sync` 使用桌面目录；脚本、配置和日志路径指向最终运行目录，而不是临时包目录。按需只安装镜像两项服务，沿用已有 CC Connect 服务；不要再次安装 `connect` 造成重复进程。

使用 `launchctl bootstrap "gui/$(id -u)" "$PLIST_FILE"` 分别加载所需服务；顺序为主链路（若尚未运行）、broker、sync。每个服务文件均应先设置对应的 `PLIST_FILE`。broker 和 sync 启动时先检查文件、schema 及项目；broker 随后连接桌面 IPC，sync 在 IPC 初始化成功前等待，不写入副本。桌面尚未启动或暂不可达时会继续等待，明确的不兼容响应则退出。已启动 broker 遇桌面暂时断开会重连，sync 遇短时连接错误会保留日志并重试。

生成的服务随用户登录启动，但 `KeepAlive` 为 false，进程退出后不会由 launchd 自动重启，以免兼容性错误反复触发写入。桌面尚未启动时等待连接；文件、接口等检查失败时需要修复后显式启动。应在目标机器验证登录恢复与桌面启动时序，不能仅凭 plist 推断自启动恢复成功。

## 同步、归档与维护

映射使用源会话键与源会话创建时间的组合作为标识，已完成问答按内容和时间去重。持久化 `mirror-*.json` 包含副本初始记录、映射及问答，是重启恢复依据；删除它可能导致重复创建副本。

同步只短时持有对应副本写锁，不接管源会话。写前检查当前 rollout 的身份与路径；写锁冲突时保留 pending 等待补写。桌面拥有归档决定，服务每次读取实际路径及归档状态，归档后继续更新归档文件且不发送取消归档通知。手动取消归档后沿用原副本 ID；已删除副本不自动重建。

运行目录内的 `status.json` 提供连接、轮数、pending 及归档摘要，`sync.log`、`broker.log`、`connect.log` 供排查。`broker-state.json` 和镜像日志包含正文，应按私人会话数据管理。状态字段不能替代真实收发和桌面显示验收。

- 普通同步维护：只重启 `${service_prefix}.sync`；修改配置前先停止对应服务。
- broker 或内部协议维护：停止 sync，关闭桌面，重启 broker，再打开桌面并恢复 sync。原实现曾出现 broker 断开后已打开视图不重新订阅的问题，因此需按此顺序恢复，并验证副本重新订阅；进程存在不能证明订阅已恢复。
- 服务状态用 `launchctl print "gui/$(id -u)/$SERVICE_LABEL"`，显式重启用 `launchctl kickstart -k "gui/$(id -u)/$SERVICE_LABEL"`，卸载用 `launchctl bootout "gui/$(id -u)/$SERVICE_LABEL"`。每次设置实际标签，不沿用其他实例。
- schema、rollout 或接口不兼容时停止镜像并适配。不要改数据库字段、删除锁、取消归档或覆盖其他会话来消除报错。

| 现象 | 检查与恢复 |
| --- | --- |
| 不生成副本 | 先查源文件中是否有完成问答及 `agent_type=codex`，再查原生项目 ID、完整检查和同步日志 |
| 打开副本后不更新 | 查 broker 连接及近期是否重启 broker 或升级桌面，恢复后实测订阅 |
| pending 长期不消失 | 查写锁、实际归档路径、数据库行是否仍存在；保留日志，不自动覆盖或重建 |
| 归档副本重新出现 | 查是否有重复旧进程或其他脚本发送取消归档通知；本实现不主动取消归档 |
| 后台启动失败 | 查结构检查、桌面是否打开、路径及包装器运行时；修复后显式启动 |

## 验证

运行隔离回归测试：

```sh
"$PYTHON_BIN" -B -m unittest discover -s "$SCRIPTS_DIR" -v
```

测试使用临时目录、模拟 RPC 与临时 socket，不向真实消息平台发送消息。当前套件覆盖原包的完成问答、标题及归档行为，并增加配置传递、生成不改既有部署、多实例标识、无数据库时不创建、schema/IPC 检查失败、稳定副本及重启恢复。

在目标机器上另行验收：

- 主链路：在指定会话验证实际收发。
- 连续同步：同一会话完成三轮问答后，副本 ID 保持不变，问答无重复；打开副本时，源会话仍可续聊。
- 话题隔离：启用话题隔离时，新话题得到独立副本。
- 归档：归档后继续追加内容，且副本不恢复为活动项；手动取消归档后，历史内容完整。
- 恢复：同步服务重启后继续更新原副本；用户退出登录并重新登录后，服务启动顺序和状态符合预期。

令牌并发刷新、新版本兼容性及桌面真实显示均不由隔离测试保证。
