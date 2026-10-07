"""字典和列表：取值、真假判断、解包，以及容器知识的补全。

①-④ 每节都标了出处，来自隔壁 langchain 仓库的 chapter1 demo。
⑤-⑧ 是补全线：那些 demo 里没出现过，但写容器代码绕不开的东西，
因此不标出处。

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


# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("⑤ 可变性与共享引用")
print("═" * 62)

# ── ⑤-1 赋值不复制 —— 名字是标签，贴在同一个对象上 ────────────────
print()
print("  ⑤-1 赋值只是多贴一张标签，不是复制")

a = [1, 2, 3]
b = a
b.append(4)
print(f"    a = [1,2,3]; b = a; b.append(4)")
print(f"    a → {a}      ← a 也变了")
print(f"    b → {b}")
print(f"    a is b → {a is b}   ← 从头到尾只有一个列表")

# 不可变类型上看不出这件事 —— 因为根本改不了，只能换一个新的。
s = "abc"
t = s
t += "d"
print(f"    字符串: s='abc'; t=s; t+='d'  → s={s!r} t={t!r}  ← s 没变")
print("    不是字符串「特殊」，是 += 对不可变类型只能造新对象再重贴标签")

# ── ⑤-2 默认参数只在定义时求值一次 ────────────────────────────────
# ⛔ 这是工具函数里最隐蔽的一类 bug：默认值是个可变对象时，所有调用共用它。
print()
print("  ⑤-2 ⛔ def f(x=[]) —— 默认值全体调用共用一个")


def add_tag_bad(tag, tags=[]):
    tags.append(tag)
    return tags


print(f"    第一次 add_tag_bad('a') → {add_tag_bad('a')}")
print(f"    第二次 add_tag_bad('b') → {add_tag_bad('b')}   ← 上一次的还在")
print(f"    第三次 add_tag_bad('c') → {add_tag_bad('c')}")
print(f"    函数身上存着那一个列表: {add_tag_bad.__defaults__}")


def add_tag_ok(tag, tags=None):
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags


print(f"    正确写法 tags=None，进来再造: {add_tag_ok('a')} {add_tag_ok('b')}")

# ── ⑤-3 拷贝分两层：浅拷贝只复制最外面那层 ────────────────────────
print()
print("  ⑤-3 copy 是浅的，deepcopy 才到底")

import copy

orig = {"tools": ["get_weather"], "n": 1}
shallow = copy.copy(orig)      # 等价于 dict(orig) / orig.copy() / {**orig}
deep = copy.deepcopy(orig)
orig["tools"].append("search")
orig["n"] = 99
print(f"    改了 orig 之后：")
print(f"      orig    = {orig}")
print(f"      shallow = {shallow}   ← n 没跟着变，tools 跟着变了")
print(f"      deep    = {deep}   ← 都没变")
print("    浅拷贝复制的是「里面那些标签」，标签指向的对象还是同一批")
print("    list 的 lst[:] / list(lst)、dict 的 {**d} —— 全都是浅拷贝")

# ── ⑤-4 可哈希 —— 为什么 list 不能当 key ─────────────────────────
# 能不能当 dict 的 key / set 的元素，判据是「可哈希」，而可变对象一律不可哈希：
# 它的哈希值会随内容改变,放进去就再也找不回来了。
print()
print("  ⑤-4 可变 ⇒ 不可哈希 ⇒ 当不了 key")

for v in ((1, 2), "abc", frozenset([1]), [1, 2], {"a": 1}, {1, 2}):
    try:
        hash(v)
        print(f"    hash({v!r:<12}) 可以   → 能当 dict 的 key / set 的元素")
    except TypeError as e:
        print(f"    hash({v!r:<12}) TypeError: {e}")

# ── ⑤-5 「不可变」只管最外层 ──────────────────────────────────────
print()
print("  ⑤-5 tuple 不可变，但装在里面的 list 照样能改")

tup = (1, [2, 3])
tup[1].append(4)
print(f"    tup = (1, [2, 3]); tup[1].append(4) → {tup}")
try:
    tup[0] = 9
except TypeError as e:
    print(f"    但 tup[0] = 9 → TypeError: {e}")
try:
    hash(tup)
except TypeError as e:
    print(f"    而且它也不可哈希了: TypeError: {e}")
print("    ⇒ tuple 保证的是「我装着哪几个对象不变」，不是「那些对象本身不变」")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("⑥ set 和 tuple")
print("═" * 62)

# ── ⑥-1 ⛔ 空的 {} 是字典，不是集合 ───────────────────────────────
print()
print("  ⑥-1 写法上唯一的坑：空集合只能用 set()")

print(f"    type({{}})      → {type({}).__name__}    ← 空花括号归字典所有")
print(f"    type(set())    → {type(set()).__name__}     ← 空集合只有这一种写法")
print(f"    type({{1, 2}})   → {type({1, 2}).__name__}     ← 非空时花括号才是集合")

# ── ⑥-2 去重，而且不保序 ──────────────────────────────────────────
print()
print("  ⑥-2 自动去重；顺序不保证，别拿它当列表用")

calls = ["get_weather", "search", "get_weather", "get_weather", "search"]
print(f"    原始调用 {calls}")
print(f"    set(...)  → {set(calls)}   ← 去重了，但顺序不是原来的")
print(f"    要去重又保序: {list(dict.fromkeys(calls))}   ← 借字典保插入序的性质")

# ── ⑥-3 交并差 —— 白名单/黑名单判断 ──────────────────────────────
print()
print("  ⑥-3 交并差：判断模型选的工具在不在白名单里")

allowed = {"get_weather", "search", "calculator"}
used = {"get_weather", "send_email", "search"}
print(f"    白名单 allowed = {sorted(allowed)}")
print(f"    实际用 used    = {sorted(used)}")
print(f"    used - allowed = {used - allowed}       ← 越权的，这就是要报警的")
print(f"    used & allowed = {sorted(used & allowed)}   ← 合法的")
print(f"    used | allowed = {len(used | allowed)} 个（并集）")
print(f"    used <= allowed = {used <= allowed}   ← 是不是全都合法（子集判断）")

# ── ⑥-4 in 的代价：list 是逐个比，set 是算哈希 ───────────────────
# ⚠ 小数据看不出差别；白名单上千条、或者在循环里反复查时，差的是量级。
print()
print("  ⑥-4 in 判断：list 是 O(n)，set 是 O(1)")

import timeit

big_list = list(range(50_000))
big_set = set(big_list)
target = 49_999  # 最坏情况：排在最后
t_list = timeit.timeit(lambda: target in big_list, number=200)
t_set = timeit.timeit(lambda: target in big_set, number=200)
print(f"    在 5 万个元素里查最后一个，单次平均:")
print(f"      list  {t_list / 200 * 1e6:9.2f} µs   ← 从头比到尾")
print(f"      set   {t_set / 200 * 1e6:9.2f} µs   ← 算一次哈希直接落位")
print(f"      相差约 {t_list / t_set:,.0f} 倍（具体倍数随机器和数据量变）")
print("    代价是元素必须可哈希（⑤-4），而且不保序")

# ── ⑥-5 tuple 作为一种类型，而不只是解包的副产品 ─────────────────
print()
print("  ⑥-5 tuple：不可变，所以能当 key")

# 靠的是逗号，不是括号 —— 单元素必须留逗号。
print(f"    x = 1, 2, 3   → {(1, 2, 3)}  括号可省")
print(f"    type((3))     → {type((3)).__name__}     ← 这不是元组，就是整数 3")
print(f"    type((3,))    → {type((3,)).__name__}   ← 单元素必须留逗号")

# 最常见的正当用途：把「一组值」当成字典的 key
cache = {}
cache[("北京", "c")] = "25 度"
cache[("北京", "f")] = "77 度"
print(f"\n    用元组当 key: {cache}")
print(f"    cache[('北京','c')] → {cache[('北京', 'c')]}")
try:
    cache[["北京", "c"]] = "x"
except TypeError as e:
    print(f"    换成 list 当 key → TypeError: {e}")
print("    ⇒ 需要「一组值作为一个整体被索引」时，tuple 是唯一现成的选择")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("⑦ dict 和 list 的日常操作")
print("═" * 62)

# ── ⑦-1 in —— 字典查的是 key，不是 value ─────────────────────────
print()
print("  ⑦-1 in：比 .get() 更直接的「有没有」")

_val = ORDERS["A123"]   # ① 那份数据，复用
print(f"    'A123' in ORDERS          → {'A123' in ORDERS}    ← 字典的 in 查的是 key")
print(f"    'C789' in ORDERS          → {'C789' in ORDERS}")
try:
    _val in ORDERS
except TypeError as e:
    # 不是返回 False —— in 要先算哈希，而 dict 不可哈希（见 ⑤-4）。
    print(f"    ORDERS['A123'] in ORDERS          → TypeError: {e}")
print(f"    ORDERS['A123'] in ORDERS.values() → {_val in ORDERS.values()}    ← 查 value 要走 .values()")
print("    ⚠ 列表的 in 是逐个比（O(n)），字典/集合的 in 是算哈希（O(1)）—— 见 ⑥-4")

# ── ⑦-2 setdefault —— 没有就放一个进去，然后把它返回 ─────────────
print()
print("  ⑦-2 setdefault：'取不到就先建一个' 的一步写法")

raw_calls = [("get_weather", "北京"), ("search", "天气"), ("get_weather", "上海")]
by_tool = {}
for _name, _arg in raw_calls:
    by_tool.setdefault(_name, []).append(_arg)
print(f"    按工具名分组: {by_tool}")
print("    等价于：if k not in d: d[k] = []  然后 d[k].append(...)")
print("    ⚠ 和 .get(k, []) 不一样：.get 只是返回，不会把这个 [] 放进字典")
probe = {}
probe.get("x", []).append(1)
print(f"    probe.get('x', []).append(1) 之后 probe = {probe}   ← 什么都没留下")
print("    key 很多时改用 collections.defaultdict（见 demo08）")

# ── ⑦-3 合并字典：update 原地改，| 造新的 ───────────────────────
print()
print("  ⑦-3 合并：update 是原地，| 返回新字典（3.9+）")

base = {"model": "opus", "temp": 0}
override = {"temp": 1, "stream": True}
merged = base | override
print(f"    base | override → {merged}   ← 右边覆盖左边，base 没动")
print(f"    base 还是        {base}")
copied = dict(base)
copied.update(override)
print(f"    update 版        {copied}   ← 原地改，返回 None（别去接它）")

# ── ⑦-4 keys/values/items 是「视图」，会跟着字典变 ───────────────
print()
print("  ⑦-4 视图不是快照")

d = {"a": 1}
ks = d.keys()
d["b"] = 2
print(f"    ks = d.keys() 之后又加了 b → ks = {ks}   ← 跟着变了")
print(f"    要快照就转成列表: {list(d.keys())}")
print("    ⛔ 别在 for k in d: 里面增删 key —— RuntimeError，改成 for k in list(d):")
try:
    for k in d:
        d[k + "!"] = 1
except RuntimeError as e:
    print(f"       实测: RuntimeError: {e}")

# ── ⑦-5 sorted 造新列表，.sort() 原地改并返回 None ───────────────
print()
print("  ⑦-5 sorted vs .sort() —— 可变类型方法的通病")

nums = [3, 1, 2]
print(f"    sorted(nums) → {sorted(nums)}   nums 仍是 {nums}")
print(f"    nums.sort()  返回 {nums.sort()}   nums 变成 {nums}   ← 返回 None")
print("    ⛔ lst = lst.sort() 会把 lst 变成 None。str 那边正好相反（见 strings 系列）")
tools = [{"name": "search", "n": 5}, {"name": "get_weather", "n": 9}]
print(f"    按字段排序: {[t['name'] for t in sorted(tools, key=lambda t: -t['n'])]}   ← key= 指定排序依据")

# ── ⑦-6 切片 —— 列表和字符串同一套语法 ───────────────────────────
print()
print("  ⑦-6 切片 [起:止:步]，止不含")

lst = [0, 1, 2, 3, 4, 5]
for expr, val in (("lst[1:4]", lst[1:4]), ("lst[:3]", lst[:3]), ("lst[3:]", lst[3:]),
                  ("lst[-2:]", lst[-2:]), ("lst[::2]", lst[::2]), ("lst[::-1]", lst[::-1])):
    print(f"    {expr:<10} → {val}")
print(f"    lst[:] 是浅拷贝（见 ⑤-3）: {lst[:] is lst}   ← 新列表，但元素还是同一批")

# ── ⑦-7 推导式不止列表一种 ───────────────────────────────────────
print()
print("  ⑦-7 换个括号就是另一种推导式")

names = ["get_weather", "search", "get_weather"]
_list = [n.upper() for n in names]
_set = {n for n in names}
_dict = {n: len(n) for n in names}
_gen = (n for n in names)
print(f"    列表   [n.upper() for n in names]  → {_list}")
print(f"    集合   {{n for n in names}}          → {_set}   ← 自动去重")
print(f"    字典   {{n: len(n) for n in names}}  → {_dict}")
print(f"    生成器 (n for n in names)          → {type(_gen).__name__}，懒执行，不占内存")
print("    ⚠ {} 里写 k: v 是字典推导式，只写 n 是集合推导式 —— 靠冒号区分")

# ══════════════════════════════════════════════════════════════════════
# ⚠ 本仓库根目录下的 collections/ 目录和标准库模块同名。现在没事（目录里没有
# __init__.py，命名空间包的优先级低于真模块），但**千万别往那个目录里放
# __init__.py** —— 那一刻起 import collections 就会拿到那个目录，而 os、
# typing、dataclasses 内部都在 import collections。
from collections import Counter, defaultdict, deque, namedtuple

print()
print("═" * 62)
print("⑧ collections 模块")
print("═" * 62)

CALLS = ["get_weather", "search", "get_weather", "get_weather", "search", "calculator"]

# ── ⑧-1 Counter —— 计数和排行 ─────────────────────────────────────
print()
print("  ⑧-1 Counter：数一数各调用了几次")

c = Counter(CALLS)
print(f"    Counter(CALLS)      → {dict(c)}")
print(f"    c['get_weather']    → {c['get_weather']}")
print(f"    c['没调过的']        → {c['没调过的']}   ← 不存在返回 0，不是 KeyError")
print(f"    c.most_common(2)    → {c.most_common(2)}   ← 直接给排行")
print(f"    sum(c.values())     → {sum(c.values())}   ← 总调用次数")
print("    手写等价：d = {}; for n in CALLS: d[n] = d.get(n, 0) + 1")

# Counter 之间能加减 —— 比较两次运行的差异
before = Counter(["get_weather", "search"])
after = Counter(["get_weather", "get_weather", "send_email"])
print(f"    after - before      → {dict(after - before)}   ← 只留正数，负的丢掉")

# ── ⑧-2 defaultdict —— 取不到 key 自动造一个 ─────────────────────
# ⑦-2 的 setdefault 每次都要写一遍那个 []，key 多了就啰嗦。
print()
print("  ⑧-2 defaultdict：把 setdefault 那个 [] 提到定义处")

raw = [("get_weather", "北京"), ("search", "天气"), ("get_weather", "上海")]
by_tool = defaultdict(list)
for name, arg in raw:
    by_tool[name].append(arg)       # 不用先判断 key 在不在
print(f"    defaultdict(list) → {dict(by_tool)}")

counts = defaultdict(int)
for name in CALLS:
    counts[name] += 1               # int() 是 0，所以能直接 +=
print(f"    defaultdict(int)  → {dict(counts)}")
print("    ⚠ 它是「读一下就会建 key」：读 d['不存在'] 之后这个 key 就真的在里面了")
probe = defaultdict(list)
probe["x"]
print(f"       probe['x'] 读一下 → probe = {dict(probe)}   ← 只想查在不在，用 in")

# ── ⑧-3 namedtuple —— 能按名字取的 tuple ─────────────────────────
print()
print("  ⑧-3 namedtuple：tuple[2] 看不出是什么，.n 看得出")

Call = namedtuple("Call", "name args ms")
call = Call("get_weather", {"city": "北京"}, 42)
print(f"    call          → {call}")
print(f"    call.name     → {call.name}      ← 比 call[0] 有意义")
print(f"    call[0]       → {call[0]}      ← 位置访问照样能用，它就是个 tuple")
print(f"    isinstance(call, tuple) → {isinstance(call, tuple)}")
print(f"    call._asdict()→ {dict(call._asdict())}")
print(f"    改一个字段    → {call._replace(ms=99)}   ← 不可变，_replace 返回新的")
print("    比 dict 省内存、能解包；比 class 少写一堆样板")
# ⚠ 「能当 key」要看字段：上面这个 Call 装着一个 dict，照 ⑤-5 就不可哈希。
try:
    hash(call)
except TypeError as e:
    print(f"    hash(call) → TypeError: {e}")
print(f"    hash(Call('search', (), 1)) → 字段全可哈希时才行: {hash(Call('search', (), 1)) != 0}")

# ── ⑧-4 deque(maxlen=) —— 只保留最近 N 条 ───────────────────────
# 对话历史、滑动窗口这类「超出就丢掉最老的」，用它比每次切片省事。
print()
print("  ⑧-4 deque：两头都是 O(1)，maxlen 满了自动挤掉最老的")

history = deque(maxlen=3)
for turn in ("第1轮", "第2轮", "第3轮", "第4轮", "第5轮"):
    history.append(turn)
    print(f"    append({turn}) → {list(history)}")
print(f"    popleft()      → {history.popleft()}，剩 {list(history)}")
print("    ⚠ list.pop(0) 要把后面所有元素前移（O(n)），deque.popleft() 是 O(1)")
print("    ⚠ 但 deque 不支持切片：d[1:3] 会 TypeError")
try:
    history[0:2]
except TypeError as e:
    print(f"       实测: TypeError: {e}")
