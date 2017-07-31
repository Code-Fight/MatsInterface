# -*- coding: utf-8 -*-
# Author zfCode
import urllib
import json
import urllib.request
from log import Log
class Http:
    def __init__(self):
        # self.url="http://10.32.112.165/railway_material/m3/pubWebservice.do"
        self.url = "http://10.32.112.165/railway_material/m3/pubWebservice.do"

    def Get(self, params, retries=3):
        try:
            data = urllib.parse.urlencode(params)
            # data = json.dumps(params)
            # print(data)
            data=data.encode(encoding='UTF8')
            # req = urllib.request.Request(self.url+'?'+params)
            # response = urllib.request.urlopen(self.url+"?data="+data)
            response = urllib.request.urlopen(self.url, data)
            the_page = response.read()
            ret = the_page.decode("UTF-8")
            return ret
        except Exception as e:
            Log.error(e)
            # print(e)
            if retries> 0:
                return self.Get(params, retries-1)
            else:
                return 'Get Failed'




if __name__=="__main__":
    params = {
        "data": {
            "data":[
                {
                    "param":"111KyJuDept",
                    "data":[
                        {
                            "deptName":"仓库名称",
                            "parentDeptId":"1.1",
                            "stationId":"1",
                            "deptCode":"1",
                            "businessCategory":"gw",
                            "deptTypeId":"1",
                            "deptId":"1"
                        }
                    ],
                    "pkId":" deptId "
                }
            ],
            "method":"saveReturnDataParam",
            "type":"1"
        }
    }
    # print(urllib.request.urlopen('''http://10.32.112.165/railway_material/m3/pubWebservice.do?data={"data": [{"param": "KyJuDept", "data": [{"deptName": "\u4ed3\u5e93\u540d\u79f0", "parentDeptId": "1.1", "stationId": "1", "deptCode": "1", "businessCategory": "gw", "deptTypeId": "1", "deptId": "1"}], "pkId": " deptId "}], "method": "saveReturnDataParam", "type": "1"}''').read().decode("UTF-8"))

    H=Http()
    print(H.Get(params))

