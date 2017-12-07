# create function for getting the price of
#   Volume, price_usd

import requests
import inflect


p = inflect.engine()

#name1 = raw_input("Enter the name of the currency")

def Coin(name):
    return requests.get("https://api.coinmarketcap.com/v1/ticker/" + name).json()

#data = Coin("bitcoin")[0]

#print data

#print p.ordinal(data["rank"])
# Return the rank of the currency compared to all the other currencies.


# change the numbers inputted to text
def numberToWords(num):
    to19 = 'One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve ' \
           'Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen'.split()
    tens = 'Twenty Thirty Forty Fifty Sixty Seventy Eighty Ninety'.split()
    def words(n):
        if n < 20:
            return to19[n-1:n]
        if n < 100:
            return [tens[n/10-2]] + words(n%10)
        if n < 1000:
            return [to19[n/100-1]] + ['Hundred'] + words(n%100)
        for p, w in enumerate(('Thousand', 'Million', 'Billion'), 1):
            if n < 1000**(p+1):
                return words(n/1000**p) + [w] + words(n%1000**p)
    return ' '.join(words(num)) or 'Zero'


def rank(data):
    currency = data
    data = Coin(data)[0]
    return str(currency + " is currently the "+p.ordinal(data["rank"]) + " ranked currency on the market.")
print rank("Bitcoin")


def price_usd(data):
    currency = data
    data = Coin(data)[0]
    return "The price of "+currency + " in US dollars is "+ numberToWords(int(data["price_usd"].split(".")[0])) + " dollars."
print price_usd("bitcoin")

def market_cap_usd(data):
    currency = data
    data = Coin(data)[0]
    return "The market cap for "+currency+" is "+ numberToWords(int(data["24h_volume_usd"].split(".")[0]))+ " dollars."
print market_cap_usd("ethereum")


def h24_volume_usd(data):
    currency = data
    data = Coin(data)[0]
    return "The market 24 hour volume of "+currency+" is "+ numberToWords(int(data["24h_volume_usd"].split(".")[0]))+ " dollars."
print h24_volume_usd("bitcoin")

def percent_change_7d(data):
    currency = data
    data = Coin(data)[0]
    return "The seven day percent change for "+currency+" is "+ data["percent_change_7d"] + " percent."
print percent_change_7d("bitcoin")

def symbol(data):
    currency = data
    data = Coin(data)[0]
    symbol = list(data["symbol"])
    return "The symbol of "+currency+" is "+" ".join(symbol)
print symbol("bitcoin")

def max_supply(data):
    currency = data
    data = Coin(data)[0]
    return "The max supply of "+currency+" is "+ numberToWords(int(data["max_supply"].split(".")[0]))+ " dollars."
print max_supply("bitcoin")


def percent_change_1h(data):
    currency = data
    data = Coin(data)[0]
    return "The one hour percent change for "+currency+" is "+data["percent_change_1h"]\
           + " percent."
print percent_change_1h("bitcoin")

def total_supply(data):
    currency = data
    data = Coin(data)[0]
    return "The total supply of "+currency+" is "+numberToWords(int(data["total_supply"].split(".")[0])) \
           +" coins."
print total_supply("bitcoin")

# def price_btc():
#     return data["price_btc"]
# print price_btc()
#
def available_supply(data):
    currency = data
    data = Coin(data)[0]
    return "The total supply of "+currency+" in the market is "+numberToWords(int(data["available_supply"].split(".")[0])) \
           +" coins."
print available_supply("bitcoin")

def percent_change_24h(data):
    currency = data
    data = Coin(data)[0]
    return "The twenty four hour percent change for "+currency+" is "+data["percent_change_24h"] + " percent."
print percent_change_24h("bitcoin")

