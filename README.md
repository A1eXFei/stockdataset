由于新版本的tushare开始需要注册等乱七八糟的东西，使用stockmarket3代码会有很多限制。
因此开发stockdataset来摆脱对tushare的依赖

版本 v0.3.2
完成技术指标遍历，计算和入库

版本 v0.3.1
完成未迁移的技术指标

版本 v0.3
1. 完成部分技术指标计算迁移， 包括MA, BBI, BIAS, BRAR, DMA, MTM, PSY, VR, KDJ, MACD
2. 未迁移的指标BOLL, CCI, ROC, RSI, WR，原因涉及TALIB库

版本 v0.2.3
1. 在从163上获取数据后更新tb_stock_list的last_update_date字段
2. 在保存163数据前增加判断

版本 v0.2.2
database/mysql添加了数据库创建语句

版本 v0.2.1
修正了日志不打印到文件的错误，删除了config下日志配置文件，改用util/app下config_logger()配置

版本 v0.2
从163获取股票的基础数据
1. biz/daily从数据库中获取股票列表和最近更新日期
2. biz/dao/StockBasicDailyDataDaoImpl从163下载数据
3. 开启多进程将数据存入数据库表中

版本 v0.1
新增和更新股票列表
1. 需要从上交所和深交所的网站上下载股票的列表文件。
    - 上交所 http://www.sse.com.cn/assortment/stock/list/share/
    - 深交所 http://www.szse.cn/market/product/stock/list/index.html
2. biz/dao/StockBasicInfoDaoImpl将读取文件内容插入数据库，新的插入，已有股票代码不做修改。
3. 此版本仅插入和更新股票代码、股票名称、上市日期和上一次更新日期（默认1991-01-01， 为日后获取日交易数据使用），有序版本可能使用爬虫获取更多信息。


运行方式：
1. 运行database/mysql下数据库脚本
2. 修改config/database_config.yaml数据库连接信息
3. 修改config/app.yaml里文件路径信息
4. 运行biz/weekly.py更新股票信息
5. 运行biz/daily.py更新个股行情信息