# CodeHelperAgent

一个基于火山方舟 Doubao-Seed-1.6-Flash 的简单代码助手 Agent。

## 1. 项目功能

- 解释代码逻辑
- 生成代码注释
- 回答编程问题
- 读取本地代码文件
- 执行简单 Python 代码
- 支持上下文记忆
- 支持工具调用
- 支持 API 错误重试

## 2. Agent 基本流程

```text
用户输入
   ↓
Agent
   ↓
LLM 推理
   ↓
是否需要工具？
  ↙       ↘
是         否
↓           ↓
调用工具    直接回答
↓
获得工具结果
↓
再次交给 LLM
↓
最终回答
```

## 3. 项目结构

```text
CodeHelperAgent/
├── main.py
├── agent.py
├── tools.py
├── config.py
├── test_api.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── test_code/
│   └── example.py
└── docs/
```

## 4. 文件作用

### main.py

程序入口，负责命令行交互。

### agent.py

Agent 核心，实现：

- LLM API 调用
- Agent Loop
- 工具调用
- 上下文记忆
- 错误重试

### tools.py

定义 Agent 可以使用的工具：

- `read_file`
- `run_python`

### config.py

读取 API Key、模型、API 地址以及其他配置。

### test_api.py

单独测试 API 是否能够正常调用。

## 5. 第一步：测试 API

运行：

```bash
python test_api.py
```

成功后应该看到：

```text
API Key：读取成功
API 调用成功！
```

如果出现：

```text
404
InvalidEndpointOrModel.NotFound
```

重点检查：

1. `ARK_MODEL` 是否正确
2. 是否应该使用 Endpoint ID
3. Endpoint 是否属于当前项目
4. API Key 是否属于同一个项目
5. 模型是否已经开通
6. 当前 Endpoint 是否允许访问该模型

如果出现：

```text
Connection error
```

重点检查：

1. 网络
2. DNS
3. 系统代理
4. VPN
5. 火山方舟 API 地址

## 6. 第二步：运行 Agent

API 测试成功以后运行：

```bash
python main.py
```

启动后可以输入：

```text
请解释下面的代码：

def add(a, b):
    return a + b
```

也可以输入：

```text
请读取 test_code/example.py，并解释代码。
```

或者：

```text
请运行下面的 Python 代码：

x = 10
y = 20
print(x + y)
```

## 7. 工具调用示例

例如：

```text
请读取 test_code/example.py，运行它，然后解释运行结果。
```

Agent 会执行：

```text
用户请求
↓
LLM 分析
↓
调用 read_file
↓
读取 example.py
↓
调用 run_python
↓
得到运行结果
↓
LLM 综合分析
↓
最终回答
```

这就是本项目最核心的 Agent Loop。

## 8. 技术栈

| 技术 | 作用 |
|---|---|
| Python | 项目开发语言 |
| Doubao-Seed-1.6-Flash | 大语言模型 |
| 火山方舟 Ark API | LLM 服务 |
| requests | HTTP API 调用 |
| python-dotenv | 环境变量管理 |
| subprocess | Python 代码执行 |

## 9. 后续可以扩展

- 增加 C/C++/Java 代码分析
- 增加 Web UI
- 增加代码搜索
- 增加 GitHub 项目读取
- 增加代码修改工具
- 增加项目级代码分析
- 增加 RAG 知识库
- 增加更完善的安全沙箱

## 10. 项目目标

通过这个项目学习和实践：

```text
LLM API
↓
Prompt
↓
Tool Calling
↓
Agent Loop
↓
Context Memory
↓
Error Handling
↓
AI Agent
```

最终实现一个可以理解代码、调用工具并完成实际编程任务的简单 AI 代码助手。
