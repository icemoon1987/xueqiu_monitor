import time
from datetime import datetime
import json
import sys
import os
import logging
import shutil

config_str='''
{
    "deal_dir" : "E:/deal",
    "success_dir" : "./success",
    "fail_dir" : "./fail",
    "log_dir" : "./log",
    "app_path" : "网上股票交易"
}
'''

class AutoTrader(object):
    def __load_config(self, config_str):
        return json.loads(config_str)

    def __init__(self, config_str):
        config = self.__load_config(config_str)

        self.__deal_dir = config["deal_dir"]
        self.__success_dir = config.get("success_dir", "./success")
        self.__fail_dir = config.get("fail_dir", "./fail")
        self.__log_dir = config.get("log_dir", "./log")
        self.__app_path = config.get("app_path")

        if not os.path.exists(self.__deal_dir):
            print "deal_dir=%s not found!" %(self.__deal_dir)
            quit()

        if not os.path.exists(self.__log_dir):
            os.mkdir(self.__log_dir)

        if not os.path.exists(self.__success_dir):
            os.mkdir(self.__success_dir)

        if not os.path.exists(self.__fail_dir):
            os.mkdir(self.__fail_dir)

        if not os.path.exists(self.__log_dir):
            os.mkdir(self.__log_dir)

        logging.basicConfig(level=logging.DEBUG, filename="%s/%s.log.%s" % (self.__log_dir, "auto_trader", datetime.now().strftime("%Y%m%d")), filemode="a", format="%(asctime)s [%(levelname)s] [%(lineno)d] %(message)s")
        return

    def __health_check(self):
        switchApp(self.__app_path)
        type(Key.F1)
        time.sleep(0.5)
        if not exists("buy_label.png"):
            return False

        time.sleep(0.5)

        type(Key.F2)
        time.sleep(0.5)
        if not exists("sell_label.png"):
            return False
    
        return True

    def __open_buy_page(self):
        switchApp(self.__app_path)
        self.__health_check()
        type(Key.F1)
        time.sleep(0.5)
        if not exists("buy_label.png"):
            return False
        return True

    def __open_sell_page(self):
        switchApp(self.__app_path)
        self.__health_check()
        type(Key.F2)
        time.sleep(0.5)
        if not exists("sell_label.png"):
            return False
        return True

    def buy(self, stock_id, price, share):

        self.__open_buy_page()
        type(stock_id)
        time.sleep(0.5)
        type(Key.TAB)
        type(price)
        type(Key.TAB)
        type(share)
        type("b")
        time.sleep(0.3)
        type("y")
        time.sleep(0.3)
        type("y")
        time.sleep(0.3)
        type(Key.ENTER)
        time.sleep(0.2)
        type(Key.ENTER)
        time.sleep(0.2)
        type(Key.ENTER)
        if exists("confirm.png"):
            click("confirm.png")     

        return True


    def sell(self, stock_id, price, share):

        self.__open_sell_page()

        type(stock_id)
        time.sleep(0.5)
        type(Key.TAB)
        type(price)
        type(Key.TAB)
        type(share)
        type("s")
        time.sleep(0.3)
        type("y")
        time.sleep(0.3)
        type("y")
        time.sleep(0.3)
        type(Key.ENTER)
        time.sleep(0.2)
        type(Key.ENTER)
        time.sleep(0.2)
        type(Key.ENTER)
        if exists("confirm.png"):
            click("confirm.png")     

        return True

    def __oneround(self):
        file_list = os.listdir(self.__deal_dir)

        for file_name in file_list:
            #002216_9.56_500_sell
            ary = file_name.split("_")
            stock_id = ary[0]
            price = ary[1]
            share = ary[2]
            action = ary[3]

            if action == "buy":
                self.buy(stock_id, price, share)
            elif action == "sell":
                self.sell(stock_id, price, share)
            else:
                continue

            shutil.move(self.__deal_dir + "/" + file_name, self.__success_dir + "/" + file_name)

            time.sleep(2)

        return True

    def start(self):
        while True:
            self.__oneround()
            if not self.__health_check():
                switchApp(self.__app_path)
                type(Key.ENTER)
                if exists("confirm.png"):
                    click("confirm.png")     
            time.sleep(3)
        return

trader = AutoTrader(config_str)
trader.start()
