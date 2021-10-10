CREATE TABLE `stockdataset`.`tb_stock_financial_zycwzb` (
  `CODE` VARCHAR(10) NOT NULL,
  `DATE` DATE NULL,
  `JBMGSY_Y` DOUBLE NULL COMMENT '基本每股收益(元)',
  `MGJZC_Y` DOUBLE NULL COMMENT '每股净资产(元)',
  `MGJYHDCSDXJLLJE_Y` DOUBLE NULL COMMENT '每股经营活动产生的现金流量净额(元)',
  `ZYYWSR_WY` DOUBLE NULL COMMENT '主营业务收入(万元)',
  `ZYYWLR_WY` DOUBLE NULL COMMENT '主营业务利润(万元)',
  `YYLR_WY` DOUBLE NULL COMMENT '营业利润(万元)',
  `TZSY_WY` DOUBLE NULL COMMENT '投资收益(万元)',
  `YYWSZJE_WY` DOUBLE NULL COMMENT '营业外收支净额(万元)',
  `LRZE_WY` DOUBLE NULL COMMENT '利润总额(万元)',
  `JLR_WY` DOUBLE NULL COMMENT '净利润(万元)',
  `JLR_KCFJCXSYH_WY` DOUBLE NULL COMMENT '净利润(扣除非经常性损益后)(万元)',
  `JYHDCSDXJLLJE_WY` DOUBLE NULL COMMENT '经营活动产生的现金流量净额(万元)',
  `XJJXJDJWJZJE_WY` DOUBLE NULL COMMENT '现金及现金等价物净增加额(万元)',
  `ZZC_WY` DOUBLE NULL COMMENT '总资产(万元)',
  `LDZC_WY` DOUBLE NULL COMMENT '流动资产(万元)',
  `ZFZ_WY` DOUBLE NULL COMMENT '总负债(万元)',
  `LDFZ_WY` DOUBLE NULL COMMENT '流动负债(万元)',
  `GDQY_WY` DOUBLE NULL COMMENT '股东权益不含少数股东权益(万元)',
  `JZCSYLJQ` DOUBLE NULL COMMENT '净资产收益率加权',
  PRIMARY KEY (`CODE`, `DATE`));


CREATE TABLE `stockdataset`.`tb_stock_financial_ylnl` (
  `CODE` VARCHAR(10) NOT NULL,
  `DATE` DATE NOT NULL,
  `ZZCLRL` DOUBLE NULL COMMENT '总资产利润率',
  `ZYYWLRL` DOUBLE NULL COMMENT '主营业务利润率',
  `ZZCJLRL` DOUBLE NULL COMMENT '总资产净利润率',
  `CBFYLRL` DOUBLE NULL COMMENT '成本费用利润率',
  `YYLRL` DOUBLE NULL COMMENT '营业利润率',
  `ZYYWCBL` DOUBLE NULL COMMENT '主营业务成本率',
  `XSJLL` DOUBLE NULL COMMENT '销售净利率',
  `JZCSYL` DOUBLE NULL COMMENT '净资产收益率',
  `GBBCL` DOUBLE NULL COMMENT '股本报酬率',
  `JZCBCL` DOUBLE NULL COMMENT '净资产报酬率',
  `ZCBCL` DOUBLE NULL COMMENT '资产报酬率',
  `XSMLL` DOUBLE NULL COMMENT '销售毛利率',
  `SXFYBZ` DOUBLE NULL COMMENT '三项费用比重',
  `FZYBZ` DOUBLE NULL COMMENT '非主营比重',
  `ZYLRBZ` DOUBLE NULL COMMENT '主营利润比重',
  PRIMARY KEY (`CODE`, `DATE`));

CREATE TABLE `stockdataset`.`tb_stock_financial_chnl` (
  `CODE` VARCHAR(10) NOT NULL,
  `DATE` DATE NOT NULL,
  `LDBL` DOUBLE NULL COMMENT '流动比率',
  `SDBL` DOUBLE NULL COMMENT '速动比率',
  `XJBL` DOUBLE NULL COMMENT '现金比率',
  `LXZFBS` DOUBLE NULL COMMENT '利息支付倍数',
  `ZCFZL` DOUBLE NULL COMMENT '资产负债率',
  `CQZWYYYZJBL` DOUBLE NULL COMMENT '长期债务与营运资金比率',
  `GDQYBL` DOUBLE NULL COMMENT '股东权益比率',
  `CQFZBL` DOUBLE NULL COMMENT '长期负债比率',
  `GDQYYGDZCBL` DOUBLE NULL COMMENT '股东权益与固定资产比率',
  `FZYSYZQYBL` DOUBLE NULL COMMENT '负债与所有者权益比率',
  `CQZCYCQZJBL` DOUBLE NULL COMMENT '长期资产与长期资金比率',
  `ZBHBL` DOUBLE NULL COMMENT '资本化比率',
  `GDZCJZL` DOUBLE NULL COMMENT '固定资产净值率',
  `ZBGDHBL` DOUBLE NULL COMMENT '资本固定化比率',
  `CQBL` DOUBLE NULL COMMENT '产权比率',
  `QSJZBL` DOUBLE NULL COMMENT '清算价值比率',
  `GDZCBZ` DOUBLE NULL COMMENT '固定资产比重',
  PRIMARY KEY (`CODE`, `DATE`));

CREATE TABLE `stockdataset`.`tb_stock_financial_cznl` (
  `CODE` VARCHAR(10) NOT NULL,
  `DATE` DATE NOT NULL,
  `ZYYWSRZZL` DOUBLE NULL COMMENT '主营业务收入增长率',
  `JLRZZL` DOUBLE NULL COMMENT '净利润增长率',
  `JZCZZL` DOUBLE NULL COMMENT '净资产增长率',
  `ZZCZZL` DOUBLE NULL COMMENT '总资产增长率',
  PRIMARY KEY (`CODE`, `DATE`));


CREATE TABLE `stockdataset`.`tb_stock_financial_yynl` (
  `CODE` VARCHAR(10) NOT NULL,
  `DATE` VARCHAR(45) NOT NULL,
  `YSZKZZL` DOUBLE NULL COMMENT '应收账款周转',
  `YSZKZZTS` DOUBLE NULL COMMENT '应收账款周转天数',
  `CHZZL` DOUBLE NULL COMMENT '存货周转率',
  `GDZCZZL` DOUBLE NULL COMMENT '固定资产周转率',
  `ZZCZZL` DOUBLE NULL COMMENT '总资产周转率',
  `CHZZTS` DOUBLE NULL COMMENT '存货周转天数',
  `ZZCZZTS` DOUBLE NULL COMMENT '总资产周转天数',
  `LDZCZZL` DOUBLE NULL COMMENT '流动资产周转率',
  `LDZCZZTS` DOUBLE NULL COMMENT '流动资产周转天数',
  `JYXJJLLDXSSRBL` DOUBLE NULL COMMENT '经营现金净流量对销售收入比率',
  `ZCDJYXJLLHBL` DOUBLE NULL COMMENT '资产的经营现金流量回报率',
  `JYXJJLLYJLRDBL` DOUBLE NULL COMMENT '经营现金净流量与净利润的比率',
  `JYXJJLLDFZBL` DOUBLE NULL COMMENT '经营现金净流量对负债比率',
  `XJLLBL` DOUBLE NULL COMMENT '现金流量比率',
  PRIMARY KEY (`CODE`, `DATE`));


ALTER TABLE `stockdataset`.`tb_stock_financial_zycwzb`
ADD COLUMN `PERIOD_TYPE` VARCHAR(10) NULL AFTER `JZCSYLJQ`;

ALTER TABLE `stockdataset`.`tb_stock_financial_yynl`
ADD COLUMN `PERIOD_TYPE` VARCHAR(10) NULL AFTER `XJLLBL`;

ALTER TABLE `stockdataset`.`tb_stock_financial_ylnl`
ADD COLUMN `PERIOD_TYPE` VARCHAR(10) NULL AFTER `ZYLRBZ`;

ALTER TABLE `stockdataset`.`tb_stock_financial_cznl`
ADD COLUMN `PERIOD_TYPE` VARCHAR(10) NULL AFTER `ZZCZZL`;

ALTER TABLE `stockdataset`.`tb_stock_financial_chnl`
ADD COLUMN `PERIOD_TYPE` VARCHAR(10) NULL AFTER `GDZCBZ`;

ALTER TABLE `stockdataset`.`tb_stock_financial_zycwzb`
CHANGE COLUMN `PERIOD_TYPE` `PERIOD_TYPE` VARCHAR(10) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`CODE`, `DATE`, `PERIOD_TYPE`);

ALTER TABLE `stockdataset`.`tb_stock_financial_yynl`
CHANGE COLUMN `PERIOD_TYPE` `PERIOD_TYPE` VARCHAR(10) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`CODE`, `DATE`, `PERIOD_TYPE`);

ALTER TABLE `stockdataset`.`tb_stock_financial_ylnl`
CHANGE COLUMN `PERIOD_TYPE` `PERIOD_TYPE` VARCHAR(10) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`CODE`, `DATE`, `PERIOD_TYPE`);

ALTER TABLE `stockdataset`.`tb_stock_financial_cznl`
CHANGE COLUMN `PERIOD_TYPE` `PERIOD_TYPE` VARCHAR(10) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`CODE`, `DATE`, `PERIOD_TYPE`);

ALTER TABLE `stockdataset`.`tb_stock_financial_chnl`
CHANGE COLUMN `PERIOD_TYPE` `PERIOD_TYPE` VARCHAR(10) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`CODE`, `DATE`, `PERIOD_TYPE`);
