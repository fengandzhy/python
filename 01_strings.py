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
