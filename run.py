
#程序入口
import sys
#导入链接数据库，下载数据和邮件发送数据文件
from core.Analyse_data import analyse
from core.Download_data import down_Sql
from core.Emaile_data import emaile



if __name__ == "__main__":
    str1 = "SELECT ord_no AS '',tenant_name AS '', tenant_name AS ''," \
           " CASE odr_channel WHEN 1 THEN '承运商下单' WHEN 5 THEN 'excel导入' WHEN 6 THEN '六合对接' WHEN 7 THEN '乳业导入' ELSE 'WMS下单' END AS ''," \
           "create_time AS '', create_user AS '', consignor_station_code AS '', " \
           "consignor_province_name AS '', consignor_city_name AS '', consignor_county_name AS '', " \
           "consignor_address AS '', concat(consignor_province_name, consignor_city_name, " \
           "consignor_county_name, consignor_address) AS '',receipt_station_code AS '', " \
           "receipt_province_name AS '',receipt_city_name AS '',receipt_county_name AS ''," \
           "receipt_address AS '',carrier_tenant_id AS '' from oms_order_msg WHERE create_time > "2020-07-17 12:00";"

    str2 = "SELECT s.station_code as '', s.customer_station_code as '', " \
           "longitude, latitude FROM bms_stations WHERE delete_status = 0 AND station_type = 0"

    Search1 = down_Sql('root', '123456', str1)
    Search2 = down_Sql('root', '123456', str2)

    data1 = Search1.from_mysql_get_all_info('localhost', 3306, 'mm', 'gbk')
    data2 = Search2.from_mysql_get_all_info('localhost', 3306, 'mm', 'gbk')

    Search1.write_csv(data1, '订单信息.csv')
    Search2.write_csv(data2, '站点库.csv')

    Write = analyse('订单信息.csv')
    # 获取具体哪天的数据，注意时间格式
    Write.get_data()

    #发送邮件，设置发送人，验证码，收件人（可以设置两个）以及邮件主题
    sender1 = emaile("mqw_test@163.com","VPAUITGNHJFNRVLN",["1594015406@qq.com", "mqw_1996@163.com"],  """异常订单详情""",
                     "异常订单详情.csv", "异常情况汇总报告.csv")
    #发送文件
    sender1.send_emaile()

