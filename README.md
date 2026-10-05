# headline-generator-lite

标题生成小工具。规则模板抽取核心关键词，组合出多个候选标题；配置 API key 时可选 LLM 润色。

## 功能

- 自动抽取高频关键词（中英混合）；
- 5 套标题模板组合多个候选；
- 配置 `OPENAI_API_KEY` 时调用 OpenAI 兼容接口生成；
- **无 key 自动降级为纯规则**，核心功能完整。

## 快速开始

```bash
python3 cli.py "人工智能 算法 芯片 芯片 算法 数据"
```

## 使用示例

```bash
# 强制只用规则
python3 cli.py "正文……" --no-llm

# 指定候选数
python3 cli.py "正文……" -n 5
```

## 有 API Key 时如何启用 LLM

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"   # 可选
export OPENAI_MODEL="gpt-3.5-turbo"                 # 可选
python3 cli.py "正文……"
```

## 无 API Key 如何运行

不设置任何环境变量直接运行，工具自动使用规则模板生成标题，结果里 `source` 为 `rule`。

## 目录结构

```
headline-generator-lite/
├── generator.py   # 关键词抽取、模板、可选 LLM
├── cli.py         # 命令行入口
├── tests/
│   └── test_generator.py
├── README.md
├── LICENSE
└── .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
