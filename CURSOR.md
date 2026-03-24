# Automotive Cursor Agents（项目说明）

这是面向 Cursor 的汽车软件工程增强仓库，聚焦 ADAS、功能安全、AUTOSAR、诊断与网络安全等领域。

## 首次配置

```bash
pip install -r requirements.txt
python -m tools.cursor_setup
python -m tools.cursor_setup --status
```

## 关键能力

- DeepSeek API Key 本地持久化（可被环境变量覆盖）
- LLM Council 多模型辩论能力
- 基于 `agents/` + `skills/` 的专家知识路由
- Cursor 规则增强（位于 `.cursor/rules/`）

## 常用命令

```bash
# 运行多模型辩论
python tools/llm_council.py "议题" -t general -r 1

# 运行测试
pytest tests/ -v

# 静态检查
ruff check tools/ scripts/
```

## 目录地图

- `skills/`: 领域技能知识
- `rules/`: 规则与约束
- `agents/`: 专家角色定义
- `workflows/`: 端到端流程
- `knowledge-base/`: 标准与参考资料
- `tools/`: 适配器与自动化工具

## 说明

本仓库当前定位为 Cursor 优先；若需要兼容历史生态，可保留相关兼容目录与脚本。
