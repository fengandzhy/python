"""字符串：f-string、切片、docstring、注释。

    python3 01_strings.py          # 或 uv run python 01_strings.py

这些都是你在 demos/ 里实际撞到过的，每条标了出处。
"""

# ═════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("③ 注释 vs docstring —— 看着都是说明，性质完全不同")
print("═" * 62)


def with_comment():
    # 这是注释：编译后就没了，运行时读不到
    return 1


def with_docstring():
    """这是 docstring：第一条语句是字符串，会被存进 __doc__。"""
    return 1


print(f"  with_comment.__doc__   = {with_comment.__doc__!r}")
print(f"  with_docstring.__doc__ = {with_docstring.__doc__!r}")
print()
print("  为什么这个区别重要：")
print("    @tool 装饰的函数，docstring 会被打包进 HTTP 请求发给模型，")
print("    还要算 input token；# 注释模型永远看不到。")
print("    出处：demos/chapter1/01_single_tool.py 里 get_weather 的 docstring")

# 判定规则只有一条：第一条语句是不是字符串字面量
print()
print("  判定规则：【第一条语句是不是字符串】")


def f1():
    "单引号也算"


def f2():
    x = 1
    """不在第一行就不算"""
    return x


def f3():
    f"f-string {1} 不算"   # f-string 是运行时表达式，不是字面量


for fn, label in [(f1, "单引号"), (f2, "不在第一行"), (f3, "f-string")]:
    print(f"    {label:14} __doc__ = {fn.__doc__!r}")

# 模块级也一样 —— 本文件开头那段就是模块 docstring
print()
print(f"  本文件的模块 docstring 前 20 字: {__doc__[:20]!r}…")