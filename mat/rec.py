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
    sql = '''SELECT TB_FDN_MATERIALS_DETAIL.ID,TB_FDN_MATERIALS_DETAIL.PARENT_CODE,TB_FDN_MATERIALS_CARD.WZBM,TB_FDN_MATERIALS_DETAIL.INSERT_TIME,
      fun_GetMatCount(TB_FDN_MATERIALS_CARD.WZBM,TB_FDN_MATERIALS_DETAIL.PARENT_CODE) COUNT,
      TB_FDN_MATERIALS_CARD.HSDJ,
      fun_GetAimDept(TB_FDN_MATERIALS_INTAKE.YHDW_CODE,'10802')duan_code,
      TB_FDN_MATERIALS_CARD.WZM,
      TB_FDN_MATERIALS_CARD.WZLB_CODE,
      TB_FDN_MATERIALS_CARD.GGXH,
      TB_FDN_MATERIALS_WAREHOUSE.CODE,
      TB_FDN_MATERIALS_DETAIL.MATERIALS_CODE
    FROM TB_FDN_MATERIALS_DETAIL
    LEFT JOIN TB_FDN_MATERIALS_INTAKE
    ON TB_FDN_MATERIALS_INTAKE.CODE=TB_FDN_MATERIALS_DETAIL.PARENT_CODE
    LEFT JOIN TB_FDN_MATERIALS_CARD
    ON TB_FDN_MATERIALS_CARD.ID=TB_FDN_MATERIALS_DETAIL.MATERIALS_ID
    LEFT JOIN TB_FDN_MATERIALS_WAREHOUSE
    ON TB_FDN_MATERIALS_WAREHOUSE.ID          =TB_FDN_MATERIALS_DETAIL.CK_CODE
    WHERE TB_FDN_MATERIALS_DETAIL.OP_TYPE_CODE='65001'
    '''

    # print(sql)

    ret = orcale.ExecuteData(sql)
    # print(ret)
    # return
    for temp in ret:
        # print(temp[18].strftime('%Y-%m-%d'))
        # print(datetime.datetime.strptime(temp[18],'%Y-%m-%d'))
        # return
        Http = HttpHelper.Http()
        params = {
            "data": {
                "data": [
                    {
                        "rectransId": temp[0],
                        "rectransItemnum": temp[2],
                        "rectransTransdate": temp[3].strftime('%Y-%m-%d'),
                        "rectransQuantity": temp[4],
                        "rectransIssuetype": 'RECEIPT',
                        "rectransPrice": temp[5],
                        "rectransUnit":"",
                        "rectransPonum": "",
                        "rectransWorkshop": "",
                        "rectransStation": temp[6],
                        "rectransPolinenum": "",
                        "rectransMemo": "",
                        "rectransFromconditioncode": "",
                        "rectransItemname":temp[7],
                        "rectransItemtype": 'ITEM',# if temp[8] == '64001' else 'TOOL',
                        "rectransToconditioncode": 1,
                        "rectransLinename": "",
                        "rectransLinetype": "",
                        "buinessCategory": 'keyun',
                        "rectransFromlocation": "",
                        "rectransFrombin": "",
                        "rectransTobin": "",
                        "rectransFromlot": "",
                        "rectransManufacturer": "",
                        "rectransManufacturerDate": "",
                        "rectransModel": temp[9],
                        "rectransTolocation": temp[10],
                        "rectransAssetnum":temp[11],
                        "rectransTolot":'001',#temp[3].strftime('%Y-%m-%d'), TODO：批次需要修改
                        "rectransMaxnum":'',
                        "rectransMinnum":'',
                        "rectransQualitydate": '',
                        "overhaulPeriod": '',
                        'rectransLifeperiod':''
                    }
                ],
                "method": "saveMatrectrans",
                "type": "keyun"
            }
        }
        ret = Http.Get(params)
        print(ret)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + temp[2] + " | " + ret[8:10])

        # return
        time.sleep(0.1)

# 启动item接口
def Start():
    SetData()


if __name__ == "__main__":
    print('start...')
    # #datetime.datetime.strftime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d %H:%M:%S")
    # print(datetime.datetime.strftime('datetime.datetime(2012, 9, 23, 21, 37, 4, 177393)','%A %B %d, %Y'))
    # print(datetime.datetime.strptime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d"))
    Start()
