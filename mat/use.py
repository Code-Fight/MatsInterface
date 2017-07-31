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
    sql = '''SELECT TB_FDN_MATERIALS_DETAIL.ID,
      TB_FDN_MATERIALS_DETAIL.PARENT_CODE,
      TB_FDN_MATERIALS_CARD.WZBM,
      TB_FDN_MATERIALS_DETAIL.INSERT_TIME,
      fun_GetMatCount(TB_FDN_MATERIALS_CARD.WZBM,TB_FDN_MATERIALS_DETAIL.PARENT_CODE) COUNT,
      TB_FDN_MATERIALS_CARD.HSDJ,
      fun_GetAimDept(TB_FDN_MATERIALS_USE.YHDW_CODE,'10802')duan_code,
      TB_FDN_MATERIALS_CARD.WZM,
      TB_FDN_MATERIALS_CARD.WZLB_CODE,
      TB_FDN_MATERIALS_CARD.GGXH,
      TB_FDN_MATERIALS_WAREHOUSE.CODE,
      TB_FDN_MATERIALS_DETAIL.MATERIALS_CODE,
      TB_FDN_MATERIALS_USE.SUBJECT_DEP_NAME,
      TB_FDN_MATERIALS_SUBJECT.TRAIN_CODE
    FROM TB_FDN_MATERIALS_DETAIL
    LEFT JOIN TB_FDN_MATERIALS_USE
    ON TB_FDN_MATERIALS_USE.CODE=TB_FDN_MATERIALS_DETAIL.PARENT_CODE
    LEFT JOIN TB_FDN_MATERIALS_CARD
    ON TB_FDN_MATERIALS_CARD.ID=TB_FDN_MATERIALS_DETAIL.MATERIALS_ID
    LEFT JOIN TB_FDN_MATERIALS_WAREHOUSE
    ON TB_FDN_MATERIALS_WAREHOUSE.ID          =TB_FDN_MATERIALS_DETAIL.CK_CODE
    LEFT JOIN TB_FDN_MATERIALS_SUBJECT
    ON Tb_Fdn_Materials_Subject.Code=TB_FDN_MATERIALS_USE.SUBJECT_CODE
    WHERE TB_FDN_MATERIALS_DETAIL.OP_TYPE_CODE='65002'
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
                        "usetransId": temp[0],  # 主键
                        "usetransStocknum": temp[2],  # 物资编号
                        "usetransStockname": temp[7],  # 物资名称
                        # "usetransWonum": '123',  # 工单号
                        "usetransLocation": temp[10],  # 位置
                        "usetransModel": temp[9],  # 规格型号
                        "usetransType": 'ISSUE',  # 使用类型（发放ISSUE/退回RETURN）
                        "usetransQuality": '-'+temp[4],  # 数量
                        "usetransPrice": temp[5],  # 单价
                        # "usetransDevicenum": '123',  # 设备
                        # "usetransWorkarea": '123',  # 工区
                        # "usetransWorkshop": '123',  # 车间
                        "usetransStation": temp[6],  # 段
                        "usetransStockstate": '1',  # 条件代码（1良好、2在修、3报废等等）
                        "usetransDate": temp[3].strftime('%Y-%m-%d'),  # 使用日期yyy-MM-dd hh:mm:ss
                        "usetransPerson": temp[12],  # 使用人
                        "businessCategory": 'keyun',  # 业务分类（例：chewu车务、jiwu机务、gongwu工务等等）
                        # "usetransStoreloc": temp[10],  # 仓库名称
                        # "usetransCurbal": '123',  # 库存数量
                        "usetransLocationdesc": temp[13],  # 位置描述
                        # "usetransReason": '123',  # 上下线原因
                        "batchNo": '001'  # 批次号 TODO:需要修改
                    }
                ],
                "method": "saveMatusetrans",
                "type": "keyun"
            }
        }
        ret = Http.Get(params)
        print(ret)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + temp[2] + " | " + ret[8:10])

        Log.Write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + temp[2] + " | " + ret[8:10])
        # return
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
