# AGENTS.md — Cursor 与本仓库

本仓库为**汽车软件**领域的技能与规则集合，在 **Cursor** 中打开即可配合 `.cursor/rules/` 使用。

## 必做（首次）

```bash
python -m tools.cursor_setup
```

将 **DeepSeek API Key** 保存到用户目录（见 `.cursor/rules/automotive-cursor.mdc`）。之后同一机器自动复用；也可用环境变量 `DEEPSEEK_API_KEY` 覆盖。

## 可选工具

- **LLM Council**：`python tools/llm_council.py "<topic>" -t general -r 1`
- **状态**：`python -m tools.cursor_setup --status`

## 内容地图

| 目录 | 用途 |
|------|------|
| `skills/` | 按领域拆分的技能说明（YAML/MD） |
| `rules/` | 编码、安全、功能安全等规则 |
| `agents/` | Agent 定义（YAML） |
| `workflows/` | 工作流 YAML |
| `knowledge-base/` | 标准与参考文档 |

在协助用户时，涉及汽车嵌入式、AUTOSAR、ISO 26262、诊断等主题，应引用上述目录中的具体文件路径。
