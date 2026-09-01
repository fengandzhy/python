"""字典和列表：取值、真假判断、解包。

    python3 02_collections.py          # 或 uv run python 02_collections.py
"""

# ══════════════════════════════════════════════════════════════════════
print("═" * 62)
print("① 字典：[] 按 key 取，不是按位置")
print("═" * 62)
# 出处：demos/chapter1/04_tool_misselection.py 的 ORDERS 和 o["shipped"]

ORDERS = {
    "A123": {"paid": True, "shipped": True, "returned": False},
    "B456": {"paid": False, "shipped": False, "returned": False},
}

o = ORDERS["A123"]                      # 外层：按订单号取
print(f"  ORDERS['A123'] = {o}")
print(f"  它有 {len(o)} 个 key: {list(o.keys())}")
print(f"  o['shipped']   = {o['shipped']}   ← 按 key 取值")

# 对比：列表用【位置】，字典用【名字】。符号一样，含义不同
lst = ["第0个", "第1个", "第2个"]
print(f"\n  列表 lst[1]      = {lst[1]!r}       ← 位置")
print(f"  字典 o['paid']   = {o['paid']}          ← 名字")

# ── [] 和 .get() 的区别 ────────────────────────────────────────────────
print()
print("  [] 和 .get() 的区别：")
print(f"    ORDERS.get('不存在') = {ORDERS.get('不存在')}      ← 返回 None，不报错")
try:
    ORDERS["不存在"]
except KeyError as e:
    print(f"    ORDERS['不存在']     → KeyError: {e}")

print()
print("  什么时候用哪个（04_tool_misselection.py 里两种都用了）：")
print("    .get()  key 可能不存在时（比如 order_id 来自模型，可能是瞎编的）")
print("    []      key 必然存在时（'shipped' 是你自己定义的，不存在=代码 bug，该崩）")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("② if 后面直接跟值 —— 判断真假，不用写 == True")
print("═" * 62)
# 出处：04_tool_misselection.py 的 if o["shipped"]: / if not o["paid"]:

if o["shipped"]:
    print("  if o['shipped']:      → True，进入分支")
if not o["returned"]:
    print("  if not o['returned']: → False 取反变 True，进入分支")

print()
print("  什么算「假」：")
for v in [False, 0, 0.0, "", [], {}, (), None]:
    print(f"    bool({v!r:8}) = {bool(v)}")
print("    → 空的东西和零都是假")
print()
print("  什么算「真」：非空、非零的一切")
for v in [True, 1, -1, "0", " ", [0], {"a": 0}]:
    print(f"    bool({v!r:8}) = {bool(v)}")
print()
print('  注意 "0" 和 " " 是【真】—— 它们是非空字符串。')
print("  这解释了一个我们遇到过的报错：@tool 的 docstring 写成空的 \"\"\"\"\"\"，")
print("  bool('') 是 False，langchain 判定为「没写」→ ValueError。")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("③ 解包 —— 等号左边写几个名字，就拆成几份")
print("═" * 62)
# 出处：06_memory_scope.py 的 ans, _, _ = ask(...)


def ask():
    """返回三个值 —— 实际是返回一个元组。"""
    return "北京晴 25 度", 4, 676


r = ask()
print(f"  r = ask()        → {r!r}")
print(f"  type(r)          → {type(r).__name__}   ← 「返回多个值」= 返回一个元组")

a, b, c = ask()
print(f"  a, b, c = ask()  → a={a!r}  b={b}  c={c}")

# _ 是普通变量名，约定俗成表示「这个我不用」
ans, _, _ = ask()
print(f"  ans, _, _ = ask() → ans={ans!r}")
print(f"                       _ 也真的被赋值了: {_}  ← 它就是个变量，不是特殊语法")

# 数量必须对上
try:
    x, y = ask()
except ValueError as e:
    print(f"  x, y = ask()     → ValueError: {e}")

# * 吞掉剩下的
first, *rest = ask()
print(f"  first, *rest     → first={first!r}  rest={rest}  ← rest 是 list")

# for 循环里的解包（demos 里 for node, update in chunk.items() 就是这个）
print()
print("  for 循环里也能解包：")
d = {"model": "第1步", "tools": "第2步"}
for k, v in d.items():
    print(f"    k={k!r}  v={v!r}     ← .items() 每次给一个二元组，就地拆开")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("④ 列表推导式 —— 一行生成一个列表")
print("═" * 62)
# 出处：03_parallel_tools.py 的 [tc["name"] for tc in msg.tool_calls]

tool_calls = [
    {"name": "get_weather", "args": {"city": "北京"}},
    {"name": "get_air_quality", "args": {"city": "北京"}},
]

names = [tc["name"] for tc in tool_calls]
print(f"  [tc['name'] for tc in tool_calls]  → {names}")

print("\n  等价的普通写法：")
names2 = []
for tc in tool_calls:
    names2.append(tc["name"])
print(f"    {names2}")

# 带条件
print()
nums = [1, 2, 3, 4, 5, 6]
print(f"  带 if 过滤:  [n for n in {nums} if n % 2 == 0]")
print(f"               → {[n for n in nums if n % 2 == 0]}")

# 双层（04_tool_misselection.py 里那个统计工具调用的就是这种）
print()
messages = [
    {"type": "ai", "tool_calls": [{"name": "a"}, {"name": "b"}]},
    {"type": "tool"},
    {"type": "ai", "tool_calls": [{"name": "c"}]},
]
picked = [tc["name"] for m in messages if m.get("tool_calls") for tc in m["tool_calls"]]
print(f"  双层 + 过滤: [tc['name'] for m in messages if m.get('tool_calls') for tc in m['tool_calls']]")
print(f"               → {picked}")
print("    读法：从左到右，和嵌套 for 的顺序一样：")
print("      for m in messages:")
print("          if m.get('tool_calls'):")
print("              for tc in m['tool_calls']:")
print("                  收集 tc['name']")
