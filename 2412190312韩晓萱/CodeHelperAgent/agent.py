import json
import time

try:
    from arkruntime import Ark
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "缺少方舟 SDK：请先运行 `python -m pip install -r requirements.txt` 安装依赖。"
    ) from exc

from config import ARK_API_KEY, MODEL
from tools import read_file, run_python


client = Ark(
    api_key=ARK_API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)


SYSTEM_PROMPT = """
你是一个代码解释助手 Agent。

你的主要职责：
1. 解释用户提供的代码。
2. 按照代码执行顺序分析程序逻辑。
3. 为代码生成清晰的中文注释。
4. 回答用户提出的编程问题。
5. 当用户需要分析本地文件时，可以使用 read_file 工具。
6. 当需要验证 Python 代码实际运行结果时，可以使用 run_python 工具。

使用工具时需要遵守：
1. 用户询问普通编程知识时，不需要调用工具。
2. 用户要求读取某个本地文件时，使用 read_file。
3. 用户明确要求运行 Python 代码，或者必须通过运行才能确认结果时，使用 run_python。
4. 不要进行没有必要的工具调用。

回答要求：
1. 默认使用中文。
2. 面向编程初学者解释。
3. 优先按照代码实际执行顺序解释。
4. 遇到错误时说明错误原因。
5. 如果工具调用失败，不要编造结果。
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取用户指定的本地代码文件，获得该文件中的完整代码内容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "需要读取的文件路径，例如 test_code/example.py",
                    }
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "执行一段 Python 代码，返回程序的标准输出或者错误信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "需要执行的完整 Python 代码",
                    }
                },
                "required": ["code"],
            },
        },
    },
]


def execute_tool(tool_name, arguments):
    if tool_name == "read_file":
        return read_file(arguments["file_path"])
    if tool_name == "run_python":
        return run_python(arguments["code"])
    return f"错误：未知工具 {tool_name}"


def call_model(messages):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )
        except Exception as e:
            print(f"\n[API 调用失败] {str(e)}")

            if attempt < max_retries - 1:
                print("正在重新尝试...")
                time.sleep(2)
            else:
                raise


class CodeHelperAgent:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def chat(self, user_input):
        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        while True:
            response = call_model(self.messages)
            message = response.choices[0].message

            if not message.tool_calls:
                answer = message.content or "模型没有返回内容。"
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )
                return answer

            self.messages.append(
                {
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments,
                            },
                        }
                        for tool_call in message.tool_calls
                    ],
                }
            )

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name

                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}

                print(f"\n[Agent 调用工具] {tool_name}")
                print(f"[工具参数] {arguments}")

                try:
                    tool_result = execute_tool(tool_name, arguments)
                except Exception as e:
                    tool_result = "工具执行失败：" + str(e)

                print("[工具执行完成]")

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_result),
                    }
                )
