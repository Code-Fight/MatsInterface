# -*- coding: utf-8 -*-
# Author zfCode
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class Oracle:
    # 保存链接参数
    def __init__(self, constr):
        self.conStr = constr
        self.cursor = None
        self.connection = None

    # 建立链接
    def Connect(self):
        if hasattr(self, "cursor") == False or None == self.cursor:
            self.connection = cx_Oracle.connect(self.conStr)
            # 创建游标对象
            self.cursor = cx_Oracle.Cursor(self.connection)

    # 关闭链接
    def Close(self):
        if self.cursor:
            self.cursor.close()
            self.connection.close()
            self.cursor = None

    # 返回游标
    def cur(self):
        try:
            if self.cursor:
                return self.cursor
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            self.Close()

    # 返回本次执行的结果
    def ExecuteData(self, sql):
        try:
            self.Connect()
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            self.Close()
            return ret
        except Exception as e:
            print(e)
        finally:
            self.Close()


    # 返回受影响行数
    def ExecuteNoquery(self, sql):
        try:
            self.Connect()
            temp = self.cursor.execute(sql)
            self.connection.commit()
            ret = temp.fetchone()
            self.Close()
            return ret
        except Exception as e:
            print(e)
        finally:
            self.Close()





    # 析构
    def __del__(self):
        self.Close()


if __name__=="__main__":
    h=Oracle('dsjky/quickhigh@192.168.2.105:1521/DSJKY')
    ret = h.ExecuteData("select * from TB_DIC_CITY")
    for temp in ret:
        print(temp[0])


    # sql = "select * from TB_DIC_CITY"
    #
    # result = h.executeData(sql)
    # count = len(result)
    # print("=====================")
    # print("Total:", count)
    # print("=====================")
    # for row in result:
    #     print(row)
