#!/usr/bin/env python
#coding=utf-8


class StockItem(object):

    def __init__(self, stock_id):
        self.stock_id = stock_id
        self.mean_price = 0.0
        self.share = 0
        self.value = 0.0
        self.last_op = ""
        self.last_price = 0.0
        self.last_share = 0

        return


class AccountSimulator(object):

    def __init__(self, name, cash):

        self.name = name
        self.cash = cash
        self.stocks = {}

        return


    def buy(self, stock_id, price, share):

        if stock_id not in self.stocks:
            self.stocks[stock_id] = StockItem(stock_id)

        if (price * share) > self.cash:
            print "not enough cash! cash:%f, try_to_spend:%f" % (self.cash, price*share)
            return False

        self.stocks[stock_id].share += share
        self.stocks[stock_id].value += price * share
        self.cash -= price * share
        self.stocks[stock_id].mean_price = self.stocks[stock_id].value / self.stocks[stock_id].share

        self.stocks[stock_id].last_op = "buy"
        self.stocks[stock_id].last_price = price
        self.stocks[stock_id].last_share = share

        return price * share


    def sell(self, stock_id, price, share):

        if stock_id not in self.stocks:
            return False

        if self.stocks[stock_id].share < share:
            print "you do not have enough share! stock_id:%s, share:%s, try to sell %d shares!" % (stock_id, self.stocks[stock_id].share, share)
            return False

        self.stocks[stock_id].share -= share
        self.stocks[stock_id].mean_price = price
        self.stocks[stock_id].value = self.stocks[stock_id].mean_price * self.stocks[stock_id].share
        self.stocks[stock_id].last_op = "sell"
        self.stocks[stock_id].last_price = price
        self.stocks[stock_id].last_share = share
        self.cash = self.cash + (share * price)

        return price * share


    def get_stock(self, stock_id):

        if stock_id in self.stocks:
            return self.stocks[stock_id]

        return None

    def get_cash(self):
        return self.cash

    def get_value(self):

        result = 0.0

        for stock_id in self.stocks:
            result = result + self.stocks[stock_id].value

        result = result + self.cash

        return result

    def dump_stock(self, stock_id):
        print "*****************************************************************************************************"
        print "stock_stock_id\t\tmean_price\t\tshare\t\tvalue\t\tlast_op\t\tlast_price\t\tlast_share"
        print "%s\t\t%f\t\t%d\t\t%f\t\t%s\t\t%f\t\t%d" % (stock_id, self.stocks[stock_id].mean_price, self.stocks[stock_id].share, self.stocks[stock_id].value, \
            self.stocks[stock_id].last_op, self.stocks[stock_id].last_price, self.stocks[stock_id].last_share)
        print ""

        return

    def dump(self):
        print "*****************************************************************************************************"
        print "stock_stock_id\t\tmean_price\t\tshare\t\tvalue\t\tlast_op\t\tlast_price\t\tlast_share"

        for stock_id in self.stocks:
            print "%s\t\t%f\t\t%d\t\t%f\t\t%s\t\t%f\t\t%d" % (stock_id, self.stocks[stock_id].mean_price, self.stocks[stock_id].share, self.stocks[stock_id].value, \
                self.stocks[stock_id].last_op, self.stocks[stock_id].last_price, self.stocks[stock_id].last_share)
        print "remain cash: %f" % (self.cash)
        print ""


        return


if __name__ == "__main__":

    cost = 0.0
    gain = 0.0

    account = AccountSimulator("panwenhai", 10000)
    cost = cost + account.buy("sh000001", 100, 10)
    account.dump()
    cost = cost + account.buy("sh000001", 50, 10)
    account.dump()
    gain = gain + account.sell("sh000001", 20, 15)
    account.dump()
    gain = gain + account.sell("sh000001", 1000, 5)
    account.dump()

    account.buy("sh000009", 10.02, 45)
    account.buy("sh000010", 10.02, 45)
    account.buy("sh000009", 10.02, 45)
    account.buy("sh000010", 10.02, 45)
    account.buy("sh000010", 10.02, 4500000)

    account.dump()

    print cost, gain, gain - cost

