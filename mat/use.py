# -*- coding: utf-8 -*-
# Author zfCode
import time
import datetime
import HttpHelper
import OracleHelper
from log import Log


# 读数据库数据
def GetData():
    '''
    从数据库获取用料数据，用料数据-退料数据=接口用料数据
    :return:
    '''
    orcale = OracleHelper.Oracle('***')
    sql = "select *  from TB_FDN_MATERIALS_USE WHERE YHDW_CODE='DEPT000073' and TIME>to_date('2017-07-20','yyyy-MM-dd') order by TIME"
    use_data = orcale.ExecuteData(sql)
    print(len(use_data))
    for use in use_data:
        # print(use[6])
        # 获取备品用料详情
        detail_sql = '''
                select * from (
                select max(ID)new_id,MATERIALS_ID,PC,sum(COUNT)COunt from (
                select TB_FDN_MATERIALS_DETAIL.*,SUBSTR(Materials_Code,13,8)PC from TB_FDN_MATERIALS_DETAIL
                where PARENT_CODE='{0}' and Materials_Type_Code='64002' and Materials_Code  not in (
                select Materials_Code from TB_FDN_MATERIALS_DETAIL where PARENT_CODE=
                (select CODE from TB_FDN_MATERIALS_RETURN where P_ID='{0}'))) group by PC,MATERIALS_ID) A
                left join TB_FDN_MATERIALS_CARD on TB_FDN_MATERIALS_CARD.ID=A.MATERIALS_ID
                '''.format(use[6])
        bp_use_detail_data = orcale.ExecuteData(detail_sql)
        if len(bp_use_detail_data) > 0:
            for bp in bp_use_detail_data:
                # def SetParams(id, num, name, loca, model, count, price, duan, date, peo, zhichu, pc)
                param = SetParams(bp_use_detail_data[0],
                                  bp[6],
                                  bp[5],
                                  use[4],  # ck
                                  bp[8],
                                  bp[3],
                                  bp[10],
                                  use[14],  # duan
                                  use[1],  # date
                                  use[2],  # peo
                                  use[13],  # zhichu
                                  bp[2])
                print(param)
                SetData(param,use[6])

        # 获取消耗品用料详情
        detail_sql = '''select *from(
select MATERIALS_ID,ID as NEW_ID,(NVL(A.COUNT,0)-NVL(B.T_COUNT,0))NEW_COUNT,A.MATERIALS_CODE from (
select TB_FDN_MATERIALS_DETAIL.*,SUBSTR(Materials_Code,13,8)PC from TB_FDN_MATERIALS_DETAIL
where PARENT_CODE='{0}' and Materials_Type_Code='64001')A
left join
(select MATERIALS_CODE,sum(count)T_COUNT from TB_FDN_MATERIALS_DETAIL where PARENT_CODE in
(select CODE from TB_FDN_MATERIALS_RETURN where P_ID='{0}') and Materials_Type_Code='64001'
group by MATERIALS_CODE
)B on B.MATERIALS_CODE=A.MATERIALS_CODE)C
left join TB_FDN_MATERIALS_CARD on TB_FDN_MATERIALS_CARD.ID=C.MATERIALS_ID
        '''.format(use[6])
        print(detail_sql)
        xh_use_detail_data = orcale.ExecuteData(detail_sql)
        if len(xh_use_detail_data) > 0 :
            for xh in xh_use_detail_data:
                # def SetParams(id, num, name, loca, model, count, price, duan, date, peo, zhichu, pc)
                param = SetParams(xh[1],
                                  xh[6],
                                  xh[5],
                                  use[4],  # ck
                                  xh[8],
                                  xh[2],
                                  xh[10],
                                  use[14],  # duan
                                  use[1],  # date
                                  use[2],  # peo
                                  use[13],  # zhichu
                                  xh[3][12:20])
                print(param)
                SetData(param,use[6])

def SetParams(id, num, name, loca, model, count, price, duan, date, peo, zhichu, pc):
    params = {
        "data": {
            "data": [
                {
                    "usetransId": id,  # 主键
                    "usetransStocknum": num,  # 物资编号
                    "usetransStockname": name,  # 物资名称
                    # "usetransWonum": '123',  # 工单号
                    "usetransLocation": loca,  # 位置
                    "usetransModel": model,  # 规格型号
                    "usetransType": 'ISSUE',  # 使用类型（发放ISSUE/退回RETURN）
                    "usetransQuality": '-' + str(count),  # 数量
                    "usetransPrice": price,  # 单价
                    # "usetransDevicenum": '123',  # 设备
                    # "usetransWorkarea": '123',  # 工区
                    # "usetransWorkshop": '123',  # 车间
                    "usetransStation": duan,  # 段
                    "usetransStockstate": '1',  # 条件代码（1良好、2在修、3报废等等）
                    "usetransDate": date.strftime('%Y-%m-%d'),  # 使用日期yyy-MM-dd hh:mm:ss
                    "usetransPerson": peo,  # 使用人
                    "businessCategory": 'keyun',  # 业务分类（例：chewu车务、jiwu机务、gongwu工务等等）
                    # "usetransStoreloc": temp[10],  # 仓库名称
                    # "usetransCurbal": '123',  # 库存数量
                    "usetransLocationdesc": zhichu,  # 位置描述
                    # "usetransReason": '123',  # 上下线原因
                    "batchNo": pc  # 批次号
                }
            ],
            "method": "saveMatusetrans",
            "type": "keyun"
        }
    }
    return params


# 写接口数据
def SetData(data, order):
    # print(ret)
    # return
    http = HttpHelper.Http()
    ret = http.Get(data)
    print(ret)
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + order + " | " + ret[8:10])

    Log.Write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + order + " | " + ret[8:10])
    # return
    # return
    # time.sleep(1)


# 启动item接口
def Start():
    GetData()


if __name__ == "__main__":
    print('start...')
    # #datetime.datetime.strftime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d %H:%M:%S")
    # print(datetime.datetime.strftime('datetime.datetime(2012, 9, 23, 21, 37, 4, 177393)','%A %B %d, %Y'))
    # print(datetime.datetime.strptime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d"))
    Start()
