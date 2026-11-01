> 中文维护译文，与[英文原文](../../../docs/distribution.md)同步，差异以英文为准。

# 验证与分发套件

从仓库根目录运行命令。安装检查使用临时项目与插件配置，不修改日常代理配置，也不调用模型。

## 本地验证

```sh
python3 -B scripts/validate.py
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s skills/cc-connect-integration/scripts -v
python3 -B scripts/smoke_install.py --native
```

冒烟检查需要 Node/npm、获取 `skills@1.7.4` 的网络连接；`--native` 还需要 Codex 和 Claude CLI。检查默认及完整深度发现、五技能套件、工作流双技能组合、四项专项单装，以及故意缺少依赖的工作流安装。缺失依赖结果是文件和组合校验，不证明模型遵循指令。原生检查执行本地注册、安装并读取真实技能清单；Codex app-server 查询不创建模型回合。

报告写入 `dist/install-report.json`。指定 `--native` 后，超时或 CLI 不可用视为失败，不将跳过或失败记作通过。GitHub Actions 执行便携检查、脚本测试、skills CLI 冒烟检查及安装报告上传，不声称覆盖运行器中不存在的原生客户端。

## 手动检查原生客户端

将 `CHECKOUT` 设为检出目录实际绝对路径。下列命令会修改执行时所用客户端配置；测试时应像冒烟脚本一样使用临时配置。

```sh
codex plugin marketplace add "$CHECKOUT"
codex plugin add vibe-dev-skills@vibe-dev-skills
claude plugin marketplace add "$CHECKOUT"
claude plugin install vibe-dev-skills@vibe-dev-skills
```

在新的本地会话确认真实注册名，仅调用工作流完成需求，观察其产出文档时加载文档设计技能，而非全部专项技能。再使用临时的工作流单装环境：代理应识别缺少 `sdlc-instr-doc-design`，暂停依赖的文档任务，解释双技能安装方式，不自行安装。模型表现与 CLI 清单检查分开记录，不为负面测试移除日常使用的文档设计技能。

## 发布并检查 GitHub 安装

仅在明确授权后发布已审阅的仓库变更，再运行：

```sh
python3 -B scripts/smoke_install.py --source jmaxzh/vibe-dev-skills
```

来源须与本地待验证技能一致。发布前远端仍是旧结构，本地冒烟通过不代表远端通过。既有手动安装先备份，再从新 `skills/` 目录更新；移除旧根路径，不保留兼容符号链接。

公开命令见[项目说明](../../../README.zh-CN.md#安装)。Codex 和 Claude Code 安装整套；skills CLI 也支持工作流加文档设计组合，以及四项专项单装。不使用自定义依赖字段或安装器。

skills.sh 根据实际安装遥测进入目录，本验证禁用遥测。SkillsMP 索引公开 GitHub 的 `SKILL.md`。发布后核对各英文来源与索引链接，不承诺立即收录；缺失时仅在授权后使用平台当前官方反馈渠道，不伪造排名或提交重复中文技能。

来源：[OpenAI 打包](https://developers.openai.com/plugins/build/plugins)、[Claude 市场发布](https://code.claude.com/docs/en/plugins/publish)、[skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)、[skills.sh 收录](https://www.skills.sh/docs/faq)、[SkillsMP](https://skillsmp.com/about)。
