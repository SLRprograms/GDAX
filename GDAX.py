# Requires python-requests. Install with pip:
#
#   pip install requests
#
# or, with easy-install:
#
#   easy_install requests
import datetime
import urllib
import ast

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
    
api_url = 'https://api.gdax.com/'
API_KEY = ''
API_SECRET = ''
API_PASS = ''
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

# Get accounts
#r = requests.get(api_url + 'accounts', auth=auth)
#print r.json()
# [{"id": "a1b2c3d4", "balance":...
def Fills():#grabs past 100 fills
    while True:
        try:
            r = requests.get(api_url + 'fills', auth=auth)
            return r.json()
        except:
            print 'fill FAILED'
            time.sleep(1)
def BTCUSDBid():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/book', auth=auth)
            return float(r.json()['bids'][0][0])
        except:
            print 'bid FAILED'
def BTCUSDAsk():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/book', auth=auth)
            return float(r.json()['asks'][0][0])
        except:
            print 'ask FAILED'
def Worth():
    try:
        worth = 0.0
        r = requests.get(api_url + 'accounts', auth=auth)
        for i in r.json():
            #print i['currency']
            if i['currency'] == 'USD':
                worth = worth + float(i['balance'])
            elif float(i['balance']) > 0.0:
                worth = worth + (BTCUSDAsk()*(float(i['balance'])))
        return worth
    except:
        print 'worth FAILED.'
def WorthForSell(initWorth):
    try:
        worth = 0.0
        r = requests.get(api_url + 'accounts', auth=auth)
        for i in r.json():
            #print i['currency']
            if i['currency'] == 'USD':
                worth = worth + float(i['balance'])
            elif float(i['balance']) > 0.0:
                worth = worth + (BTCUSDAsk()*(float(i['balance'])))
        if worth == 'None':
            print 'worth FAILED 2.'
            return initWorth
        return worth
    except:
        print 'worth FAILED.'
        return initWorth
    #return float(r.json()[3]['balance'])
# Place an order
def TickAndVolume():
    info = [0.0,0.0]
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/ticker', auth=auth)
            info[0] = float(r.json()['price'])
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            info[1] = (float(r.json()[1][5])+float(r.json()[0][5]))/2.0
            return info
        except:
            print 'tickAndVolume FAILED'
            time.sleep(1)
def Tick():
    while True:
        try:
            r = requests.get(api_url + 'products/LTC-BTC/ticker', auth=auth)
            return float(r.json()['price'])
        except:
            print 'FAILED tick.'
            time.sleep(1)
def Amount():
    while True:
        try:
            r = requests.get(api_url + 'accounts', auth=auth)
            for i in r.json():
                #print i['currency']
                if i['currency'] == 'BTC':
                    return float(i['balance'])
            #return float(r.json()[3]['balance'])
        except:
            print 'amount FAILED'
            time.sleep(1)
def LitecoinAmount():
    try:
        r = requests.get(api_url + 'accounts', auth=auth)
        for i in r.json():
            #print i['currency']
            if i['currency'] == 'LTC':
                return float(i['balance'])
        #return float(r.json()[3]['balance'])
    except:
        print 'FAILED amount.'
        time.sleep(1)
def BuyIsActive():
    while True:
        try:
            r = requests.get(api_url + 'orders', auth=auth)
            for i in range(0,len(r.json())):
                if r.json()[i]['side'] == 'buy':
                    return True
            return False
        except:
            print 'buyIsActive FAILED'
            time.sleep(1)
def SellIsActive():
    while True:
        try:
            r = requests.get(api_url + 'orders', auth=auth)
            for i in range(0,len(r.json())):
                if r.json()[i]['side'] == 'sell':
                    return True
            return False
        except:
            print 'active FAILED.'
            time.sleep(1)
def BitcoinActive():
    try:
        r = requests.get(api_url + 'orders', auth=auth)
        for i in r.json():
            return True
    except:
        print 'FAILED active.'
        return False
def ActivateOne():
    try:
        r = requests.get(api_url + 'orders', auth=auth)
        for i in r.json():
            if float(i['price']) == 1.0:
                return True
        return False
    except:
        print 'FAILED Activate.'
        return False
def ActivateTwo():
    try:
        r = requests.get(api_url + 'orders', auth=auth)
        for i in r.json():
            if float(i['price']) == 2.0:
                return True
        return False
    except:
        print 'FAILED Activate.'
        return False
def ActivateThree():
    try:
        r = requests.get(api_url + 'orders', auth=auth)
        for i in r.json():
            if float(i['price']) == 3.0:
                return True
        return False
    except:
        print 'FAILED Activate.'
        return False
def DisActivate():
    try:
        r = requests.get(api_url + 'orders', auth=auth)
        for i in r.json():
            if float(i['price']) == 4.0:
                return True
        return False
    except:
        print 'FAILED Activate.'
        return False
def Buy(size):
    try:
        order = {
            'size': size,
            'price': BTCUSDBid(),
            'post_only': True,
            'time_in_force' : 'GTT',
            'cancel_after' : 'hour',
            'side': 'buy',
            'product_id': 'BTC-USD',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        print r.json()
    except:
        print 'buy FAILED'
def Sell(size):
    try:
        order = {
            'size': size,
            'price': BTCUSDAsk(),
            'post_only': True,
            'time_in_force' : 'GTT',
            'cancel_after' : 'hour',
            'side': 'sell',
            'product_id': 'BTC-USD',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        print r.json()
    except:
        print 'sell FAILED'
def LitecoinSell(size,price):
    try:
        order = {
            'size': size,
            'price': price,
            'post_only': True,
            'side': 'sell',
            'product_id': 'LTC-USD',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        print r.json()
    except:
        print 'damn litecoin sell'
def LitecoinBuy(size,price):
    try:
        order = {
            'size': size,
            'price': price,
            'post_only': True,
            'side': 'buy',
            'product_id': 'LTC-USD',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        print r.json()
    except:
        print 'damn litecoin buy'        
def LTCtoBTCSell(size,price):
    try:
        order = {
            'size': size,
            'price': price,
            'post_only': False,
            'side': 'sell',
            'product_id': 'LTC-BTC',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        print r.json()
    except:
        print 'damn ltc to btc sell'
def LTCtoBTCBuy(size,price):
    try:
        order = {
            'size': size,
            'price': price,
            'post_only': False,
            'side': 'buy',
            'product_id': 'LTC-BTC',
        }
        r = requests.post(api_url + 'orders', json=order, auth=auth)
        print r.json()
    except:
        print 'damn ltc to btc buy'
def ForceSell():
    while True:
        try:
            tick = Tick()
            order = {
                'size': Amount(),
                'price': round(tick-(tick*0.01),2),
                'post_only': False,
                'side': 'sell',
                'product_id': 'BTC-USD',
            }
            r = requests.post(api_url + 'orders', json=order, auth=auth)
            return r.json()
        except:
            print 'forceSell FAILED'
            time.sleep(3)
def ForceBuy(size):
    tick = BitcoinTick()
    order = {
        'size': size,
        'price': round(tick+(tick*0.01),2),
        'post_only': False,
        'side': 'buy',
        'product_id': 'BTC-USD',
    }
    r = requests.post(api_url + 'orders', json=order, auth=auth)
    print r.json()
def Target():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            sumMA=0.0
            for i in range(0,200):
                sumMA=float(r.json()[i][1]) + sumMA
            sumMA = sumMA/200.0
            return sumMA
        except:
            print 'target FAILED.'
            time.sleep(1)
def BitcoinFastMA():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            sumMA=0.0
            for i in range(0,10):
                sumMA=float(r.json()[i][4]) + sumMA
            sumMA = sumMA/10.0
            print 'fast: '+str(sumMA)
            return sumMA
        except:
            print 'failed MA.'
            time.sleep(5)
def TimeISO():
    r = requests.get(api_url + 'time', auth=auth)
    return r.json()['iso']
def TimeEpoch():
    r = requests.get(api_url + 'time', auth=auth)
    return r.json()['epoch']
def GrabPast(granularity,candleVar):
    #time = 0
    #low = 1
    #high = 2
    #open = 3
    #close = 4
    #volume = 5
    depth = 300
    unit = 60
    timeEpoch = TimeEpoch()
    print 'timeEpoch: '+str(timeEpoch)
    end = datetime.datetime.utcfromtimestamp(timeEpoch).isoformat()
    end = end.strip('.000')
    end = end + 'Z'
    remove = (float(granularity)*float(depth))
    start = float(timeEpoch)-remove
    start = datetime.datetime.utcfromtimestamp(start).isoformat()
    start = start.strip('.000')
    start = start + 'Z'
    #start = '2017-12-15T00:27:52.233Z'
    #end = '2017-12-21T22:17:52.233Z'
    intro = 'https://api.gdax.com/products/BTC-USD/candles?'
    start = str(start)+'&'
    end = str(end)+'&'
    gran = 'granularity='+str(granularity)
    f = urllib.urlopen(intro + start + end + gran)
    print 'start: '+str(start)
    print 'end: '+str(end)
    count = 0
    _list = ast.literal_eval(f.read())
    var = []
    varNum = 0
    if candleVar == 'time':
        varNum = 0
    elif candleVar == 'low':
        varNum = 1
    elif candleVar == 'high':
        varNum = 2
    elif candleVar == 'open':
        varNum = 3
    elif candleVar == 'close':
        varNum = 4
    elif candleVar == 'volume':
        varNum = 5
    while True:
        try:
            var.insert(len(var),float(_list[count][varNum]))
            count += 1
        except:
            count -= 1
            return var
#print GrabPast(60,'close')
def Past(depth):#depth = 1-300
    CLOSE = []#3
    for i in range(0,depth):
        CLOSE.insert(len(CLOSE),0.0)
    while True:
        try:    
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            print int(r.json()[0][0])-int(timeEpoch)
            for i in range(0,depth):
                CLOSE[i] = float(r.json()[i][4])
            return CLOSE
        except:
            print 'failed MA.'
            time.sleep(1)
def BitcoinPrices():
    candles = BitcoinPast(300)
    delta = []
    for i in range(1,len(candles[2])):
        delta.insert(len(delta),candles[3][i-1])
    return delta
def BitcoinPriceDelta():
    candles = BitcoinPast(300)
    delta = []
    for i in range(1,len(candles[2])):
        delta.insert(len(delta),candles[3][i-1] - candles[3][i])
    return delta
def BitcoinVolumeDelta():
    candles = BitcoinPast(300)
    delta = []
    for i in range(1,len(candles[4])):
        delta.insert(len(delta),candles[4][i-1] - candles[4][i])
    return delta
def BitcoinDoubleReds():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,2):
                if float(r.json()[i][4]) < float(r.json()[i+1][4]):
                    if float(r.json()[i+1][4]) < float(r.json()[i+2][4]):
                        return True
            return False
        except:
            print 'failed DoubleRed.'
def BitcoinTrippleReds():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,2):
                if float(r.json()[i][4]) < float(r.json()[i+1][4]):
                    if float(r.json()[i+1][4]) < float(r.json()[i+2][4]):
                        if float(r.json()[i+2][4]) < float(r.json()[i+3][4]):
                            return True
            return False
        except:
            print 'failed DoubleRed.'
def BitcoinMostRed():
    while True:
        green = 0
        red = 0
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,20):
                if float(r.json()[i][4]) < float(r.json()[i+1][4]):
                    red = red + 1
                else:
                    green = green + 1
            print red
            if red > 12:
                print 'most red'
                return True
            else:
                return False
        except:
            print 'failed DoubleRed.'
def BitcoinSingleRed():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,1):
                if float(r.json()[i][4]) < float(r.json()[i+1][4]):
                        return True
            return False
        except:
            print 'failed DoubleRed.'
def BitcoinIncreasedVolume():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,1):
                if float(r.json()[i][5]) > float(r.json()[i+1][5]):
                    return True
            return False
        except:
            print 'failed DoubleRed.'
def BitcoinDecreasedVolume():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,1):
                if float(r.json()[i][5]) < float(r.json()[i+1][5]):
                    return True
            return False
        except:
            print 'failed DoubleRed.'
def BitcoinOverOneOfFive():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,5):
                if float(r.json()[i][4]) > float(r.json()[i+1][4]) or float(r.json()[i][4]) > float(r.json()[i+2][4]) or float(r.json()[i][4]) > float(r.json()[i+3][4]) or float(r.json()[i][4]) > float(r.json()[i+4][4]) or float(r.json()[i][4]) > float(r.json()[i+5][4]):
                    print 'was over.'
                    return True
            return False
        except:
            print 'failed ThreeRed.'
def BitcoinThreeGreens():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/candles', auth=auth)
            for i in range(0,1):
                if float(r.json()[i][4]) > float(r.json()[i+1][4]):
                    return True
            return False
        except:
            print 'failed ThreeGreen.'
def BitcoinCancel():
    try:
        r = requests.delete(api_url + 'orders', auth=auth)
        print 'SUCCESS cancel'
    except:
        print 'FAILED cancel.'
#print r.json()
# {"id": "0428b97b-bec1-429e-a94c-59992926778d"}
def ETHUSDBid():
    while True:
        try:
            r = requests.get(api_url + 'products/ETH-USD/book', auth=auth)
            return float(r.json()['bids'][0][0])
        except:
            print 'bid FAILED'
def ETHUSDAsk():
    while True:
        try:
            r = requests.get(api_url + 'products/ETH-USD/book', auth=auth)
            return float(r.json()['asks'][0][0])
        except:
            print 'ask FAILED'
def ETHBTCBid():
    while True:
        try:
            r = requests.get(api_url + 'products/ETH-BTC/book', auth=auth)
            return float(r.json()['bids'][0][0])
        except:
            print 'bid FAILED'
def ETHBTCAsk():
    while True:
        try:
            r = requests.get(api_url + 'products/ETH-BTC/book', auth=auth)
            return float(r.json()['asks'][0][0])
        except:
            print 'ask FAILED'
def LTCBTCBid():
    while True:
        try:
            r = requests.get(api_url + 'products/LTC-BTC/book', auth=auth)
            return float(r.json()['bids'][0][0])
        except:
            print 'bid FAILED'
def LTCBTCAsk():
    while True:
        try:
            r = requests.get(api_url + 'products/LTC-BTC/book', auth=auth)
            return float(r.json()['asks'][0][0])
        except:
            print 'ask FAILED'
def LTCUSDBid():
    while True:
        try:
            r = requests.get(api_url + 'products/LTC-USD/book', auth=auth)
            return float(r.json()['bids'][0][0])
        except:
            print 'bid FAILED'
def LTCUSDAsk():
    while True:
        try:
            r = requests.get(api_url + 'products/LTC-USD/book', auth=auth)
            return float(r.json()['asks'][0][0])
        except:
            print 'ask FAILED'
def BCHBTCBid():
    while True:
        try:
            r = requests.get(api_url + 'products/BCH-BTC/book', auth=auth)
            return float(r.json()['bids'][0][0])
        except:
            print 'bid FAILED'
def BCHBTCAsk():
    while True:
        try:
            r = requests.get(api_url + 'products/BCH-BTC/book', auth=auth)
            return float(r.json()['asks'][0][0])
        except:
            print 'ask FAILED'
def BCHUSDBid():
    while True:
        try:
            r = requests.get(api_url + 'products/BCH-USD/book', auth=auth)
            return float(r.json()['bids'][0][0])
        except:
            print 'bid FAILED'
def BCHUSDAsk():
    while True:
        try:
            r = requests.get(api_url + 'products/BCH-USD/book', auth=auth)
            return float(r.json()['asks'][0][0])
        except:
            print 'ask FAILED'
def Volume():
    while True:
        try:
            r = requests.get(api_url + 'products/BTC-USD/ticker', auth=auth)
            return float(r.json()['volume'])
        except:
            print 'Volume FAILED'
            time.sleep(1)
def BitcoinMatchedPrice(price):#takes in Buy or Sell, Spits out prices.
    while True:
        try:
            r = requests.get(api_url + 'orders', auth=auth)
            for i in range(0,len(r.json())):
                if float(r.json()[i]['price']) == price:
                    return True
            return False
        except:
            print 'ask FAILED'
            time.sleep(10)
