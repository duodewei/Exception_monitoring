import pymysql
import csv

class down_Sql:
    def __init__(self,user, password, sql):
        self.user = user
        self.password = password
        self.sql = sql

    def from_mysql_get_all_info(self, host, port, db, charset):
        '''
        Connect to the database
        Use the cursor to get all the data in the table
        '''
        conn = pymysql.connect(
            host = host,
            port = port,
            user = self.user,
            db = db,
            password= self.password,     #password
            charset= charset)
        cursor = conn.cursor()
        sql = self.sql
        cursor.execute(self.sql.encode('gbk'))
        data = cursor.fetchall()
        conn.close()
        return data

    def write_csv(self, data, filename):
        '''
        Write data to local
        '''
        filename = filename
        with open(filename, mode='w',newline ='', encoding='gbk') as f:
            write = csv.writer(f,dialect='excel')
            for item in data:
                write.writerow(item)

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