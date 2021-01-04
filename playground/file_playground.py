import pandas as pd

sse = pd.read_csv("../sse.xls", delimiter="\t", encoding="gbk")
print(sse)

szse = pd.read_excel("../szse.xlsx")
print(szse)