# -*- coding: utf-8 -*-
# Author zfCode
import logging
import datetime

class Log:
    @staticmethod
    def Write(msg):
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='error' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log',
                            filemode='a+')
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s:%(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)


        logging.error(msg)


if __name__=="__main__":
    Log.Write("test")

