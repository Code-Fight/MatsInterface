# -*- coding: utf-8 -*-
# Author zfCode
import time
import datetime
import HttpHelper
import OracleHelper
from log import Log


# 读数据库数据
def GetData():
    pass

# 写接口数据
def SetData():
    orcale = OracleHelper.Oracle('dsjky/quickhigh@192.168.2.105:1521/DSJKY_P')
    ret = orcale.ExecuteData("select * from TB_FDN_MATERIALS_WAREHOUSE")
    for temp in ret:
        # print(temp[18].strftime('%Y-%m-%d'))
        # print(datetime.datetime.strptime(temp[18],'%Y-%m-%d'))
        # return
        Http = HttpHelper.Http()
        params = {
            "data": {
                "data": [
                    {
                        "param": "KyJuLocation",
                        "data": [
                            {
                                "locationId": temp[0],
                                "locationName": temp[1],
                                "locationStation": temp[6],
                                "locationType": 'STOREROOM',
                                "businessCategory": 'keyun',
                                "itemAttribute": '1'
                            }
                        ],
                        "pkId": "locationId"
                    }
                ],
                "method": "saveReturnDataParam",
                "type": "keyun"
            }
        }
        ret = Http.Get(params)
        # print(ret)
        # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + temp[0] + " | " + "None" if ret is None else ret)
        Log.info(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + temp[0] + " | " + "None" if ret is None else ret)
        return
        time.sleep(1)

# 启动item接口
def Start():
    SetData()


if __name__ == "__main__":
    print('start...')
    Start()