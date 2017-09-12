# -*- coding: utf-8 -*-
# Author zfCode
import time
import datetime
import HttpHelper
import OracleHelper
from log import Log


# 读数据库数据
def GetData():
    orcale = OracleHelper.Oracle('*')

    try:
        # 先取出来所有的单据  TODO：添加时间过滤
        sql = "select * from TB_FDN_MATERIALS_INTAKE WHERE YHDW_CODE='DEPT000073'"
        order_data = orcale.ExecuteData(sql)
        print(len(order_data))
        # 遍历所有的单据 去找物资信息
        for order in order_data:
            # 取出该订单的物资信息
            sql = '''
                                    select TB_FDN_MATERIALS_DETAIL.*,
                        TB_FDN_MATERIALS_CARD.WZM,
                        TB_FDN_MATERIALS_CARD.WZBM,
                        TB_FDN_MATERIALS_CARD.WZLB,
                        TB_FDN_MATERIALS_CARD.GGXH,
                        TB_FDN_MATERIALS_CARD.JLDW,
                        TB_FDN_MATERIALS_CARD.HSDJ,
                        TB_FDN_MATERIALS_CARD.WZLB_CODE,
                        TB_FDN_MATERIALS_CARD.WZLB_NAME,
                        TB_FDN_MATERIALS_CARD.MAX,
                        TB_FDN_MATERIALS_CARD.MIN,
                        TB_FDN_MATERIALS_CARD.ITEMCATEGORY
                        from TB_FDN_MATERIALS_DETAIL left join TB_FDN_MATERIALS_CARD
                        on TB_FDN_MATERIALS_CARD.ID=TB_FDN_MATERIALS_DETAIL.MATERIALS_ID
                        where PARENT_CODE='%s'
                                    ''' % (order[12])
            # print(sql)

            detail = orcale.ExecuteData(sql)
            # print(detail)

            # 合并该订单物资信息
            mat_detail = []
            for d in detail:
                if len(mat_detail) == 0:
                    mat_detail.append(list(d))
                    continue
                for mat in mat_detail:
                    # print(mat[8])
                    # print(d[8])
                    # print('------------')
                    if mat[4] == d[4]:
                        # print(type( mat))
                        mat[10] = int(mat[10]) + int(d[10])
                        break
                else:
                    # print(d[9].strftime('%Y-%m-%d %H:%M'))
                    # print(type(d[9]))
                    mat_detail.append(list(d))
            # print(mat_detail)
            # 按订单提交数据
            SetData(mat_detail)
            # return


    except BaseException as e:
        print(e)
        # Log.error(e)
        pass
    finally:
        pass

# 写接口数据
def SetData(order_data):
    try:
        http = HttpHelper.Http()
        for data in order_data:
            # print(data)
            # continue
            # print(data[24] if data[24] else 0)
            # return
            params = {
                "data": {
                    "data": [
                        {
                            "rectransId": data[0], # 主键
                            "rectransItemnum": data[17], # 物资编号
                            "rectransTransdate": data[9].strftime('%Y-%m-%d'), # 入库日期yyy-MM-dd hh:mm:ss
                            "rectransQuantity": data[10], # 入库数量
                            "rectransIssuetype": 'RECEIPT',
                            "rectransPrice": data[21], # 接收单价
                            "rectransUnit":"", # 接收单位
                            "rectransPonum": "",  # 采购单号
                            "rectransWorkshop": "", # 车间编号
                            "rectransStation": data[15], # 段编号
                            "rectransPolinenum": "", # 采购明细单号
                            "rectransMemo": "", # 备注
                            "rectransFromconditioncode": "", # 物资原状态
                            "rectransItemname":data[16], # 物资名称
                            "rectransItemtype": 'ITEM',# 物资类型
                            "rectransToconditioncode": 1, # 物资接收状态
                            "rectransLinename": "", # 线名
                            "rectransLinetype": "", # 行别
                            "buinessCategory": 'keyun',  # 业务分类
                            "rectransFromlocation": "", # 资产编号
                            "rectransFrombin": "", # 原货柜
                            "rectransTobin": "", # 目标货柜
                            "rectransFromlot": "", # 原批次
                            "rectransManufacturer": "", # 制造商
                            "rectransManufacturerDate": "", # 生产日期
                            "rectransModel": data[19], # 规格型号
                            "rectransTolocation": data[14], # 接收仓库编号
                            "rectransAssetnum":'', # 资产编号
                            "rectransTolot":str(data[8])[12:20], # 批次
                            "rectransMaxnum":data[24] if data[24] else 0, # 物资在本库最大储备量
                            "rectransMinnum":data[25] if data[24] else 0, # 物资在本库最小储备量
                            "rectransQualitydate": '',# 质保期（天
                            "overhaulPeriod": '', # 超大修期（天）
                            'rectransLifeperiod':'' # 寿命期（天）
                        }
                    ],
                    "method": "saveMatrectrans",
                    "type": "keyun"
                }
            }
            print(params)
            # return
            ret = http.Get(params)
            print(ret)
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | ' + data[2] + " | " + ret[8:10])
    except BaseException as e:
        Log.error(e)

# 启动item接口
def Start():
    GetData()


if __name__ == "__main__":
    print('start...')
    # #datetime.datetime.strftime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d %H:%M:%S")
    # print(datetime.datetime.strftime('datetime.datetime(2012, 9, 23, 21, 37, 4, 177393)','%A %B %d, %Y'))
    # print(datetime.datetime.strptime('datetime.datetime(2017, 5, 11, 0, 0)',"%Y-%m-%d"))
    Start()
