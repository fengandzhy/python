"""类与对象：实例化、属性访问、装饰器。

    python3 04_objects.py          # 或 uv run python 04_objects.py
"""

# ══════════════════════════════════════════════════════════════════════
print("═" * 62)
print("① 类 vs 实例 —— 括号的意义")
print("═" * 62)
# 出处：checkpointer=MemorySaver()  ← 那对括号不能少


class Box:
    """一个储物箱。"""

    def __init__(self):
        self.items = []          # 每个实例有自己的 items

    def put(self, x):
        self.items.append(x)


print(f"  Box     = {Box}")
print(f"            ↑ 一个【类】，相当于图纸")
print(f"  Box()   = {Box()}")
print(f"            ↑ 一个【实例】，按图纸造出来的实物")

# 每次实例化都是独立的对象
a, b = Box(), Box()
a.put("给A的")
print(f"\n  a, b = Box(), Box()")
print(f"    a is b   = {a is b}      ← 两个独立的对象")
print(f"    a.items  = {a.items}")
print(f"    b.items  = {b.items}       ← b 不受影响")
print()
print("  出处：checkpointer=MemorySaver() 必须加括号，因为要的是【实例】")
print("    （能往里存东西的实物），不是类本身。")
print("    而且两次 MemorySaver() 是两个独立的储物间 —— 所以要写在")
print("    create_agent() 里，保证整个 agent 用同一个。")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("② 属性访问：. 和 getattr()")
print("═" * 62)
# 出处：03_parallel_tools.py 的 getattr(msg, "tool_calls", None)


class AIMsg:
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls


class ToolMsg:
    def __init__(self, content):
        self.content = content
        # 注意：没有 tool_calls 这个属性


ai = AIMsg("好的", tool_calls=[{"name": "get_weather"}])
tm = ToolMsg("北京晴 25 度")

print(f"  ai.tool_calls = {ai.tool_calls}")
try:
    tm.tool_calls
except AttributeError as e:
    print(f"  tm.tool_calls → AttributeError: {e}")

print()
print("  getattr(对象, '属性名', 默认值) —— 拿不到就给默认值，不报错：")
print(f"    getattr(ai, 'tool_calls', None) = {getattr(ai, 'tool_calls', None)}")
print(f"    getattr(tm, 'tool_calls', None) = {getattr(tm, 'tool_calls', None)}")
print()
print("  这就是 demos 里为什么写 getattr(msg, 'tool_calls', None) 而不是")
print("  msg.tool_calls —— 消息列表里混着 AIMessage 和 ToolMessage，")
print("  后者没有这个属性，直接点会崩。")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("③ 判断类型")
print("═" * 62)
# 出处：03_parallel_tools.py 用 type(msg).__name__ == "ToolMessage"
#      02_chained_tools_memory.py 用 msg.type == "tool"

for m in [ai, tm]:
    print(f"  {type(m)}")
    print(f"    type(m).__name__ = {type(m).__name__!r}")
    print(f"    isinstance(m, AIMsg) = {isinstance(m, AIMsg)}")

print()
print("  三种写法各有场合：")
print("    isinstance(m, AIMessage)          最标准，但要 import 那个类")
print("    type(m).__name__ == 'ToolMessage'  不用 import，字符串比较（demos 用的）")
print("    m.type == 'tool'                   langchain 消息对象自带的字段")

# ══════════════════════════════════════════════════════════════════════
print()
print("═" * 62)
print("④ 装饰器 @ —— 用一个函数改造另一个函数")
print("═" * 62)
# 出处：@tool


def shout(fn):
    """一个装饰器：把返回值改成大写并加感叹号。"""
    def wrapped(*args, **kwargs):
        return fn(*args, **kwargs).upper() + "!"
    return wrapped


@shout
def hello(name):
    return f"hello {name}"


print(f"  @shout 装饰后: hello('bob') = {hello('bob')!r}")
print()
print("  @shout 只是语法糖，等价于：")
print("    def hello(name): ...")
print("    hello = shout(hello)      ← 用装饰器的返回值【替换】原函数")

# 装饰器可以把函数换成完全不同的东西
print()
print("  装饰器甚至能把函数换成一个【对象】—— @tool 就是这么干的：")


class FakeTool:
    def __init__(self, fn):
        self.name = fn.__name__
        self.description = fn.__doc__
        self._fn = fn

    def invoke(self, args: dict):
        return self._fn(**args)


def faketool(fn):
    return FakeTool(fn)


@faketool
def get_weather(city: str) -> str:
    """获取指定城市的实时天气状况和气温。"""
    return f"{city} 晴 25°C"


print(f"    type(get_weather)        = {type(get_weather).__name__}   ← 不再是函数了")
print(f"    get_weather.name         = {get_weather.name!r}")
print(f"    get_weather.description  = {get_weather.description!r}")
try:
    get_weather("北京")
except TypeError as e:
    print(f"    get_weather('北京')      → TypeError: {e}")
print(f"    get_weather.invoke({{'city': '北京'}}) = {get_weather.invoke({'city': '北京'})!r}")
print()
print("  真的 @tool 做的事一模一样：读函数名、docstring、类型注解，")
print("  生成 JSON Schema，把函数换成 StructuredTool 对象。")
print("  所以 @tool 之后不能再 get_weather('北京')，必须 .invoke({'city': '北京'})。")
