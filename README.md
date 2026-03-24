# Automotive Cursor Agents（汽车工程智能助手库）

本项目是面向 Cursor 的汽车软件工程知识与流程增强仓库，覆盖 ADAS、功能安全、AUTOSAR、诊断、网络安全、电池管理等核心域。

> 上游来源：本项目主要基于开源项目 [theja0473/automotive-claude-code-agents](https://github.com/theja0473/automotive-claude-code-agents) 进行 Cursor 化迁移与增强。

## 项目定位

- 在 Cursor 中直接使用汽车领域 `skills`、`rules`、`agents`、`workflows`、`knowledge-base`
- 提供 DeepSeek API 接入与本地持久化配置（`tools/cursor_config.py`、`tools/cursor_setup.py`）
- 保留 LLM Council 多模型辩论能力（`tools/llm_council.py`）

## 快速开始（Cursor）

```bash
# 1) 安装 Python 依赖
pip install -r requirements.txt

# 2) 初始化 DeepSeek Key（会保存到用户目录）
python -m tools.cursor_setup

# 3) 检查是否已配置
python -m tools.cursor_setup --status

# 4) 运行一次 LLM Council 验证
python tools/llm_council.py "Generate FTA for overcurrent protection in ASIL-D BMS" -t general -r 1
```

> 说明：`llm_council.py` 默认会并行调用两个模型（`deepseek-chat` + `deepseek-reasoner`），并在结束后进行一次综合结论（synthesis）。

## 运行前提

- Python 3.10+（推荐 3.11/3.12）
- 可访问 DeepSeek API（默认 `https://api.deepseek.com`）
- 已配置 `DEEPSEEK_API_KEY` 或已执行 `python -m tools.cursor_setup`

## Key 持久化机制

- 优先级：环境变量 `DEEPSEEK_API_KEY` > 本地配置文件
- 配置文件路径：
  - Windows：`%USERPROFILE%\.automotive-cursor-agents\config.json`
  - Linux/macOS：`~/.automotive-cursor-agents/config.json`
- 常用命令：
  - `python -m tools.cursor_setup --status`
  - `python -m tools.cursor_setup --force`
  - `python -m tools.cursor_setup --clear`

## 目录说明

- `skills/`：汽车领域技能知识（ADAS、功能安全、诊断、电池等）
- `rules/`：编码规范与安全规则（MISRA、ISO 26262、ISO 21434 等）
- `agents/`：角色型专家 Agent 定义
- `workflows/`：端到端流程模板（YAML）
- `knowledge-base/`：标准与实践参考文档
- `tools/`：CLI/适配器/LLM Council 工具链
- `tests/`：单元与集成测试

## 已迁移能力（Cursor 平台）

- DeepSeek 适配与统一配置读取
- Cursor 环境引导与规则文件（`.cursor/rules/`）
- Agent 到 Skill 的自动关联规则（提及 `Using automotive-...` 时自动解析）
- Cursor 文档入口（`AGENTS.md`、`CURSOR.md`）
- LLM Council 产物目录按真实模型名落盘（例如 `deepseek-chat/`、`deepseek-reasoner/`）
- LLM Council 成本按 token 实际用量计费并同时输出 CNY/USD

## LLM Council 输出与成本

- 产物目录默认在：`/tmp/llm-council-<pid>-<timestamp>`（Windows 常见映射为 `C:\tmp\...`）
- 关键文件：
  - `consensus/SYNTHESIS.md`：最终综合结论与 action items
  - `metrics/debate-stats.json`：轮次耗时、token 统计、成本明细
- 成本口径（DeepSeek）：
  - 输入缓存命中：0.2 元 / 百万 tokens
  - 输入缓存未命中：2 元 / 百万 tokens
  - 输出：3 元 / 百万 tokens
- CLI 与产物会同时显示人民币与美元金额（美元按代码中的汇率换算）

## 验证建议

```bash
# 运行测试
pytest tests/ -v

# 代码检查
ruff check tools/ scripts/

# 重点测试
python -m pytest tests/test_skills.py tests/test_agents.py
```

## 使用建议

- 在 Cursor 中直接提问汽车工程任务（如 FMEA/FTA、AUTOSAR、诊断策略）
- 若需要指定专家视角，明确写出 `Using automotive-xxx-agent`
- 涉及功能安全结论时，优先结合 `skills/automotive-safety/` 与 `rules/` 对齐术语和约束
- 若只想降低成本，可减少 `-r` 轮数，或后续改为单模型执行模式

## 许可

本项目遵循 [MIT License](LICENSE)。
