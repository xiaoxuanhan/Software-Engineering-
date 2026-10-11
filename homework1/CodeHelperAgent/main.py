def main():
    try:
        from agent import CodeHelperAgent
    except RuntimeError as e:
        print(e)
        return

    agent = CodeHelperAgent()

    print("=" * 55)
    print("              CodeHelper Agent")
    print("              智能代码助手")
    print("=" * 55)
    print()
    print("支持功能：")
    print("1. 解释代码")
    print("2. 生成代码注释")
    print("3. 回答编程问题")
    print("4. 读取本地代码文件")
    print("5. 执行 Python 代码")
    print()
    print("输入 exit 或 quit 可以退出程序。")
    print("-" * 55)

    while True:
        try:
            user_input = input("\n你：").strip()
        except EOFError:
            print("\nCodeHelper Agent 已退出。")
            break

        if user_input.lower() in ["exit", "quit"]:
            print("\nCodeHelper Agent 已退出。")
            break

        if not user_input:
            continue

        try:
            answer = agent.chat(user_input)
            print("\nAgent：")
            print(answer)
        except Exception as e:
            print("\nAgent 运行发生错误：")
            print(str(e))


if __name__ == "__main__":
    main()
