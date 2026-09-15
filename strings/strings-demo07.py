"""类型码与动态宽度：同一个精度在不同类型上的含义，以及按数据算列宽。

    python3 strings/strings-demo07.py

拆自 01_strings.py 的第 ④ 节；格式说明符的语法见 strings-demo05.py。
"""

#==============================================
print()
print("  ④-4 精度按值的类型解释")

long_rows = [("北京", 25, 690), ("Amsterdam-Zuid", 26, 803), ("广州", 30, 953)]
print(f"    字符串  {'abcdef':.3}                 ← 最多取 3 个字符")
print(f"    .2f    {3.14159:.2f}                   ← 保留 2 位小数")
print(f"    .3g    {31415.9:.3g}              ← 保留 3 位有效数字")
print(f"    ,      {1234567:,}              ← 千分位")
print(f"    .1%    {0.856:.1%}                   ← 先乘 100 再加百分号")
try:
    "{:.2d}".format(123)
except ValueError as e:
    print(f"    .2d    ValueError: {e}  ← 整数不接受精度")

# 数字永远不会被砍位（砍了值就错了），所以宽度对数字列只是「排版建议」：
print(f"    {123456789:>6.2f}  ← 宽度 6 也拦不住，照样溢出")

# 各段可以组合，顺序是 对齐 宽度 , .精度 类型 —— 财务报表那种列就这么排：
print(f"    {1234.5:>12,.2f}  ← >12,.2f")

# 宽度本身也能用 {} 动态填：先按实际数据算出最大宽度，表格就永远不会歪。
w = max(len(c) for c, _, _ in long_rows)
print()
print(f"  ④-5 动态宽度（按数据算出 w={w}）")
for c, t, tok in long_rows:
    print(f"  {c:<{w}}{t:>6}{tok:>10}")