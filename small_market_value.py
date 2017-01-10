import pandas
import tushare as ts
import re

stRegex = re.compile(r"^[^\*ST.*]")

lc = ts.get_today_all()
lc.to_csv('a.txt',encoding="utf-8")
# lc = pandas.read_csv('a.txt',encoding='utf-8')
lc_amount = lc.query('amount>10000000')
lc_amount_except_ST = lc_amount[(lc_amount['name'].str.contains(stRegex, regex=True))]
res = lc_amount_except_ST.sort_values(by="mktcap").head(5)
# print(res)
print(res[['code','name','changepercent','trade','amount']])