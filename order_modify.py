import requests

url = "https://wss1.mtsp.co.in:15207/orders/regular/128439"

payload = {
  "order_type": "MARKET",
  "quantity": "5",
  "validity": "DAY",
  "price": "830"
}

headers = {
  "Content-Type": "application/x-www-form-urlencoded",
  "Api-Version": "3",
  "Authorization": "API_KEY:REQUEST_TOKEN"
}

response = requests.put(url, data=payload, headers=headers)

data = response.json()
print(data)
