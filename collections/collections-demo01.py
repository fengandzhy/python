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