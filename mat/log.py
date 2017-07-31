# -*- coding: utf-8 -*-
# Author zfCode
import logging
import datetime

class Log:
    logging.basicConfig(level=logging.NOTSET,
                        format='%(asctime)s %(filename)s[line:%(lineno)d]\t%(levelname)s\t%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='[LOG]' + datetime.datetime.now().strftime('%Y-%m-%d') + '.log',
                        filemode='a+')
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]\t%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def Write(msg):
        Log.info(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def debug(msg):
        logging.debug(msg)


if __name__=="__main__":
    Log.Write("Write test")
    Log.Write("Write test")
    Log.Write("Write test")
    Log.Write("Write test")
    Log.Write("------------")

    Log.error("error 1test")
    Log.error("error 1test")
    Log.error("error 1test")
    Log.error("error 1test")
    Log.Write("------------")
    Log.debug("debug 1test")
    Log.debug("debug 1test")
    Log.debug("debug 1test")
    Log.debug("debug 1test")
    Log.Write("------------")


