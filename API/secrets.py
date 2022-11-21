import api
import requests
from requests import Session
from pprint import pprint as pp

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api.API_KEY,
}
r = requests.get(url, headers = headers)
# print(r.json())

class GetInfo:
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': token,}
        self.session = Session()
        self.session.headers.update(self.headers)

    def GetAllCoins(self):
        url= self.apiurl + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data']
        return data

    def GetPrice(self, symbol):
        url= self.apiurl + '/v1/cryptocurrency/quotes/latest'
        param = {'symbol': symbol}
        r = self.session.get(url, params=param)
        data = r.json()['data']
        return data

info = GetInfo(api.API_KEY)

# print(pp(info.GetAllCoins()))

print(pp(info.GetPrice('ETH')))