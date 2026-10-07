print()
print("═" * 62)
print("② if 后面直接跟值 —— 判断真假，不用写 == True")
print("═" * 62)
# 出处：04_tool_misselection.py 的 if o["shipped"]: / if not o["paid"]:

ORDERS = {
    "A123": {"paid": True, "shipped": True, "returned": False},
    "B456": {"paid": False, "shipped": False, "returned": False},
}

o = ORDERS["A123"]

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
