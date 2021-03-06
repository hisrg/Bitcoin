# ****************************************************************************************************************
#############################基于Gate.io的自动交易软件
#############################版本号V1.0
# ****************************************************************************************************************
################导入所用的库
from __future__ import print_function
import ccxt
import requests
import time
import datetime
import pandas as pd
import os
import gate_api
from gate_api.rest import ApiException

pd.set_option('expand_frame_repr', False)  # 不让它出现省略号


##################################获取账户信息###################################
def get_info_acc_order(ltc_used, ltc_total):
    print("-------------------------------获取账户信息-----------------------")
    apiKey = '073193AA-70CB-486A-B777-FA1ADF8544D5'
    secret = '1381a2091471e42d0aa4da874a092cb6b1eca48c9c17432f1c492add8f85a058'  # Gate.io Key
    try:
        gateio = ccxt.gateio({"apiKey": apiKey, 'secret': secret})
        balance = gateio.fetch_balance()
        print(balance)
        temp = balance['LTC']  # 获取LTC
        ltc_used = float(temp['used'])
        ltc_total = float(temp['total'])
    except ApiException as e:
        ltc_used = 0
        ltc_total = 0
        print("Woring: Connection fail!!!!!!!" % e)
    print(ltc_total)  # 获取账户余额

    return ltc_used, ltc_total


##############*************************************
################设定阈值
limit_chpercent = 1  ##设定每次交易占余额的百分比
buy_down_percent = 3  ##当行情低于此价格后进入买入操作
sell_up_percent = 6  ##当行情高于此价格后卖出操作
limit_amount = 100  # 设定每次交易量占用百分比 100%,75%等
i = 1
while True:
    print(str(i) + "th try:")
    i = i + 1
    #################Setup 1 获取参数######################
    ##Volume:交易量
    ##high24hr: 43.15 最高价
    ##last:最新成交价
    ##low24hr:最低价
    ##percentChange:涨停百分比
    ##################N0.1 获取LTC当前行情###############
    print("-------------------------------获取LTC当前行情-----------------------")
    BASE_URL = 'https://data.gateio.life'
    report = '/api2/1/ticker/ltc_usdt'
    resp = requests.get(BASE_URL + report)
    resp_json = resp.json()
    # print(resp_json)
    volume = float(resp_json['quoteVolume'])
    # print(type(volume))
    high24hr = float(resp_json['high24hr'])
    # print(type(high24hr))
    # print(high24hr)
    last = float(resp_json['last'])
    low24hr = float(resp_json['low24hr'])
    percentChange = float(resp_json['percentChange'])
    print("Highest in 24hr:" + str(high24hr))
    print("Current Value:" + str(last))
    print("Low in 24hr:" + str(low24hr))
    print("Percent Change:" + str(percentChange))
    print("OK")
    # exit()
    ################N0.2 获取K线#######################
    print("-------------------------------获取LTC K线-----------------------")
    BASE_URL = 'https://data.gateio.life/'
    #
    kline = 'api2/1/candlestick2/ltc_usdt?group_sec=600&range_hour=1'  # 在此处更改时间长度
    # #
    kline_url = BASE_URL + kline
    # print(kline_url)  # 打印网址
    resp = requests.get(kline_url)
    resp_json = resp.json()
    data = resp_json['data']
    # print(data)
    df = pd.DataFrame(data, columns={'time': 0, 'volume': 1, 'close': 2, 'high': 3, 'low': 4, 'open': 5})
    print(df)
    # print(df['time'])
    timelist = df['time']
    # 转换成localtime
    # timestamp = int(timelist[6])
    # print(timestamp)
    # timestamp = float(timestamp / 1000)
    # timearray = time.localtime(timestamp)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
    # print(otherStyleTime)
    print("OK")
    # exit()
    #######################N0.3获取账户信息########################################
    print("-------------------------------获取账户信息-----------------------")
    apiKey = '073193AA-70CB-486A-B777-FA1ADF8544D5'
    secret = '1381a2091471e42d0aa4da874a092cb6b1eca48c9c17432f1c492add8f85a058'  # Gate.io Key
    gateio = ccxt.gateio({"apiKey": apiKey, 'secret': secret})
    balance = gateio.fetch_balance()
    # print(balance)
    temp = balance['LTC']  # 获取LTC
    print(temp)
    usdt_money = balance['USDT']
    usdt_free = usdt_money['free']
    usdt_used = usdt_money['used']
    usdt_total = usdt_money['total']
    ltc_free = float(temp['free'])
    ltc_used = float(temp['used'])
    ltc_total = float(temp['total'])
    print("ltc_free" + str(ltc_free))
    print("ltc_used:" + str(ltc_used))  # 显示账户中的LTC余额
    print("ltc_total:" + str(ltc_total))
    print("usdt_free:" + str(usdt_free))  # 显示账户中的USDT余额
    print("usdt_total:" + str(usdt_total))
    print("usdt_used:" + str(usdt_used))
    # configuration = gate_api.Configuration()
    # configuration.key = '8a3097686a7430c9b49ee6fa2f88f79e'
    # configuration.secret = '7a0322c00bdb949c364d44e8317fbf8cbeef9de0f7945d90650c94dfcd47e751'
    #
    # # create an instance of the API class
    # api_instance = gate_api.SpotApi(gate_api.ApiClient(configuration))
    # order_id = '12345'  # str | ID returned on order successfully being created
    # currency_pair = 'LTC_USDT'  # str | Currency pair
    #
    # try:
    #     # Get a single order
    #     api_response = api_instance.get_order(order_id, currency_pair)
    #     print(api_response)
    # except ApiException as e:
    #     print("Exception when calling SpotApi->get_order: %s\n" % e)

    #######################N0.4获取挂单信息########################################
    print("-------------------------------获取挂单信息-----------------------")
    orders = gateio.fetch_orders('LTC/USDT')
    print(orders)
    len_orders = len(orders)
    order_id = orders[len_orders - 1]['id']
    order_mount = orders[len_orders - 1]['amount']
    order_mode = orders[len_orders - 1]['side']
    order_symbol = orders[len_orders - 1]['symbol']
    # print(orders)
    print('order_id:' + str(orders[len_orders - 1]['id']))  ##注意顺序与网站是相反的
    print('order_price:' + str(orders[len_orders - 1]['price']))
    print('order_mode:' + str(order_mode))
    print('order_amount:' + str(orders[len_orders - 1]['amount']))
    print('order_symbol:' + str(order_symbol))

    ############################################################################
    #######################N0.5获取交易记录#######################################
    print("-------------------------------获取交易记录-----------------------")
    # 获取trade orders

    print("OK")
    # print(len(open_orders))
    # print(open_orders[len(open_orders)-1])
    #######################Control Logical######################################
    print("-------------------------------控制逻辑-----------------------")
    if abs(percentChange) > 3:
        if percentChange < 0.0:  # 行情下降
            if ltc_free > 0.28 and percentChange < buy_down_percent:  # 3 保底售出 order_mount=表示当前订单量 order_mode 表示当前订单是买入还是卖出
                print("Sell to stop lose！！！")
                new_order = gateio.create_order(symbol='LTC/USDT', type='limit', side='sell', amount=ltc_free,
                                                price=last)  ##注意价格哦 sell是卖出 卖出量是ltc_free
            elif usdt_free > 1.0 and ltc_free < 1.0:  # 若是当前订单为卖出，且不是LTC交易币，则买入
                print("Buy!!")
                amount_temp = (usdt_free / last) * (limit_amount / 100)  # 计算本次ltc amount交易量
                new_order = gateio.create_order(symbol='LTC/USDT', type='limit', side='buy', amount=0.3,
                                                price=last)  ##注意价格哦 sell是卖出
        elif percentChange > 0.0:  # 行情上升
            if ltc_free > 0.28 and percentChange > sell_up_percent:  # 若ltc_free里面有数值，则表明有存量，则挂单卖出
                print("Sell to earn!!!!")
                new_order = gateio.create_order(symbol='LTC/USDT', type='limit', side='sell', amount=ltc_free,
                                                price=last)  ##注意价格哦 sell是卖出 卖出量是ltc_free
            elif usdt_free > 1.0 and ltc_free < 1.0:  # 若行情上升则买入
                print("Buy!!")
                amount_temp = (usdt_free / last) * (limit_amount / 100)  # 计算本次ltc amount交易量
                new_order = gateio.create_order(symbol='LTC/USDT', type='limit', side='buy', amount=0.3,
                                                price=last)  ##注意价格哦 sell是
    else:
        print("Nothing to do !!!!!!!!!!")
    time.sleep(2)
    print("OK!")
    print("-------------------------------完成-----------------------")
    #####创建订单##########
    # new_order = gateio.create_order(symbol='LTC/USDT', type='limit', side='buy', amount=0.085, price=43.02)##注意价格哦 sell是卖出
    # print(new_order)

    #####取消订单##########
    # delete_order=gateio.cancel_order(id='', symbol='LTC/USDT')
    # print(delete_order)
    if i % 10 == 0:
        os.system('cls')
