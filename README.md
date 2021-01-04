由于新版本的tushare开始需要注册等乱七八糟的东西，使用stockmarket3代码会有很多限制。
因此开发stockdataset来摆脱对tushare的依赖

版本 v0.1
新增和更新股票列表
1. 需要从上交所和深交所的网站上下载股票的列表文件。
    - 上交所 http://www.sse.com.cn/assortment/stock/list/share/
    - 深交所 http://www.szse.cn/market/product/stock/list/index.html
2. sessions/StockSession将读取文件内容插入数据库，新的插入，已有股票代码不做修改。
3. 此版本仅插入和更新股票代码、股票名称、上市日期和上一次更新日期（默认1991-01-01， 为日后获取日交易数据使用），有序版本可能使用爬虫获取更多信息。

