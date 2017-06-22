# -*- coding: utf-8 -*-
# Author zfCode
import urllib
import json
import urllib.request

class Http:
    def __init__(self):
        # self.url="http://10.32.112.165/railway_material/m3/pubWebservice.do"
        self.url = "http://10.32.112.165/railway_material/m3/pubWebservice.do"
        self.proxy_support = urllib.request.ProxyHandler({"http": "http://quickhigh:quickhigh@223.100.134.235:808/"})

        self.proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        self.opener = urllib.request.build_opener(self.proxy_support)
        urllib.request.install_opener(self.opener)


    def Get(self, params):
        try:
            data = urllib.parse.urlencode(params)
            # data = json.dumps(params)
            print(data)
            data=data.encode(encoding='UTF8')
            # req = urllib.request.Request(self.url+'?'+params)
            # response = urllib.request.urlopen(self.url+"?data="+data)
            response = urllib.request.urlopen(self.url, data)
            the_page = response.read()
            return the_page.decode("UTF-8")
        except urllib.error.HTTPError as e:
            print('--------------error--------------')
            print(e.code)
            print(e.info())
            print(e.geturl())
            print(e.read())




if __name__=="__main__":
    params = {
        "data": {
            "data":[
                {
                    "param":"KyJuDept",
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
    H.Get(params)