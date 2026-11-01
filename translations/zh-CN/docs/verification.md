> 中文维护译文，与[英文原文](../../../docs/verification.md)同步，差异以英文为准。

# 分发验证记录

验证日期：2026-11-01。实现提交 `41f0c4e` 已完成审查、快进合并到 `main` 并推送到 GitHub。下表分别记录本地和远端检查。

| 检查 | 状态与证据 |
| --- | --- |
| Codex 本地市场和插件安装 | 临时 `CODEX_HOME` 中通过；`codex-cli 0.166.0-alpha.5.1` |
| Codex 运行时发现 | app-server `skills/list` 返回属于 `vibe-dev-skills@vibe-dev-skills` 的五项已启用技能，安装资料可读 |
| Claude Code 原生验证与安装 | 临时 `CLAUDE_CONFIG_DIR` 中通过；`2.1.267`；严格清单校验通过，组件清单包含五项技能 |
| 源文件、译文与本地链接 | `scripts/validate.py` 通过：五项英文入口、带来源译文、本地路径与锚点、声明和清单一致 |
| 安装组合与发布归档 | 8 项分发测试通过，覆盖套件、双技能、专项单装、缺失依赖、越界链接、清单和资产错误、可重复英文 ZIP 及既有产物保护 |
| skills CLI 发现与安装 | 固定 `skills@1.7.4` 在临时项目通过默认与完整扫描、套件、双技能、四项专项安装及预期缺失依赖识别，遥测已关闭 |
| CC Connect 隔离回归 | 28 项测试通过，12 个 Python 源码和测试文件与迁移前逐字节一致 |
| 模型执行与依赖遵循 | 未执行；清单与文件检查不证明模型会加载依赖或在缺失时正确暂停 |
| CC Connect 真实消息与桌面表现 | 未在部署目标验证 |
| 远端 GitHub 安装 | GitHub API 与 HTTPS `ls-remote` 确认 `main` 为 `41f0c4efc9c63b71406cbbe18d505660942b83be`。skills CLI 远端来源冒烟检查两次在发现阶段超时，不能判定远端安装通过 |
| GitHub CI | 实现提交 `41f0c4e` 的[运行 41294750749](https://github.com/jmaxzh/vibe-dev-skills/actions/runs/41294750749)成功完成 |
| skills.sh / SkillsMP 收录 | 本次未提交或确认 |
| OpenAI / Anthropic 公共目录 | OpenAI 登录成功，但上传被已验证开发者身份要求阻塞；Anthropic 需要登录。均未上传或提交 |

复现方法见[分发说明](distribution.md)。冒烟报告区分本地 CLI 安装、命名空间发现、缺失依赖文件检查和模型行为。宣称行为验收通过或提交公开目录前，完成新会话的正负面模型检查。

完整冒烟脚本通过 12 项记录检查，含实际原生安装和 Codex 命名空间运行时目录。审阅 ZIP 为 `dist/vibe-dev-skills-0.1.0.zip`，机器可读报告为 `dist/install-report.json`，两者均未上传。
