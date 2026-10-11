import subprocess
import sys


def read_file(file_path):
    """
    读取本地代码文件。

    参数:
        file_path: 文件路径

    返回:
        文件内容或者错误信息
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"错误：找不到文件 {file_path}"
    except Exception as e:
        return f"读取文件发生错误：{str(e)}"


def run_python(code):
    """
    执行一段 Python 代码。

    参数:
        code: Python 代码字符串

    返回:
        程序运行结果或者错误信息
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            if not result.stdout.strip():
                return "程序执行成功，但没有输出。"
            return result.stdout

        return result.stderr
    except subprocess.TimeoutExpired:
        return "错误：代码运行超过 5 秒，已停止执行。"
    except Exception as e:
        return f"执行代码发生错误：{str(e)}"
