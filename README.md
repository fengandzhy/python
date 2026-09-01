# python

Python 语法速查，**只收录在实际项目里撞到过的**。

来源是隔壁 [fengandzhy/langchain](https://github.com/fengandzhy/langchain) 那个
LangChain 学习项目 —— 每条语法都标了「它在哪行代码里出现过」。所以文件里出现的
`01_single_tool.py`、`llm.py`、`@tool`、`create_agent` 之类，指的都是那个仓库里的
文件，不是本仓库的。

不是通用教程 —— 通用教程网上很多，这里的价值在于「你见过这行代码，这是它的原理」。

## 跑法

```bash
python3 01_strings.py
python3 02_collections.py
python3 03_functions.py
python3 04_objects.py
python3 05_iteration.py
```

**纯标准库，不联网、不装依赖、不花钱。** 兼容 Python 3.9+（用 macOS 自带的
`/usr/bin/python3` 就能跑）。可以随便改随便跑。

## 索引

| 文件 | 内容 | 出处（langchain 仓库）|
|---|---|---|
| **01_strings** | f-string `f"{x}"` | `01_single_tool.py` 的 `return f"{city} 今天…"` |
| | 切片 `[:40]` | 各 demo 里截断模型长回答 |
| | 注释 vs docstring | `@tool` 的 docstring 会发给模型，`#` 不会 |
| | 格式说明符 `{x:<12}` | `06_memory_scope.py` 的对齐输出 |
| **02_collections** | 字典 `o["shipped"]`、`.get()` | `04_tool_misselection.py` 的 `ORDERS` |
| | 真假判断 `if o["shipped"]:` | 同上的三个前提检查 |
| | 解包 `ans, _, _ = ask()` | `06_memory_scope.py` |
| | 列表推导式 | `03_parallel_tools.py` 收集 `tool_calls` 的名字 |
| **03_functions** | 位置参数 / 关键字参数 | |
| | 默认值决定「必填还是可选」 | `@tool` 靠这个生成 schema 的 `required` |
| | `*args` / `**kwargs` | `07_context_budget.py` 的 `run()`、`llm.py` 的 `get_llm()` |
| | 类型注解 | `def get_weather(city: str) -> str` |
| **04_objects** | 类 vs 实例（括号的意义） | `checkpointer=MemorySaver()` |
| | `getattr(obj, name, 默认值)` | `getattr(msg, "tool_calls", None)` |
| | 判断类型的三种写法 | demos 里三种都用过 |
| | 装饰器 `@` | `@tool` 的原理（文件里手写了一个简化版） |
| **05_iteration** | 生成器 vs 列表 | `agent.stream()`、`get_state_history()` |
| | `for k, v in d.items()` | `for node, update in chunk.items()` |
| | 模块与 `sys.path` | 为什么那些 demo 必须用 `-m` |
| | `if __name__ == '__main__':` | import 会执行整个模块 |

## 这里记下的几个坑

都是实际踩到的：

- **空 docstring** `""""""` 等于没写 —— `bool('')` 是 `False`，`@tool` 会 `ValueError`
- **f-string 不能当 docstring** —— 它是运行时表达式，不是字面量
- **可变对象当默认值** `def f(box=[])` —— 那个 `[]` 只创建一次，会被复用
- **类型注解运行时不检查** —— 标了 `-> str` 却返回 `None` 也不报错
- **`getattr` 而不是直接点属性** —— 消息列表里混着有/没有 `tool_calls` 的对象
- **生成器只能遍历一次** —— 所以 `get_state_history()` 要 `list()` 展开
- **数字开头的文件名** —— `-m` 能跑，`import` 语句不行
- **f-string 里嵌套反斜杠** 是 Python 3.12+ 才允许的 —— 为了兼容 3.9，本仓库
  避开了这种写法（把表达式提取到变量里）
