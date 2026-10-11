from arkruntime import Ark

from config import ARK_API_KEY, MODEL


client = Ark(
    api_key=ARK_API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)


try:
    print("当前模型：", MODEL)
    print("开始调用豆包...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": "你好，只回复四个字：测试成功",
            }
        ],
    )

    print("\nAPI 调用成功：")
    print(response.choices[0].message.content)
except Exception as e:
    print("\nAPI 调用失败：")
    print("错误类型：", type(e).__name__)
    print("错误内容：", str(e))
    print("完整错误：", repr(e))
