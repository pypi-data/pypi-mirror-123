# /api/v3/ticker/price

#https://ftx.com/api/markets/BTC/USD

#


import requests
import json
# import telebot
# from telebot import types
# from requests import get


# token = '2086368578:AAH0Ax0MZOhrCBXpnFvFzFVd6IlIWt7YLuE'


# bot = telebot.TeleBot(token)


# def toFixed(numObj, digits=0):
#     return f"{numObj:.{digits}f}"
# @bot.message_handler(commands=['start'])
# def response_send(message):
#     url_binance = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
#     response_binance = requests.get(url_binance)
#     print('BINANCE  :  ', toFixed(float(response_binance.json()['price']), 2 ))
#     str_out = '\nBINANCE  :  ' +  str(toFixed(float(response_binance.json()['price']), 2 ))
#     #type = r1.json()['type']

#     url_coinbase = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
#     response_coinbase = requests.get(url_coinbase)
#     print('COINBASE :  ', response_coinbase.json()['data']['amount'])
#     str_out += '\nCOINBASE :  ' + str(response_coinbase.json()['data']['amount'])

#     url_ftx = 'https://ftx.com/api/markets/BTC/USD'
#     response_ftx = requests.get(url_ftx)
#     print('FTX      :  ', response_ftx.json()['result']['last'])
#     str_out += '\nFTX      :  ' + str(response_ftx.json()['result']['last'])



#     resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=BTCUSD')

#     print('KRAKEN   :  ', toFixed(float(resp.json()['result']['XXBTZUSD']['a'][0]), 2))


#     url_bitstamp = 'https://www.bitstamp.net/api/v2/ticker/btcusd'
#     response_bitstampsp = requests.get(url_bitstamp)
#     str_out += '\nBITSTAMP   :  ' + response_bitstampsp.json()['last']

#     str_out += '\nKRAKEN   :  ' + str(toFixed(float(resp.json()['result']['XXBTZUSD']['a'][0]), 2))


#     bot.send_message(message.from_user.id, f'{str_out}')





# bot.polling()


class Binance():

    def __init__(self, crypto_name, currency):
        self.crypto_name = crypto_name
        self.currency = currency
        return None
        

    def toFixed(self, numObj, digits=0):
        return f"{numObj:.{digits}f}"


    def __str__(self):
        url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
        response = requests.get(url)
        str_out = str(self.toFixed(float(response.json()['price']), 2 ))

        return str(str_out)



class Coinbase():

    def __init__(self, crypto_name, currency):
        self.crypto_name = crypto_name
        self.currency = currency
        return None
        

    def toFixed(self, numObj, digits=0):
        return f"{numObj:.{digits}f}"


    def __str__(self):
        url_coinbase = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
        response = requests.get(url_coinbase)
        str_out = str(response.json()['data']['amount'])

        return str(str_out)


class FTX():

    def __init__(self, crypto_name, currency):
        self.crypto_name = crypto_name
        self.currency = currency
        return None
        

    def toFixed(self, numObj, digits=0):
        return f"{numObj:.{digits}f}"


    def __str__(self):
        url_ftx = 'https://ftx.com/api/markets/BTC/USD'
        response = requests.get(url_ftx)
        str_out = str(response.json()['result']['last'])

        return str(str_out)


class Kraken():

    def __init__(self, crypto_name, currency):
        self.crypto_name = crypto_name
        self.currency = currency
        return None
        

    def toFixed(self, numObj, digits=0):
        return f"{numObj:.{digits}f}"


    def __str__(self):
        resp = requests.get('https://api.kraken.com/0/public/Ticker?pair=BTCUSD')
        str_out = str(self.toFixed(float(resp.json()['result']['XXBTZUSD']['a'][0]), 2))
        return str(str_out)



class BitStamp():

    def __init__(self, crypto_name, currency):
        self.crypto_name = crypto_name
        self.currency = currency
        return None
        

    def toFixed(self, numObj, digits=0):
        return f"{numObj:.{digits}f}"


    def __str__(self):
        url_bitstamp = 'https://www.bitstamp.net/api/v2/ticker/btcusd'
        response = requests.get(url_bitstamp)
        str_out = response.json()['last']
        return str(str_out)