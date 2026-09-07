"""迭代：for、生成器、模块与导入。

    python3 05_iteration.py          # 或 uv run python 05_iteration.py
"""

import time

# ══════════════════════════════════════════════════════════════════════
print("═" * 62)
print("① 生成器 vs 列表 —— 懒执行")
print("═" * 62)
# 出处：agent.stream(...) 返回生成器；agent.get_state_history() 也是


def make_list():
    """一次性算完，全部塞进内存。"""
    print("    [列表] 开始算…")
    out = []
    for i in range(3):
        time.sleep(0.2)
        out.append(f"第{i}项")
    print("    [列表] 全部算完了，才返回")
    return out


def make_gen():
    """yield 一个就交出去一个，用的时候才算下一个。"""
    for i in range(3):
        time.sleep(0.2)
        print(f"    [生成器] 现在才算第{i}项")
        yield f"第{i}项"


t0 = time.time()
lst = make_list()
print(f"  make_list() 返回后已过 {time.time() - t0:.1f}s，返回 {type(lst).__name__}")

print()
t0 = time.time()
gen = make_gen()
print(f"  make_gen() 返回后已过 {time.time() - t0:.1f}s，返回 {type(gen).__name__}")
print("    ↑ 瞬间返回！函数体一行都还没跑")
print("  开始 for 循环：")
for item in gen:
    print(f"      拿到 {item}（已过 {time.time() - t0:.1f}s）")

print()
print("  这解释了 agent.stream() 的行为：")
print("    · stream() 瞬间返回，一次 HTTP 请求都没发")
print("    · 第一次迭代才真正开始跑图、发请求")
print("    · 循环体和图的执行是【交替】的，不是「先全跑完再打印」")
print()
print("  生成器只能遍历一次：")
print(f"    再 for 一遍 gen: {list(gen)}   ← 空的，已经耗尽")
print("    所以 list(agent.get_state_history(cfg)) 里的 list() 是把它一次性展开。")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("② for 循环里的解包")
print("═" * 62)
# 出处：for node, update in chunk.items()

chunk = {"model": {"messages": ["AIMessage"]}}

print(f"  chunk = {chunk}")
print()
print("  写法1（不解包）：")
for key in chunk:
    print(f"    key={key!r}  value={chunk[key]}")

print("  写法2（解包，demos 用的）：")
for node, update in chunk.items():
    print(f"    node={node!r}  update={update}")
print("    ← .items() 每次产出一个 (key, value) 元组，就地拆成两个名字")

print()
print("  enumerate 也是同一个套路：")
for i, name in enumerate(["a", "b", "c"], start=1):
    print(f"    i={i}  name={name!r}")
print()
print("  ─── 解包只认【位置】，不认类型 ───────────────────────")
print("  for fn, label in [...] 里，Python 只保证「数量对得上就拆」，")
print("  左边到底该是函数还是字符串，是你自己的约定，它不检查。")


def f1():
    "单引号也算"


# ── ①个数不对 → 立刻 ValueError，最容易发现 ─────────────────────
print()
print("  ① 元组个数不对 → 立刻 ValueError（还没用就炸）")

for bad in [[(f1, "多一个", "溢出")], [(f1,)]]:
    try:
        for fn, label in bad:
            pass
    except ValueError as e:
        print(f"      {bad[0]!r:34} → ValueError: {e}")

# ── ②左右写反、类型不兼容 → 用到那一刻才 TypeError ───────────────
print()
print("  ② 左右写反，用的时候类型不兼容 → TypeError（解包本身不报错）")

for fn, label in [("不在第一行", f1)]:            # 反了：fn 是字符串，label 是函数
    print(f"      解包成功: fn={fn!r}  label={label.__name__}  ← Python 一声不吭")
    try:
        print(f"      {label:14} __doc__ = {fn.__doc__!r}")
    except TypeError as e:
        print(f"      用的时候才炸 → TypeError: {e}")
        print("      （{label:14} 想给函数补空格补到 14 位，函数不支持格式化）")

# ── ③左右写反、类型碰巧都能用 → 不报错，静默输出错东西 ────────────
print()
print("  ③ 左右写反，类型碰巧都能用 → 不报错，静默输出垃圾（最坑）")

for fn, label in [("单引号", "单引号也算")]:       # 两个都是字符串
    got = fn.__doc__
    print(f"      {label:14} __doc__ = {got[:38]!r}…")
    print("      ↑ 没有任何报错。因为字符串也有 .__doc__（继承自 str 类），")
    print("        读到的是 str 这个类的官方文档，不是你想要的东西。")

# ── ④三个元组类型各不一样 → 完全合法 ───────────────────────────
print()
print("  ④ 每个元组类型各不相同 → 完全合法，Python 不管")

for a, b in [(f1, "字符串"), (123, [1, 2]), ({"k": 1}, None)]:
    print(f"      a={a!r:26} b={b!r}")
print("      数量对得上就行，类型爱是什么是什么。")

# ── 想让 Python 帮你把关 ──────────────────────────────────────
print()
print("  ─── 想让写反了能被发现，两个办法 ───────────────────────")

# 办法1：用字典，靠 key 取值而不是靠位置
print("  办法1 用字典（靠名字取，写反了立刻看得出）：")
for case in [{"fn": f1, "label": "单引号"}]:
    print(f"      {case['label']:14} __doc__ = {case['fn'].__doc__!r}")

# 办法2：用 NamedTuple，既有名字又有类型标注，IDE 会画红线
from typing import Callable, NamedTuple


class Case(NamedTuple):
    fn: Callable
    label: str


print("  办法2 用 NamedTuple（带类型标注，IDE / mypy 会提前报）：")
for c in [Case(f1, "单引号")]:
    print(f"      {c.label:14} __doc__ = {c.fn.__doc__!r}")

print()
print("  根源：Python 是运行时才检查类型的。")
print("  「我以为它是 X」和「它运行时真是 X」之间那道缝，就是 bug 的主要来源")
print("  —— 跟 01_strings.py 里 __doc__ 是 None 却拿去切片，是同一类问题。")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("③ 模块与导入 —— 为什么 demos 必须用 -m")
print("═" * 62)

import sys
from pathlib import Path

print("  「模块」= 一个 .py 文件。import 时 Python 去 sys.path 里找。")
print()
print("  当前 sys.path 的前几项：")
for p in sys.path[:4]:
    print(f"    {p!r}")

print()
print("  关键区别：")
print("    uv run python -m demos.chapter1.01_single_tool")
print("      → 把【当前目录】放进 sys.path → 找得到根目录的 llm.py  ✓")
print()
print("    uv run demos/chapter1/01_single_tool.py")
print("      → 只把【那个文件所在目录】放进 sys.path → 找不到 llm.py  ✗")
print("      → ModuleNotFoundError: No module named 'llm'")
print()
print("  （PyCharm 里没这问题：它的 Add content roots to PYTHONPATH 开着，")
print("    等价于把项目根目录加进去了。）")

# ── import 时会执行整个模块 ────────────────────────────────────────────
print()
print("  ⚠ import 一个模块会【执行】它的全部顶层代码：")
print("    · llm.py 顶层有 load_dotenv() → 所以 from llm import get_llm 顺带读了 .env")
print("    · demos 里的代码也都在顶层 → import 它们会真的发出 API 请求")
print()
print("  防止被 import 时执行，用这个惯用法：")
print("      if __name__ == '__main__':")
print("          main()")
print(f"\n  本文件的 __name__ = {__name__!r}")
print("    直接跑时是 '__main__'；被 import 时是模块名 'python_basics.05_iteration'")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("④ 数字开头的文件名")
print("═" * 62)

print("  demos 和本目录的文件都是 01_ 02_ 开头，这有个细节：")
print()
print("    uv run python -m demos.chapter1.01_single_tool     ✓ 可以")
print("      （-m 走 importlib，接受任意字符串）")
print()
print("    import demos.chapter1.01_single_tool               ✗ SyntaxError")
print("      （import 语句要求合法标识符，不能数字开头）")
print()
print("  所以数字前缀只适合【独立脚本】。要做成能被别人 import 的模块，")
print("  文件名就得是合法标识符（字母或下划线开头）。")
print(f"\n  比如 llm.py 就没有数字前缀 —— 因为所有 demo 都要 import 它。")
