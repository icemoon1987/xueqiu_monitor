__author__ = 'Administrator'
import json
import datetime

def store_deal(deal,deal_dir):
    file_name = deal["stock_id"] + "_" + str(deal["price"]) + "_" + str(deal["share"]) + "_" + str(deal["action"])
    # print file_name[:8]
    with open("%s/%s" % (deal_dir, file_name[2:]), "w") as f:
        f.write("\n")
    return

def store_record(deal, record_dir):
    with open("%s.record" % (record_dir), "a") as f:
        f.write(json.dumps(deal))
        f.write("\n")
    return

def is_trade_date(date):
    if date.weekday() == 5 or date.weekday() == 6:
        return False

    holidays = ["2017-01-27","2017-01-30","2017-01-31","2017-02-02","2017-02-01","2017-04-03","2017-04-04",
                "2017-05-01","2017-05-29","2017-05-30","2017-10-02","2017-10-03","2017-10-04","2017-10-05",
                "2017-10-06"]

    if date.strftime("%Y-%m-%d") in holidays:
        return False
    return True