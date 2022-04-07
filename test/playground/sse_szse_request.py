import random

import requests
from tempfile import TemporaryFile
import pandas as pd

SSE_URL = "http://query.sse.com.cn//sseQuery/commonExcelDd.do"
SSE_PARAMS = {"sqlId": "COMMON_SSE_CP_GPJCTPZ_GPLB_GP_L",
              "type": "inParams",
              "CSRC_CODE": "",
              "STOCK_CODE": "",
              "REG_PROVINCE": "",
              "STOCK_TYPE": 1,
              "COMPANY_STATUS": "2, 4, 5, 7, 8"}
SSE_HEADERS = {"Accept-Encoding": "gzip, deflate",
               "Host": "query.sse.com.cn",
               "Referer": "http://www.sse.com.cn/"}
# http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110&TABKEY=tab1&random=0.8477375686788808
SZSE_URL = "http://www.szse.cn/api/report/ShowReport"
SZSE_PARAMS = {"SHOWTYPE": "xlsx",
               "CATALOGID": "1110",
               "TABKEY": "tab1",
               "random": random.random()}

r = requests.get(SZSE_URL, params=SZSE_PARAMS)
if r.status_code == 200:
    # filename = r.headers["Content-Disposition"].split(";")[1][10:-1]
    # with open(file=filename, mode="wb") as f:
    #     f.write(r.content)
    temp = TemporaryFile()
    temp.write(r.content)
    temp.seek(0)
    df = pd.read_excel(temp)
    print(df)
    temp.close()
