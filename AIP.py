#! /usr/bin/env python
#coding: utf-8

__author__ = 'Administrator'
#AIP: automatic investment plan, 基金定投

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import datetime
import time
import urllib2
import mail

class AIP():
    def __load_config_file(self, filename):
        with open(filename, 'r') as f:
            return json.loads(f.read())

    def __init__(self):
        config = self.__load_config_file("./conf/AIP_config.json")

        self.__mail = config["mail_config"]
        self.__month_money = config["month_money"]
        self.__cube_fixed = config["cube_fixed"]
        self.__cube_value = config["cube_value"]
        self.__last = datetime.datetime.strptime(config["start"],"%Y-%m")
        tmp = config["trade_date"].encode('utf-8').split(',')
        self.__trade_date = [int(m) for m in tmp]
        self.__today = datetime.datetime.today()
        self.__timegap_day = 24*60*60
        self.__timegap_min = 60*30
        self.__deal_dir = config["deal_dir"]
        self.__dealer_config = config.get("dealer_config", {})

    def __is_trade_time(self, time_obj):
        if not time_obj.day in self.__trade_date:
            return 1
        if self.__today.month == self.__last.month and self.__today.year == self.__last.year:
            return 2

        starttime = datetime.datetime.strptime(time_obj.strftime("%Y-%m-%d") + " 13:25:00", "%Y-%m-%d %H:%M:%S")
        endtime = datetime.datetime.strptime(time_obj.strftime("%Y-%m-%d") + " 15:00:00", "%Y-%m-%d %H:%M:%S")
        if time_obj < starttime or time_obj > endtime:
            return 3
        return 0

    def __get_net(self, code):
        url = "http://hq.sinajs.cn/list=" + code
        res = urllib2.urlopen(url)
        line = res.read()
        sep = line.split(',')
        return float(sep[3])

    def __store_deal(self, deal):
        file_name = deal["stock_id"] + "_" + str(deal["price"]) + "_" + str(deal["share"]) + "_" + str(deal["action"])
        print file_name
        with open("%s/%s" % (self.__deal_dir, file_name), "w") as f:
            f.write("\n")
        return

    def __send_mail(self, deal_list):
        mail_detail = "<p>调仓时间啦</p>\n"
        mail_detail += "<table border=\"1\"><tbody>\n"
        mail_detail += u"<tr>\n"
        mail_detail += u"<td>股票id</td>\n"
        mail_detail += u"<td>股票名称</td>\n"
        mail_detail += u"<td>交易价格</td>\n"
        mail_detail += u"<td>交易数量</td>\n"
        mail_detail += u"</tr>\n"

        for item in deal_list:
            stock_id = item["stock_id"]
            stock_name = item["stock_name"]
            price = item["price"]
            share = item["share"]

            mail_detail += u"<tr>\n"
            mail_detail += u"<td>" + str(stock_id) + "</td>\n"
            mail_detail += u"<td>" + str(stock_name) + "</td>\n"
            mail_detail += u"<td>" + str(price) + "</td>\n"
            mail_detail += u"<td>" + str(share) + "%</td>\n"
            mail_detail += u"</tr>\n"

        title = "调仓啦~~(潘文海)"

        mail_detail += "</tbody></table>\n"

        mail_detail += "<br/>\n"
        mail_detail += "<p>生成订单:</p>\n"
        mail_detail += "<table border=\"1\"><tbody>\n"
        mail_detail += u"<tr>\n"
        mail_detail += u"<td>动作</td>\n"
        mail_detail += u"<td>证券id</td>\n"
        mail_detail += u"<td>证券名字</td>\n"
        mail_detail += u"<td>交易价格</td>\n"
        mail_detail += u"<td>交易股数</td>\n"
        mail_detail += u"</tr>\n"

        for deal in deal_list:
            mail_detail += u"<tr>\n"
            mail_detail += u"<td>" + str(deal["action"]) + "</td>\n"
            mail_detail += u"<td>" + str(deal["stock_id"]) + "</td>\n"
            mail_detail += u"<td>" + str(deal["price"]) + "</td>\n"
            mail_detail += u"<td>" + str(deal["share"]) + "</td>\n"
            mail_detail += u"</tr>\n"

        mail_detail += "</tbody></table>\n"


        if "email" in self.__dealer_config:

            for mail_address in self.__dealer_config["email"]:
                # mail.sendhtmlmail([mail_address], title,mail_detail.encode("utf-8", "ignore"))

                mail.sendhtmlmail(['sunada2005@163.com'], title,mail_detail.encode("utf-8", "ignore"))

        return

    def AIP_fixedMonthMoney(self):
        deal_list = []
        for cube_id in self.__cube_fixed:
            net = self.__get_net(cube_id)
            share = int(self.__month_money / net / 100) * 100
            deal = {}
            deal["stock_id"] = cube_id
            deal["price"] = net
            deal["share"] = share
            deal["action"] = "buy"
            deal["stock_name"] = self.__cube_fixed[cube_id]
            self.__store_deal(deal)
            deal_list.append(deal)

        return deal_list

    def AIP_valueAvergaging(self):
        return 1

    def AIP(self):
        while True:
            res = self.__is_trade_time(datetime.datetime.now())
            print res
            #res=1 表示不在定投日期内；2 表示该月已经定投；3 表示不在定投日规则定投时间内；0表示可定投
            if res == 1 or res == 2:
                # break;
                time.sleep(self.__timegap_day)
                continue
            elif res == 3:
                time.sleep(self.__timegap_min)
                continue

            deal_list = self.AIP_fixedMonthMoney()
            self.AIP_valueAvergaging()

            self.__last = self.__today
            self.__send_mail(deal_list)

if __name__ == "__main__":
    aip = AIP()
    aip.AIP()
