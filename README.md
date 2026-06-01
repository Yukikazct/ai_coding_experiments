# Week 11 — AI Coding 实验

## 项目概述

本周实验包含两个模块：

| 模块 | 目录 | 内容 |
|------|------|------|
| MCP 协议实践 | `mcp/` | 构建一个代码质量分析 MCP Server |
| Prompt Engineering | `prompt_engineering/` | 练习 6 种 LLM Prompt 技术 |

---

## 环境依赖

- **Python** ≥ 3.10
- **Ollama** — 本地运行 LLM
  - `mistral-nemo:12b`（K-shot prompting）
  - `llama3.1:8b`（其余 5 个技术）
- **Python 包**: `mcp[cli]`, `ollama`, `python-dotenv`

```bash
# 安装 Ollama
brew install --cask ollama
ollama serve

# 拉取模型
ollama run mistral-nemo:12b
ollama run llama3.1:8b

# 安装 Python 依赖
pip install "mcp[cli]" ollama python-dotenv
```

---

## 目录结构

```
ai_coding_experiments/
├── README.md                          # 本文件
├── .gitignore
├── mcp/                               # MCP Server 模块
│   ├── code_analyzer_server.py        # MCP Server 主程序（3个工具）
│   ├── test_server.py                 # 功能测试（直接调用函数）
│   ├── test_mcp_protocol.py           # 协议冒烟测试（JSON-RPC）
│   └── samples/
│       ├── sample_code.py             # Python 示例文件
│       └── sample_code.js             # JavaScript 示例文件
└── prompt_engineering/                # Prompt 技术模块
    ├── assignment.md                  # 实验说明
    ├── k_shot_prompting.py            # 技术1: K-shot 提示
    ├── chain_of_thought.py            # 技术2: 思维链
    ├── tool_calling.py                # 技术3: 工具调用
    ├── self_consistency_prompting.py  # 技术4: 自一致性
    ├── rag.py                         # 技术5: RAG 检索增强生成
    ├── reflexion.py                   # 技术6: 反射调试
    └── data/
        └── api_docs.txt               # RAG 用 API 文档
```

---

## 模块一：MCP Code Analyzer

### 简介

基于 **FastMCP** 构建的代码质量分析 Server，向 AI 助手提供三个工具：

| 工具 | 功能 | 参数 |
|------|------|------|
| `analyze_file` | 分析单文件质量指标 | `file_path`, `metrics` |
| `scan_directory` | 扫描目录代码文件 | `directory_path`, `extensions` |
| `compare_files` | 对比两个文件结构差异 | `file_a`, `file_b` |

### 支持的指标

- **lines** — 总行数、代码行、注释行、空行
- **functions** — 函数/方法/类结构（AST + 正则）
- **complexity** — 圈复杂度估算（McCabe）
- **imports** — 导入/依赖分析

### 支持的语言

Python、JavaScript/TypeScript、Java、C++、Go、Rust、Ruby、PHP、Swift、Kotlin、Scala 等。

### 运行测试

```bash
cd mcp
python3.12 test_server.py          # 功能测试
python3.12 test_mcp_protocol.py    # 协议测试
```

---

## 模块二：Prompt Engineering

### 6 种 Prompt 技术

#### 1. K-shot Prompting（少样本提示）
- **文件**: `k_shot_prompting.py`
- **模型**: `mistral-nemo:12b`
- **任务**: 反转单词 "httpstatus" → "sutatsptth"
- **思路**: 在 prompt 中给出多个单词反转示例，特别将 "http" 和 "status" 分别作为示例，帮助模型分解复合词

#### 2. Chain-of-Thought（思维链）
- **文件**: `chain_of_thought.py`
- **模型**: `llama3.1:8b`
- **任务**: 计算 3^12345 mod 100
- **思路**: 引导模型使用欧拉定理和模幂运算逐步推导，最终给出 "Answer: 43"

#### 3. Tool Calling（工具调用）
- **文件**: `tool_calling.py`
- **模型**: `llama3.1:8b`
- **任务**: 模型输出 JSON 格式的工具调用指令
- **思路**: 严格定义工具 schema 和输出格式，要求模型只输出 JSON 不包含额外文本

#### 4. Self-Consistency（自一致性）
- **文件**: `self_consistency_prompting.py`
- **模型**: `llama3.1:8b`
- **任务**: 数学应用题（亨利骑行问题）
- **思路**: 运行 5 次推理（temperature=1），取多数答案作为最终结果

#### 5. RAG（检索增强生成）
- **文件**: `rag.py`
- **模型**: `llama3.1:8b`
- **任务**: 根据 API 文档生成 `fetch_user_name` 函数
- **思路**: 将 API 文档作为上下文注入 prompt，要求模型严格基于文档生成代码

#### 6. Reflexion（反射调试）
- **文件**: `reflexion.py`
- **模型**: `llama3.1:8b`
- **任务**: 生成密码验证函数并通过测试
- **思路**: 先生成初始实现，运行测试获取失败信息，将失败反馈传给模型进行自我修正

### 运行测试

```bash
cd prompt_engineering
python3.12 k_shot_prompting.py
python3.12 chain_of_thought.py
python3.12 tool_calling.py
python3.12 self_consistency_prompting.py
python3.12 rag.py
python3.12 reflexion.py
```

---

## 测试结果

| # | 模块 | 测试项 | 状态 |
|---|------|--------|------|
| 1 | MCP | `test_server.py`（6 项功能） | ✅ |
| 2 | MCP | `test_mcp_protocol.py`（协议） | ✅ |
| 3 | Prompt | K-shot Prompting | ✅ |
| 4 | Prompt | Chain-of-Thought | ✅ |
| 5 | Prompt | Tool Calling | ✅ |
| 6 | Prompt | Self-Consistency | ✅ |
| 7 | Prompt | RAG | ✅ |
| 8 | Prompt | Reflexion | ✅ |

---

