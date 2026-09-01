"""函数：参数、默认值、*args / **kwargs、类型注解。

    python3 03_functions.py          # 或 uv run python 03_functions.py
"""

# ══════════════════════════════════════════════════════════════════════
print("═" * 62)
print("① 位置参数 vs 关键字参数")
print("═" * 62)


def greet(name, greeting="你好"):
    return f"{greeting}，{name}！"


print(f"  greet('小王')                      → {greet('小王')!r}")
print(f"  greet('小王', '早上好')             → {greet('小王', '早上好')!r}")
print(f"  greet(name='小王', greeting='晚上好') → {greet(name='小王', greeting='晚上好')!r}")
print(f"  greet(greeting='嗨', name='小王')    → {greet(greeting='嗨', name='小王')!r}")
print("    ← 用名字传的话顺序可以乱；用位置传的话必须按顺序")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("② 默认值 —— 决定了参数「必填还是可选」")
print("═" * 62)
# 这一条在 langchain 里有实际后果：
# @tool 生成的 JSON Schema 里，无默认值 → "required"，有默认值 → 可选


def no_default(city):
    return city


def has_default(city="北京"):
    return city


import inspect

for fn, label in [(no_default, "无默认值"), (has_default, "有默认值")]:
    p = inspect.signature(fn).parameters["city"]
    required = p.default is inspect.Parameter.empty
    default_part = "" if required else '="北京"'
    print(f"  def {fn.__name__}(city{default_part}){'':<10} 必填={required}")

print()
print("  出处：@tool 靠这个决定 schema 里的 required。")
print("    def get_weather(city: str)         → \"required\": [\"city\"]")
print("    def get_weather(city: str = '北京') → 无 required，模型可以不传")

# 常见坑：默认值只求值一次
print()
print("  ⚠ 坑：可变对象当默认值")


def bad(item, box=[]):          # ← 这个 [] 只在定义时创建一次！
    box.append(item)
    return box


print(f"    bad('a') → {bad('a')}")
print(f"    bad('b') → {bad('b')}   ← 竟然还有 'a'！同一个列表被复用了")


def good(item, box=None):
    if box is None:
        box = []                # ← 每次调用新建
    box.append(item)
    return box


print(f"    good('a') → {good('a')}")
print(f"    good('b') → {good('b')}   ← 正确")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("③ *args 和 **kwargs —— 收集不定数量的参数")
print("═" * 62)


def show(*args, **kwargs):
    print(f"    args   = {args}        ← 位置参数，打包成【元组】")
    print(f"    kwargs = {kwargs}      ← 关键字参数，打包成【字典】")


print("  show(1, 2, 3, a=4, b=5):")
show(1, 2, 3, a=4, b=5)

print()
print("  星号是语法，后面的名字随你起：")
for fn in [lambda **kw: kw, lambda **选项: 选项]:
    print(f"    {fn(x=1, y=2)}")

# ── 同一个 ** 在两处方向相反 ────────────────────────────────────────────
print()
print("  同一个 ** 在两处方向【相反】：")


def target(model, tools, middleware=None, debug=False):
    parts = [f"model={model}", f"tools={tools}"]
    if middleware:
        parts.append(f"middleware={middleware}")
    if debug:
        parts.append("debug=True")
    return "Agent(" + ", ".join(parts) + ")"


def wrapper(label, **kw):          # ← 定义处：把多余的关键字参数【打包】成 dict
    print(f"    {label}: kw={kw}")
    print(f"       → {target('sonnet', ['天气'], **kw)}")
    #                                            ↑ 调用处：把 dict【拆包】回参数


wrapper("不传")
wrapper("传一个", middleware=["摘要"])
wrapper("传两个", middleware=["摘要"], debug=True)

print()
print("  为什么要这样写（出处：07_context_budget.py 的 run()、llm.py 的 get_llm()）：")
print("    固定的参数写一次，变化的原样透传。")
print("    上面 wrapper 加参数时一个字都没改 —— 这就是 **kw 的用处。")
print()
print("    不用它的话，wrapper 得把 target 的每个参数都抄进自己的签名，")
print("    target 多一个参数你就得改两行（形参一行、传递一行）。")
print("    create_agent 有 16 个参数，全抄一遍显然不现实。")

# 拆包时 key 必须是目标函数认识的
print()
try:
    target("m", ["t"], **{"不存在的参数": 1})
except TypeError as e:
    print(f"  ⚠ 但不是万能通道: TypeError: {e}")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("④ 类型注解 —— 给人和工具看的，运行时【不检查】")
print("═" * 62)
# 出处：demos 里所有 @tool 函数的 def get_weather(city: str) -> str


def typed(city: str, days: int = 1) -> str:
    """有类型注解的函数。"""
    return f"{city} {days} 天"


print(f"  def typed(city: str, days: int = 1) -> str")
print(f"    city: str   参数类型")
print(f"    -> str      返回类型")
print()
print(f"  正常调用:  {typed('北京', 3)!r}")
print(f"  传错类型:  {typed(123, '不是数字')!r}   ← 不报错！Python 不做运行时检查")
print()
print("  那注解有什么用：")
print("    · IDE 补全和报警")
print("    · mypy 之类的静态检查工具")
print("    · 【在 langchain 里有实际作用】@tool 靠它生成 schema 的 type 字段：")
print("        city: str → \"type\": \"string\"")
print("        city: int → \"type\": \"integer\"")
print("      但 -> str 那个返回注解不进 schema —— 实测标了 -> str 却返回 None 也不报错。")
