import pandas as pd
import numpy as np
import datetime
import xlsxwriter


class analyse:
    def __init__(self, file1):
        self.file1 = file1

    def get_data(self):
        data = pd.read_csv(self.file1, encoding='gbk', header=None, names=['订单号', '客户名称',
                                                                           '所属租户', '订单来源',
                                                                           '下单时间', '下单员',
                                                                           '起运站点编码',
                                                                           '起运省', '起运市',
                                                                           '起运区', '起运详细地址',
                                                                           '送货站点编码',
                                                                           '送货省', '送货市', '送货区',
                                                                           '送货详细地址',
                                                                           '承运人'])

        # ----------------------------------------------------------------------------
        # 起运站点编码为空
        No_ConsignorID = data[pd.isna(data["起运站点编码"])].copy()
        # print(No_ConsignorID)

        # 起运站点编码为空，省市区详细地址都不为空
        NoEmpty_ConsignorID = No_ConsignorID[pd.notna(No_ConsignorID["起运省"]) &
                                             pd.notna(No_ConsignorID["起运市"]) &
                                             pd.notna(No_ConsignorID["起运区"]) &
                                             pd.notna(No_ConsignorID["起运详细地址"])].copy()
        # print(NoEmpty_ConsignorID)

        # 起运站点编码为空，省市区详细地址都为空
        Empty_ConsignorID = No_ConsignorID[pd.isna(No_ConsignorID["起运省"]) &
                                           pd.isna(No_ConsignorID["起运市"]) &
                                           pd.isna(No_ConsignorID["起运区"]) &
                                           pd.isna(No_ConsignorID["起运详细地址"])].copy()
        # print(Empty_ConsignorID)

        # 起运站点编码为空，省市区详细地址不全为空
        ConsignorID_1 = No_ConsignorID.append(NoEmpty_ConsignorID)
        ConsignorID_1 = ConsignorID_1.append(Empty_ConsignorID)
        NotAll_Empty_ConsignorID = ConsignorID_1.drop_duplicates(keep=False).copy()
        # print(NotAll_Empty_ConsignorID)

        # ---------------------------------------------------------------------------------
        # 存在起运站点编码
        ConsignorID = data[pd.notna(data["起运站点编码"])].copy()
        # print(ConsignorID)

        # 站点库信息下载后保存到本地，比如叫做（站点库.csv）
        data2 = pd.read_csv('站点库.csv', encoding='gbk', names=['起运站点库', '送货站点库', '起运站点库经度', '起运站点库纬度'])

        list_library = []
        for i in ConsignorID["起运站点编码"].values:
            if i not in data2['起运站点库'].values:
                list_library.append(i)
        # print(list_library)

        # 起运站点编码有但不存在站点库中
        Illegal_ConsignorID = ConsignorID[ConsignorID['起运站点编码'].isin(list_library)].copy()
        # print(Illegal_ConsignorID)

        # 起运站点编码有且存在站点库中
        Legal_ConsignorID = ConsignorID[~ConsignorID['起运站点编码'].isin(list_library)].copy()
        # print(Legal_ConsignorID)

        # 起运站点编码有存在站点库中，省市区详细地址都不为空
        NoEmpty_Legal_ConsignorID = Legal_ConsignorID[pd.notna(Legal_ConsignorID["起运省"]) &
                                                      pd.notna(Legal_ConsignorID["起运市"]) &
                                                      pd.notna(Legal_ConsignorID["起运区"]) &
                                                      pd.notna(Legal_ConsignorID["起运详细地址"])].copy()
        # print(NoEmpty_Legal_ConsignorID)

        # 起运站点编码有存在站点库中，省市区详细地址都为空
        Empty_Legal_ConsignorID = Legal_ConsignorID[pd.isna(Legal_ConsignorID["起运省"]) &
                                                    pd.isna(Legal_ConsignorID["起运市"]) &
                                                    pd.isna(Legal_ConsignorID["起运区"]) &
                                                    pd.isna(Legal_ConsignorID["起运详细地址"])].copy()
        # print(Empty_Legal_ConsignorID)
        # print(Empty_Legal_ConsignorID)
        # 起运站点编码有存在站点库中，省市区详细地址不全为空
        NotAll_Empty_Legal_ConsignorID = Legal_ConsignorID.append(NoEmpty_Legal_ConsignorID)
        NotAll_Empty_Legal_ConsignorID = NotAll_Empty_Legal_ConsignorID.append(Empty_Legal_ConsignorID)
        NotAll_Empty_Legal_ConsignorID = NotAll_Empty_Legal_ConsignorID.drop_duplicates(keep=False).copy()
        # print(NotAll_Empty_Legal_ConsignorID)

        # ---------------------------------------------------------------------------------------
        # 送货站点编码为空
        No_ReceiptID = data[pd.isna(data["送货站点编码"])].copy()
        # print(No_ReceiptID)

        # 送货站点编码为空，省市区详细地址都不为空
        NoEmpty_ReceiptID = No_ReceiptID[pd.notna(No_ReceiptID["送货省"]) &
                                         pd.notna(No_ReceiptID["送货市"]) &
                                         pd.notna(No_ReceiptID["送货区"]) &
                                         pd.notna(No_ReceiptID["送货详细地址"])].copy()
        # print(NoEmpty_ReceiptID)

        # 送货站点编码为空，省市区详细地址都为空
        Empty_ReceiptID = No_ReceiptID[pd.isna(No_ReceiptID["送货省"]) &
                                       pd.isna(No_ReceiptID["送货市"]) &
                                       pd.isna(No_ReceiptID["送货区"]) &
                                       pd.isna(No_ReceiptID["送货详细地址"])].copy()
        # print(Empty_ReceiptID)

        # 送货站点编码为空，省市区详细地址不全为空
        ReceiptID_1 = No_ReceiptID.append(NoEmpty_ReceiptID)
        ReceiptID_1 = ReceiptID_1.append(Empty_ReceiptID)
        NotAll_Empty_ReceiptID = ReceiptID_1.drop_duplicates(keep=False).copy()
        # print(NotAll_Empty_ReceiptID)

        # ---------------------------------------------------------------------------------------
        # 存在送货站点编码
        ReceiptID = data[pd.notna(data["送货站点编码"])].copy()
        # print(ReceiptID)

        # 送货站点库信息下载后保存到本地，比如叫做（站点库.csv）
        data3 = pd.read_csv('站点库.csv', encoding='gbk', names=['起运站点库', '送货站点库', '起运站点库经度', '起运站点库纬度'])

        list_library_2 = []
        for i in ReceiptID["送货站点编码"].values:
            if i not in data3['送货站点库'].values:
                list_library_2.append(i)
        # print(list_library_2)

        # 送货站点编码有但不存在送货站点库中
        Illegal_ReceiptID = ReceiptID[ReceiptID['送货站点编码'].isin(list_library_2)].copy()
        # print(Illegal_ReceiptID)

        # 送货站点编码有且存在送货站点库中
        Legal_ReceiptID = ReceiptID[~ReceiptID['送货站点编码'].isin(list_library_2)].copy()
        # print(Legal_ReceiptID)

        # 送货站点编码有存在站点库中，省市区详细地址都不为空
        NoEmpty_Legal_ReceiptID = Legal_ReceiptID[pd.notna(Legal_ReceiptID["送货省"]) &
                                                  pd.notna(Legal_ReceiptID["送货市"]) &
                                                  pd.notna(Legal_ReceiptID["送货区"]) &
                                                  pd.notna(Legal_ReceiptID["送货详细地址"])].copy()
        # print(NoEmpty_Legal_ReceiptID)

        # 送货站点编码有存在站点库中，省市区详细地址都为空
        Empty_Legal_ReceiptID = Legal_ReceiptID[pd.isna(Legal_ReceiptID["送货省"]) &
                                                pd.isna(Legal_ReceiptID["送货市"]) &
                                                pd.isna(Legal_ReceiptID["送货区"]) &
                                                pd.isna(Legal_ReceiptID["送货详细地址"])].copy()
        # print(Empty_Legal_ReceiptID)

        # 送货站点编码有存在站点库中，省市区详细地址不全为空
        Legal_ReceiptID_1 = Legal_ReceiptID.append(NoEmpty_Legal_ReceiptID)
        Legal_ReceiptID_1 = Legal_ReceiptID_1.append(Empty_Legal_ReceiptID)
        NotAll_Empty_Legal_ReceiptID = Legal_ReceiptID_1.drop_duplicates(keep=False).copy()
        # print(NotAll_Empty_Legal_ReceiptID )

        # ---------------------------------------------------------------------------------------
        # 定义错误类型

        NoEmpty_ConsignorID["异常类型"] = "起运站点编码为空,省市区详细地址都不为空"
        Empty_ConsignorID["异常类型"] = "起运站点编码为空，省市区详细地址都为空"
        NotAll_Empty_ConsignorID["异常类型"] = "起运站点编码为空，省市区详细地址不全为空"
        Illegal_ConsignorID["异常类型"] = "起运站点编码有但不存在站点库中"
        Empty_Legal_ConsignorID["异常类型"] = "起运站点编码有存在站点库中，省市区详细地址都为空"
        NotAll_Empty_Legal_ConsignorID["异常类型"] = "起运站点编码有存在站点库中，省市区详细地址不全为空"
        NoEmpty_Legal_ConsignorID["异常类型"] = "起运站点编码有存在站点库中，省市区详细地址都不为空"

        # 这个需要核对的应该是起运省，起运市，起运区和起运详细地址
        # noempty_p_c_a["异常类型"] = "起运站点与站点库信息不符"

        NoEmpty_ReceiptID["异常类型"] = "送货站点编码为空,省市区详细地址都不为空"
        Empty_ReceiptID["异常类型"] = "送货站点编码为空，省市区详细地址都为空"
        NotAll_Empty_ReceiptID["异常类型"] = "送货站点编码为空，省市区详细地址不全为空"
        Illegal_ReceiptID["异常类型"] = "送货站点编码有但不存在站点库中"
        Empty_Legal_ReceiptID["异常类型"] = "送货站点编码有存在站点库中，省市区详细地址都为空"
        NotAll_Empty_Legal_ReceiptID["异常类型"] = "送货站点编码有存在站点库中，省市区详细地址不全为空"
        NoEmpty_Legal_ReceiptID["异常类型"] = "送货站点编码有存在站点库中，省市区详细地址都不为空"

        # 这个需要核对的应该是起运省，起运市，起运区和起运详细地址
        # noempty_p_c_a["异常类型"] = "送货站点与站点库信息不符"
        # 这个需要核对的应该是起运省，起运市，起运区和起运详细地址
        # noempty_p_c_a["异常类型"] = "起运地址 与 送货地址 相同(都不为空，编码省市区详细地址相同)"

        # -----------------------------------------------------------------------------------------
        # 写入异常订单详情
        NoEmpty_ConsignorID.to_csv('异常订单详情.csv', encoding='gbk')
        Empty_ConsignorID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        NotAll_Empty_ConsignorID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        Illegal_ConsignorID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        Empty_Legal_ConsignorID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        NotAll_Empty_Legal_ConsignorID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        NoEmpty_Legal_ConsignorID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')

        NoEmpty_ReceiptID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        Empty_ReceiptID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        NotAll_Empty_ReceiptID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        Illegal_ReceiptID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        Empty_Legal_ReceiptID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        NotAll_Empty_Legal_ReceiptID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')
        NoEmpty_Legal_ReceiptID.to_csv('异常订单详情.csv', mode='a', header=False, encoding='gbk')

        # -----------------------------------------------------------------------------------------
        # 写入异常订单统计报告

        # 新建文件并写入表头
        lst = ["错误订单类型", "承运商下单", "excel导入", "六和对接", "乳业导入", "WMS下单", "虚拟订单"]
        out_f = open("异常情况汇总报告.csv", 'w', newline='')
        writer = csv.writer(out_f)
        writer.writerow(lst)
        out_f.close()

        # 读取文件，将第一行设置为索引
        data4 = pd.read_csv('异常情况汇总报告.csv', encoding='gbk', header=0)
        ss = ["起运站点编码为空,省市区详细地址都不为空",
              "起运站点编码为空，省市区详细地址都为空",
              "起运站点编码为空，省市区详细地址不全为空",
              "起运站点编码有但不存在站点库中",
              "起运站点编码有存在站点库中，省市区详细地址都为空",
              "起运站点编码有存在站点库中，省市区详细地址不全为空",
              "起运站点编码有存在站点库中，省市区详细地址都不为空",
              "送货站点编码为空,省市区详细地址都不为空",
              "送货站点编码为空，省市区详细地址都为空",
              "送货站点编码为空，省市区详细地址不全为空",
              "送货站点编码有但不存在站点库中",
              "送货站点编码有存在站点库中，省市区详细地址都为空",
              "送货站点编码有存在站点库中，省市区详细地址不全为空",
              "送货站点编码有存在站点库中，省市区详细地址都不为空"]
        dd = [NoEmpty_ConsignorID, Empty_ConsignorID, NotAll_Empty_ConsignorID, Illegal_ConsignorID,
              Empty_Legal_ConsignorID, NotAll_Empty_Legal_ConsignorID, NoEmpty_Legal_ConsignorID,
              NoEmpty_ReceiptID, Empty_ReceiptID, NotAll_Empty_ReceiptID, Illegal_ReceiptID,
              Empty_Legal_ReceiptID, NotAll_Empty_Legal_ReceiptID, NoEmpty_Legal_ReceiptID]
        for m in range(len(ss)):
            sss = ss[m]
            ddd = dd[m]
            sss = sss.split('>')
            for cc in ["承运商下单", "excel导入", "六和对接", "乳业导入", "WMS下单", "虚拟订单"]:
                try:
                    sss.append(ddd.loc[:, '订单来源'].value_counts()["%s" % cc])
                except KeyError:
                    sss.append(0)
            # print(sss)
            sss = pd.DataFrame(sss).T
            # print(sss)
            sss.to_csv('异常情况汇总报告.csv', mode='a', header=False, encoding='gbk', index=False)


Write = analyse('订单信息.csv')
# 获取具体哪天的数据，注意时间格式
Write.get_data()