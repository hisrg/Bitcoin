from __future__ import print_function
import gate_api
from gate_api.rest import ApiException

configuration = gate_api.Configuration()
# APIV4
configuration.key = 'your gateio key'
configuration.secret = 'your gateio secret'
##########################################################获取账户信息################################################################
print("*" * 50 + "获取该账户的LTC信息" + 50 * "*")
# create an instance of the API class
api_instance = gate_api.SpotApi(gate_api.ApiClient(configuration))
currency = 'LTC'  # str | Retrieved specified currency related data (optional)

try:
    # List spot accounts
    api_response = api_instance.list_spot_accounts(currency=currency)
    print(api_response)
except ApiException as e:
    print("Exception when calling SpotApi->list_spot_accounts: %s\n" % e)
print("*" * 50 + "获取该账户的USDT信息" + 50 * "*")
# create an instance of the API class
api_instance = gate_api.SpotApi(gate_api.ApiClient(configuration))
currency = 'USDT'  # str | Retrieved specified currency related data (optional)

try:
    # List spot accounts
    api_response = api_instance.list_spot_accounts(currency=currency)
    print(api_response)
except ApiException as e:
    print("Exception when calling SpotApi->list_spot_accounts: %s\n" % e)

# create an instance of the API class
##########################################################获取交易记录 API################################################################
print("*" * 50 + "获取交易记录" + 50 * "*")
api_instance = gate_api.SpotApi(gate_api.ApiClient(configuration))
currency_pair = 'LTC_USDT'  # str | Currency pair
limit = 1  # int | Maximum number of record returned in one list (optional) (default to 100)
page = 1  # int | Page number (optional) (default to 1)
order_id = '12345'  # str | List all trades of specified order (optional)

try:
    # List personal trading history
    api_response = api_instance.list_my_trades(currency_pair, limit=limit, page=page)
    print(api_response)
except ApiException as e:
    print("Exception when calling SpotApi->list_my_trades: %s\n" % e)
#########################################################获取订单#######################################################################
print("*" * 50 + "获取订单" + 50 * "*")
# create an instance of the API class
api_instance = gate_api.SpotApi(gate_api.ApiClient(configuration))
currency_pair = 'LTC_USDT'  # str | Currency pair
status = 'open'  # str | List orders based on status  `open` - order is waiting to be filled `finished` - order has been filled or cancelled
page = 1  # int | Page number (optional) (default to 1)
limit = 100  # int | Maximum number of record returned in one list (optional) (default to 100)

try:
    # List orders
    api_response = api_instance.list_orders(currency_pair, status, page=page, limit=limit)
    print(api_response)
except ApiException as e:
    print("Exception when calling SpotApi->list_orders: %s\n" % e)
#######################################################get_currency_pair#############################################################
print("*" * 50 + "get_currency_pair" + 50 * "*")
# create an instance of the API class
# create an instance of the API class
api_instance = gate_api.SpotApi()
currency_pair = 'LTC_USDT'  # str | Currency pair
try:
    # Get detail of one single order
    api_response = api_instance.get_currency_pair(currency_pair)
    print(api_response)
except ApiException as e:
    print("Exception when calling SpotApi->get_currency_pair: %s\n" % e)
######################################################创建订单################################################################
# print("*" * 50 + "创建订单" + 50 * "*")
# # create an instance of the API class
# api_instance = gate_api.SpotApi(gate_api.ApiClient(configuration))
# order = gate_api.Order(currency_pair=currency_pair, side='sell', amount=0.30, account='spot', price=40.72,
#                        type='limit')  # Order | #卖出
#
# try:
#     # Create an order
#     api_response = api_instance.create_order(order)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling SpotApi->create_order: %s\n" % e)
######################################################取消订单################################################################
# print("*" * 50 + "取消订单" + 50 * "*")
# api_instance = gate_api.SpotApi(gate_api.ApiClient(configuration))
# order_id = '12345' # str | ID returned on order successfully being created
# currency_pair = 'LTC_USDT' # str | Currency pair
#
# try:
#     # Cancel a single order
#     api_response = api_instance.cancel_order(order_id, currency_pair)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling SpotApi->cancel_order: %s\n" % e)
######################################################获取LTC 行情################################################################
# create an instance of the API class
print("*" * 50 + "获取LTC 行情" + 50 * "*")
api_instance = gate_api.SpotApi()
currency_pair = 'LTC_USDT'  # str | Currency pair (optional)

try:
    # Retrieve ticker information
    api_response = api_instance.list_tickers(currency_pair=currency_pair)
    print(api_response)
    if api_response:
        temp = dict(api_response[0].to_dict())
        high24hr = float(temp['high_24h'])
        highest_bid = float(temp['highest_bid'])
        last = float(temp['last'])
        low24hr = float(temp['low_24h'])
        lowest_ask = float(temp['lowest_ask'])
        print("lowest_ask:" + str(lowest_ask))
        print("highest_bid:" + str())
except ApiException as e:
    print("Exception when calling SpotApi->list_tickers: %s\n" % e)
