"""repr() 与 !r：让隐形的空白和转义符现形，顺带辨清这两种写法差在哪。

    python3 strings/strings-demo06.py

拆自 01_strings.py 的第 ④ 节；格式说明符本身见 strings-demo05.py。
"""

#==============================================
# ── ④-6 repr() 与 !r —— 让空白字符现形 ────────────────────────────
# strings-demo05.py 里 ④-2 / ④-3 的演示全靠它：空格是隐形的，
# 不加引号就没法证明「补了几个」。
# 槽位的完整语法其实是 {值!转换:格式说明符}，感叹号那段叫「转换标志」：
#     !s → str()    !r → repr()    !a → ascii()
# 别去找 {x!r} 和 {repr(x)} 的输出差别 —— 没有，调的就是同一个 repr()。
# 它俩差在「能写在哪儿」，见 ④-7。
print()
print("  ④-6 repr() 与 !r")

pad = f"{'北京':<8}"  # 宽度 8，内容 2 个字符 → 右边补了 6 个空格
print("    行尾光打印 : " + pad)
print("    ↑ pad 后面什么都没跟，6 个空格彻底隐形，连「有没有」都不知道")
print("    后面跟东西 : " + pad + "← 空隙是看见了，但几个空格？谁补的？判断不了")
print("    repr(pad)  : " + repr(pad))
print(f"    {{pad!r}}    : {pad!r}  ← 和上一行输出一模一样")
print(f"    len(pad)={len(pad)}，去掉「北京」还剩 {len(pad) - 2} 个空格")

# 「看得见空隙」为什么还不够：下面三个肉眼几乎一样，实际互不相同。
wider = f"{'北京':<9}"      # 补 7 个
manual = "北京" + "      "  # 手打 6 个，压根没经过格式化
print("    对照 <8  : " + pad + "|")
print("    对照 <9  : " + wider + "|")
print("    手打空格 : " + manual + "|")
print(f"    repr 才分得清: {pad!r} / {wider!r} / {manual!r}")
print(f"    pad==wider? {pad == wider}    pad==manual? {pad == manual}")

# 转义符也会显形 —— 调试「这个字符串结尾是不是多了个 \r」这类问题时靠它。
messy = "含\t制表符和换行\n"
print("    print(messy): " + messy.replace("\n", "⏎") + "  ← 制表符被真的展开了")
print(f"    {{messy!r}}   : {messy!r}  ← \\t \\n 显示成字面量")

# str() 和 repr() 的分工：前者给用户看，后者给程序员看。
# print(x) 内部走 str()，交互式解释器里敲变量名回车走的是 repr()
# —— 这就是为什么 REPL 里看字符串有引号、print 出来没有。
print()
for v in ("3", 3, None, [1, "a"]):
    print(f"    str={str(v):<8} repr={v!r}")
print("    只有字符串两者不同：str 脱掉引号，repr 留着")

# !a 比 !r 更狠，非 ASCII 字符也转成转义序列
print(f"    !r → {'北京'!r}      !a → {'北京'!a}")

# 顺序不能反：转换标志在冒号「前」，格式说明符在冒号「后」。
print(f"    {'ab'!r:>10}|  ← !r 先转成 'ab'（4 个字符），再按 >10 右对齐")
try:
    "{:>10!r}".format("ab")
except ValueError as e:
    print(f"    {'{:>10!r}':<10} → ValueError: {e}")

# ── ④-7 那 !r 和 repr() 到底差在哪 ────────────────────────────────
# f-string 能内联任意表达式，所以两种写法在 f-string 里撞了车、看不出区别。
# 但 !r 是「模板语法」，repr() 是「函数调用」—— 一旦离开 f-string，
# str.format / logging 的 {} 模板里不求值表达式，!r 就成了唯一选择。
print()
print("  ④-7 唯一的真区别：能写在哪儿")

x = "北京  "
print(f"    f-string 里      : {f'{x!r}' == f'{repr(x)}'}  ← 两种写法输出相等")
print('    模板里 {!r}      : ' + "{!r}".format(x))
try:
    "{repr(x)}".format(x=x)
except KeyError as e:
    print(f"    模板里 {{repr(x)}} : KeyError {e} ← 模板把它当键名，不会调函数")

# 另一个坑（两种写法都会中招）：!r 先把值变成 str，后面的格式说明符就改由
# str 来解释了，原类型自己的格式化能力全丢。
import datetime

d = datetime.date(2026, 9, 12)
print(f"    {'{d:%Y年}':<16} → {d:%Y年}")
for label, value, spec in (("{d!r:%Y年}", d, "%Y年"), ("{3.14159!r:.2f}", 3.14159, ".2f")):
    try:
        format(repr(value), spec)
    except ValueError as e:
        print(f"    {label:<16} → ValueError: {e}")
