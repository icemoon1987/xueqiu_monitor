#! /usr/bin/env python
#coding: utf-8

import re
import mail
import hashlib
import json
import os
import time
import logging
import urllib
import urllib2
import cookielib
import shutil
import socket
import json
from datetime import datetime, timedelta

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class XueqiuMonitor(object):


    def __init__(self):
        self.__cube_map = {
                    "ZH928259": "成长之王策略",
                    "ZH218796": "小盘股王子"
                }

        self.__log_dir = "./log"
        self.__tmp_dir = "./tmp"
        self.__backup_dir = "./backup"
        self.__result_dir = "./result"

        if not os.path.exists(self.__log_dir):
            os.mkdir(self.__log_dir)

        if not os.path.exists(self.__tmp_dir):
            os.mkdir(self.__tmp_dir)

        if not os.path.exists(self.__backup_dir):
            os.mkdir(self.__backup_dir)

        if not os.path.exists(self.__result_dir):
            os.mkdir(self.__result_dir)

        logging.basicConfig(level=logging.DEBUG, filename="%s/%s.log" % (self.__log_dir, __file__[:-3]), filemode='a', format='%(asctime)s [%(levelname)s] [%(lineno)d] %(message)s')
        self.__logger = logging.getLogger(__name__)
        self.__timegap = 30
        self.__header = { 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive', 'Host':'xueqiu.com' }
        self.__urlopener = None

        return


    def __get_rebalance_id(self, cube_id):
        """ 获取一个组合的最新调仓策略id """

        url = "https://xueqiu.com/P/%s" % (cube_id)
        req = urllib2.Request(url, headers=self.__header)
        resp = self.__urlopener.open(req)
        html = resp.readlines()

        for line in html:
            m = re.match(r'.*SNB.cubeInfo = {(.*)?}.*', line)
            if m != None:
                json_str = m.group(1)
    
        json_obj = json.loads("{" + json_str + "}")
        rb_id = json_obj["last_user_rb_gid"]

        return rb_id


    def __crawl_rebalance(self, cube_id):
        """ 获取一个组合的调仓策略 """

        # 获取最新调仓策略id
        rb_id = self.__get_rebalance_id(cube_id)

        # 获取调仓策略
        url = "https://xueqiu.com/cubes/rebalancing/show_origin.json?rb_id=%d&cube_symbol=%s" % (rb_id, cube_id)
        req = urllib2.Request(url, headers=self.__header)
        resp = self.__urlopener.open(req)
        html = resp.read()
        json_obj = json.loads(html)

        result = {}
        result["cube_id"] = cube_id
        result["rb_timestamp"] = json_obj["rebalancing"]["updated_at"]
        result["trade_action"] = []

        history = json_obj["rebalancing"]["rebalancing_histories"]

        for item in history:
            tmp = {}
            tmp["stock_id"] = item["stock_symbol"]
            tmp["stock_name"] = item["stock_name"]
            tmp["price"] = item["price"]

            tmp["pre_rate"] = item.get("prev_weight_adjusted", 0)
            if not tmp["pre_rate"]:
                tmp["pre_rate"] = 0

            tmp["post_rate"] = item.get("target_weight", 0)
            if not tmp["post_rate"]:
                tmp["post_rate"] = 0

            result["trade_action"].append(tmp)

        return result


    def __send_mail(self, rb_result):

        mail_detail = "<p>调仓时间：" + str(datetime.fromtimestamp(int(rb_result["rb_timestamp"]) / 1000)) + "</p>\n"
        mail_detail += "<table border=\"1\"><tbody>\n"
        mail_detail += u"<tr>\n"
        mail_detail += u"<td>股票id</td>\n"
        mail_detail += u"<td>股票名称</td>\n"
        mail_detail += u"<td>交易价格</td>\n"
        mail_detail += u"<td>原仓位</td>\n"
        mail_detail += u"<td>现仓位</td>\n"
        mail_detail += u"</tr>\n"

        for item in rb_result["trade_action"]:
            stock_id = item["stock_id"]
            stock_name = item["stock_name"]
            price = item["price"]
            pre_rate = item["pre_rate"]
            post_rate = item["post_rate"]

            mail_detail += u"<tr>\n"
            mail_detail += u"<td>" + str(stock_id) + "</td>\n"
            mail_detail += u"<td>" + str(stock_name) + "</td>\n"
            mail_detail += u"<td>" + str(price) + "</td>\n"
            mail_detail += u"<td>" + str(pre_rate) + "%</td>\n"
            mail_detail += u"<td>" + str(post_rate) + "%</td>\n"
            mail_detail += u"</tr>\n"

        title = rb_result["cube_id"] + self.__cube_map[rb_result["cube_id"]] + "调仓啦~~(潘文海)"

        mail_detail += "</tbody></table>\n"
        #mail.sendhtmlmail(['546674175@qq.com', '182101630@qq.com', '81616822@qq.com', '373894584@qq.com'], title,mail_detail.encode("utf-8", "ignore"))
        mail.sendhtmlmail(['546674175@qq.com'], title,mail_detail.encode("utf-8", "ignore"))

        return


    def __store_rb_timestamp(self, rb_result):
        with open("%s/%s.timestamp" % (self.__tmp_dir, rb_result["cube_id"]), "w") as f:
            f.write(str(rb_result["rb_timestamp"]))
        return


    def __get_latest_rb_timestamp(self, cube_id):
        try:
            with open("%s/%s.timestamp" % (self.__tmp_dir, cube_id), "r") as f:
                return int(f.read())
        except Exception, ex:
            return 0


    def __store_record(self, rb_result):
        with open("%s/%s.record" % (self.__backup_dir, rb_result["cube_id"]), "a") as f:
            f.write(json.dumps(rb_result))
            f.write("\n")
        return


    def __store_result(self, rb_result):
        with open("%s/%s.%d" % (self.__result_dir, rb_result["cube_id"], rb_result["rb_timestamp"]), "w") as f:
            f.write(json.dumps(rb_result))
            f.write("\n")
        return

    def __refresh_cookie(self):
        cj = cookielib.CookieJar()
        self.__urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        url = "https://xueqiu.com"
        req = urllib2.Request(url, headers=self.__header)
        resp = self.__urlopener.open(req)
        return


    def start_monitor(self):

        self.__refresh_cookie()
        self.__logger.info("start monitoring...")

        while True:
            try:
                for cube_id in self.__cube_map:
                    rb_result = self.__crawl_rebalance(cube_id)
                    rb_timestamp = int(rb_result["rb_timestamp"])
                    latest_rb_timestamp = self.__get_latest_rb_timestamp(cube_id)

                    self.__logger.debug("crawl cube_id=%s, rb_timestamp=%d, latest_rb_timestamp=%d" % (cube_id, rb_timestamp, latest_rb_timestamp))
                    # 如果没有最近调仓或新调仓时间大于最近调仓，说明是一次新的调仓记录
                    if latest_rb_timestamp == None or rb_timestamp > latest_rb_timestamp:

                        # 如果没有操作，则记录错误
                        if rb_result["trade_action"] == 0:
                            self.__logger.error("no trade_action, something is wrong")
                            continue

                        # 如果没有具体价格，则为挂单，只记录，不触发
                        if rb_result["trade_action"][0]["price"] == None:
                            self.__logger.debug("no price, only record it")
                            self.__store_rb_timestamp(rb_result)
                            self.__store_record(rb_result)
                            continue

                        # 一次正常的调仓，记录并通知
                        self.__logger.info("NEW REBALANCE! store result. cube_id=%s" % (cube_id))
                        self.__store_result(rb_result)
                        self.__store_rb_timestamp(rb_result)
                        self.__store_record(rb_result)
                        self.__send_mail(rb_result)

                    # 一次旧的调仓记录，跳过
                    else:
                        self.__logger.debug("skip old rebalance. cube_id=%s" % (cube_id))

                time.sleep(self.__timegap)
            except Exception, ex:
                self.__refresh_cookie()
                time.sleep(self.__timegap)
                self.__logger.error("network seems down! try to refresh cookie")

        return


if __name__ == "__main__":
    monitor = XueqiuMonitor()
    monitor.start_monitor()

