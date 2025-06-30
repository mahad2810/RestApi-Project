import requests

url = "https://wss1.mtsp.co.in:15207/orders/regular"

payload = {
  "tradingsecurity": "3045",
  "exchange": "NSECM",
  "transaction_type": "BUY",
  "order_type": "LIMIT",
  "quantity": "10",
  "validity": "DAY",
  "price": "830",
  "product": "CNC"
}

headers = {
  "Content-Type": "application/x-www-form-urlencoded",
  "Api-Version": "3",
  "Authorization": "ijTLVhyDdou1iyK5MLnJmyAwT:T>k53|N3WBtb*bT.415%"
}

response = requests.post(url, data=payload, headers=headers)

data = response.json()
print(data)
