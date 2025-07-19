import requests

url = "https://wss1.multitrade.tech:15207/trades/2920"

payload={}
headers = {
  'Api-Version': '3',
  'Authorization': 'API_KEY:REQUEST_TOKEN'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
