"""inspect：把函数身上的东西读出来 —— 工具调用那套代码的地基。

    python3 strings/strings-demo08.py

接着 01_strings.py 的 ③-6（getdoc）往下走，自成第 ⑤ 节。
⑤-7 的 eval_str 需要 Python 3.10+；本文件在 3.14 下验过。
"""

#==============================================
import inspect

print()
print("═" * 62)
print("⑤ inspect —— 把函数身上的东西读出来")
print("═" * 62)

# ── ⑤-0 起点：getdoc（③-4 讲过，这里当引子）──────────────────────
print()
print("  ⑤-0 起点 —— getdoc 洗掉公共缩进和首尾空行")


def multi():
    """第一行。

        缩进的第二段
    """
    return 1


print(f"    原始 : {multi.__doc__!r}")
print(f"    洗净 : {inspect.getdoc(multi)!r}")

# ── ⑤-1 signature —— @tool 生成 JSON schema 的原料 ────────────────
# 03_functions.py 用过 parameters["city"].default，那只是其中一列。
# 完整的签名还能分出参数的「种类」，决定它在 schema 里进 required 还是 properties。
print()
print("  ⑤-1 signature —— 参数的种类、标注、默认值")


def get_weather(city: str, unit: str = "c", *tags: str, verbose: bool = False, **extra) -> str:
    """获取天气。"""
    return f"{city} 晴"


sig = inspect.signature(get_weather)
print(f"    整体签名: {sig}")
print(f"    返回标注: {sig.return_annotation}")
for _name, _p in sig.parameters.items():
    # ⛔ 「没有默认值」不能用 `p.default is None` 判断 —— None 本身是个合法默认值。
    # 哨兵是 Parameter.empty，标注缺失同理。
    _d = "(必填)" if _p.default is inspect.Parameter.empty else f"默认={_p.default!r}"
    _a = "(无标注)" if _p.annotation is inspect.Parameter.empty else _p.annotation.__name__
    print(f"    {_name:<8}{_p.kind.description:<23}标注={_a:<7}{_d}")
print("    五种 kind：位置或关键字 / 纯位置(/ 之前) / *args / 纯关键字(* 之后) / **kwargs")

# ── ⑤-2 bind —— 调用之前就知道参数对不对得上 ──────────────────────
# 模型回传的 arguments 是一坨 JSON，直接 fn(**args) 出错时栈很难看。
# 先 bind 一下拿到干净的 TypeError，apply_defaults() 还能把默认值补齐，
# 日志里就能记下「这次实际用的全套参数」。
print()
print("  ⑤-2 bind —— 先对一遍参数，再真的调用")

for _kw in ({"city": "北京"}, {"city": "北京", "unit": "f"}, {"citty": "北京"}, {}):
    try:
        _b = sig.bind(**_kw)
        _b.apply_defaults()
        print(f"    {str(_kw):<30} ✅ {dict(_b.arguments)}")
    except TypeError as e:
        print(f"    {str(_kw):<30} ❌ {e}")

# ── ⑤-3 iscoroutinefunction —— 该走 invoke 还是 ainvoke ───────────
print()
print("  ⑤-3 iscoroutinefunction —— 同步工具和异步工具的分流")


async def search(q: str) -> str:
    """异步工具。"""
    return q


for _fn in (get_weather, search):
    print(f"    {_fn.__name__:<12} 协程函数? {inspect.iscoroutinefunction(_fn)}")
print("    同一个执行器要同时接两种工具时，就靠这个分派")

# ── ⑤-4 getsource —— 把函数自己的源码取回来 ───────────────────────
# ⚠ 只对有源文件的对象有效：REPL 里定义的、内置函数都会抛 OSError。
print()
print("  ⑤-4 getsource —— 连源码带行号")

for _line in inspect.getsource(multi).rstrip().split("\n"):
    print(f"    |{_line}")
print(f"    定义在 {inspect.getsourcefile(multi).split('/')[-1]} 第 {inspect.getsourcelines(multi)[1]} 行")

# ── ⑤-5 getmembers + 谓词 —— 枚举一个类/模块里的东西 ──────────────
# 「把一个模块里所有函数自动注册成工具」这种事就这么写。
print()
print("  ⑤-5 getmembers —— 第二个参数是过滤器")


class Toolbox:
    """一箱工具。"""

    def get_weather(self): ...
    def search(self): ...
    VERSION = 1


print("    isfunction :", [n for n, _ in inspect.getmembers(Toolbox, inspect.isfunction)])
print("    其他常用谓词：isclass / ismodule / ismethod / iscoroutinefunction")

# ── ⑤-6 stack —— 谁调的我 ─────────────────────────────────────────
# ⚠ 别放在热路径上：它要构造整个调用栈的帧对象，很慢。
print()
print("  ⑤-6 stack —— [0] 是自己，[1] 是调用者")


def who_called_me():
    caller = inspect.stack()[1]
    return f"{caller.function}() @ {caller.filename.split('/')[-1]}:{caller.lineno}"


def outer():
    return who_called_me()


print(f"    {outer()}")

# ── ⑤-7 最容易踩的坑：标注是字符串 ────────────────────────────────
# 文件顶上写了 `from __future__ import annotations`，这个文件里**所有**标注
# 都会变成字符串。下面用手写引号的标注制造同样的局面 —— 效果一样，而且
# 不用把整个文件的行为改掉。
#
# ⛔ 危险在于它不报错：任何「读标注生成 schema」的代码会安静地把类型全认不出来。
print()
print("  ⑤-7 标注变成字符串时，读标注的代码会安静地失效")


def quoted(city: "str", unit: "str" = "c") -> "str":
    """标注写成了字符串。"""
    return city


_raw = inspect.signature(quoted).parameters["city"]
print(f"    直接读   : annotation={_raw.annotation!r}  是 str 这个类吗? {_raw.annotation is str}")
_ev = inspect.signature(quoted, eval_str=True).parameters["city"]
print(f"    eval_str : annotation={_ev.annotation!r}  是 str 这个类吗? {_ev.annotation is str}")
print(f"    get_annotations(eval_str=True): {inspect.get_annotations(quoted, eval_str=True)}")
print("    解法：inspect.signature(fn, eval_str=True) 或 inspect.get_annotations(fn, eval_str=True)")
