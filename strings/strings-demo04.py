"""注释 vs docstring：看着都是说明，性质完全不同。

    python3 strings/strings-demo04.py

拆自 01_strings.py 的第 ③ 节。
"""

#==============================================
print()
print(f"  本文件的模块 docstring 前 20 字: {__doc__[:20]!r}…")

# ── ③-1 __doc__ 是「属性」，不是一个全局变量 ────────────────────────
# 每个能装说明的东西身上各挂一份自己的，互相看不见。
# 点左边写谁，读的就是谁的；光秃秃不带点的才是模块自己那份。
print()
print("  ③-1 每个对象各有各的 __doc__")

def with_docstring():
    """这是 docstring：第一条语句是字符串，会被存进 __doc__。"""
    return 1

class Tool:
    """类的 docstring。"""

    def run(self):
        """方法的 docstring。"""


print(f"    模块  __doc__          = {__doc__[:12]!r}…")
print(f"    函数  with_docstring   = {with_docstring.__doc__[:12]!r}…")
print(f"    类    Tool             = {Tool.__doc__!r}")
print(f"    方法  Tool.run         = {Tool.run.__doc__!r}")
print("    规则完全一样：看它自己的第一条语句是不是字符串。")

# ── ③-2 没写 docstring ≠ 这个变量不存在 ────────────────────────────
# 出处：strings/strings-demo03.py 踩过的坑 —— 那个文件第一行是 print()，
# 于是 __doc__ 被赋成 None，最后一行 __doc__[:20] 直接崩。
print()
print("  ③-2 没写 docstring 时，__doc__ 存在、但值是 None")


def no_doc():
    return 1


print(f"    no_doc.__doc__ = {no_doc.__doc__!r}          ← 属性在，值是 None")

try:
    no_doc.__doc__[:20]
except TypeError as e:
    print(f"    no_doc.__doc__[:20] → TypeError: {e}")

try:
    no_doc.__docXX__
except AttributeError as e:
    print(f"    no_doc.__docXX__    → AttributeError: {e}")

print("    两个错要分清：TypeError = 名字找得到但值不对；")
print("                  AttributeError / NameError = 名字压根不存在。")

# ── ③-3 它就是个普通属性，能读也能改 ──────────────────────────────
print()
print("  ③-3 Python 只是「顺手」帮你赋值，没有魔法")


def greet():
    """原来的说明。"""
    return 1


print(f"    改之前: {greet.__doc__!r}")
greet.__doc__ = "运行时改掉的说明。"          # 就是个普通属性赋值
print(f"    改之后: {greet.__doc__!r}")

# ── ③-4 三引号只是引号，换行和缩进原样存进去 ──────────────────────
print()
print("  ③-4 三引号不进值里；换行、空格原样保留")


def multi():
    """第一行。

        缩进的第二段
    """
    return 1


print(f"    repr : {multi.__doc__!r}")
print(f"    长度 : {len(multi.__doc__)}   ← 换行符 \\n 也算 1 个字符")

# 想拿「洗干净」的版本（去掉公共缩进和首尾空行）用 inspect.getdoc
import inspect

print(f"    洗净 : {inspect.getdoc(multi)!r}")
print("    中文和英文一样都算 1 个字符，全角标点也是 1 个（数的是字符数，不是显示宽度）。")

# ── ③-5 谁会真的去读这份 __doc__ ──────────────────────────────────
print()
print("  ③-5 谁在读 __doc__")
print("    help(fn)          → 交互式文档，打印的就是这一份")
print("    IDE 悬浮提示      → 同一份")
print("    @tool 装饰器      → 打包进 HTTP 请求发给模型，要算 input token")
print("      出处：demos/chapter1/01_single_tool.py:133 get_weather 的 docstring")
print("    注意 @tool 读的是【函数身上】那份，跟模块的那份没关系。")






