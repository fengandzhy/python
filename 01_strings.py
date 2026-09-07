"""字符串：f-string、切片、docstring、注释。

    python3 01_strings.py          # 或 uv run python 01_strings.py

这些都是你在 demos/ 里实际撞到过的，每条标了出处。
"""

# ══════════════════════════════════════════════════════════════════════
print("═" * 62)
print("① f-string —— 前面加 f，大括号里的表达式会被求值")
print("═" * 62)
# 出处：demos/chapter1/01_single_tool.py 的 return f"{city} 今天天气晴朗…"

city = "北京"
temp = 25

print("  普通字符串:", "{city} 今天 {temp} 度")      # 大括号原样输出
print("  f-string:  ", f"{city} 今天 {temp} 度")     # 被替换

# 大括号里能放任何【表达式】，不只是变量名
print("  运算:      ", f"{temp * 2}")
print("  函数调用:  ", f"{len(city)}")
print("  方法链:    ", f"{city.upper()}")
print("  条件:      ", f"{'热' if temp > 30 else '舒适'}")

# 大括号本身是「插槽」语法，不是表达式。想输出真正的大括号要写两个
print("  字面大括号:", f'{{"city": "{city}"}}')

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("② 切片 [start:end] —— 取一段")
print("═" * 62)
# 出处：demos 里到处都是的 content[:40]，用来截断模型的长回答
#
# 冒号是【分隔符】：s[起点:终点:步长]，三个槽位两个冒号。
# 省略的是「值」不是「冒号」—— s[:1] 那个 1 是终点，s[::1] 那个 1 是步长。
# 详细拆解见 strings/strings-demo02.py。

s = "北京今天天气晴朗，气温 25°C，适合外出活动。"
print(f"  原文({len(s)} 字): {s}")
print(f"  s[:6]    = {s[:6]!r}       前 6 个")
print(f"  s[6:12]  = {s[6:12]!r}     第 6~11 个")
print(f"  s[-6:]   = {s[-6:]!r}      最后 6 个")
print(f"  s[::2]   = {s[::2]!r}      每隔一个取（第三个数是步长）")
print(f"  s[::-1]  = {s[::-1][:12]!r}…  倒序（步长为负，是唯一的切片倒序写法）")

# 关键：切片超出长度不会报错，给多少算多少
print(f"  '短'[:40] = {'短'[:40]!r}   ← 不用先判断长度，直接切就行")

# ══════════════════════════════════════════════════════════════════════
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

# ── ③-1 __doc__ 是「属性」，不是一个全局变量 ────────────────────────
# 每个能装说明的东西身上各挂一份自己的，互相看不见。
# 点左边写谁，读的就是谁的；光秃秃不带点的才是模块自己那份。
print()
print("  ③-1 每个对象各有各的 __doc__")


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

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("④ 格式说明符 —— 冒号后面控制对齐和宽度")
print("═" * 62)
# 出处：demos/chapter1/06_memory_scope.py 里的 f"  第{i}轮  {q:<12}{n:<8}"

rows = [("北京", 25, 690), ("上海", 26, 803), ("广州", 30, 953)]
print(f"  {'城市':<8}{'气温':>6}{'tokens':>10}")
for c, t, tok in rows:
    print(f"  {c:<8}{t:>6}{tok:>10}")
print("    <  左对齐    >  右对齐    ^  居中    数字是宽度")

print(f"  {3.14159:.2f}      ← .2f 保留两位小数")
print(f"  {1234567:,}   ← 千分位")
print(f"  {0.856:.1%}     ← 百分比")
