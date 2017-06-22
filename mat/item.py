# -*- coding: utf-8 -*-
# Author zfCode
import time
import datetime
import HttpHelper
import OracleHelper


# 读数据库数据
def GetData():
    pass

# 写接口数据
def SetData():
    orcale = OracleHelper.Oracle('dsjky/quickhigh@192.168.2.105:1521/DSJKY_P')
    ret = orcale.ExecuteData("select * from TB_FDN_MATERIALS_CARD")
    for temp in ret:
        # print(temp[18].strftime('%Y-%m-%d'))
        # print(datetime.datetime.strptime(temp[18],'%Y-%m-%d'))
        # return
        Http = HttpHelper.Http()
        params = {
            "data": {
                "data": [
                    {
                        "param": "KyJuItem",
                        "data": [
                            {
                                "itemnum": temp[2],
                                "description": temp[1],
                                "issueunit": temp[5],
                                "cModel": temp[4],
                                "itemtype": 'ITEM',# if temp[7] == '64001' else 'TOOL',
                                "createDate": temp[18].strftime('%Y-%m-%d'),
                                "businessCategory": 'keyun',
                                # TODO：这个是材料分类  目前咱们的库里没有
                                "itemcategory": 0,
                                "rotating": '0' # if temp[7] == '64001' else '1'
                            }
                        ],
                        "pkId": " itemnum "
                    }
                ],
                "method": "saveReturnDataParam",
                "type": "keyun"
            }
        }
        ret = Http.Get(params)
        # print(ret)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + temp[2] + " | " + ret[8:10])

        # return
        time.sleep(1)

# 启动item接口
def Start():
    SetData()


if __name__ == "__main__":
    print('start...')
    # #datetime.datetime.strftime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d %H:%M:%S")
    # print(datetime.datetime.strftime('datetime.datetime(2012, 9, 23, 21, 37, 4, 177393)','%A %B %d, %Y'))
    # print(datetime.datetime.strptime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d"))
    Start()