print("═" * 62)
print("① f-string —— 前面加 f，大括号里的表达式会被求值")
print("═" * 62)

city = "北京"
temp = 25

print("  普通字符串:", "{city} 今天 {temp} 度")      # 大括号原样输出
print("  f-string:  ", f"{city} 今天 {temp} 度")     # 被替换

# 大括号里能放任何【表达式】，不只是变量名
print("  运算:      ", f"{temp * 2}")
print("  函数调用:  ", f"{len(city)}")
print("  方法链:    ", f"{city.upper()}")
print("  条件:      ", f"{'热' if temp > 30 else '舒适'}")

# 大括号本身是「插槽」语法，不是表达式。想输出真正的大括号要写两个
print("  字面大括号:", f'{{"city": "{city}"}}')