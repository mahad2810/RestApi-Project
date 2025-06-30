import requests

url = "https://wss1.mtsp.co.in:15207/orders/regular"

payload = {
  "tradingsecurity": "150013",
  "exchange": "NSESLBM",
  "transaction_type": "SELL",
  "order_type": "LIMIT",
  "quantity": "8",
  "validity": "DAY",
  "price": "800",
  "product": "NRML",
  "open_close":"Lend",
  "userid":"DAPI1"
}

headers = {
  "Content-Type": "application/x-www-form-urlencoded",
  "Api-Version": "3",
  "Authorization": "ijTLVhyDdou1iyK5MLnJmyAwT:T>k53|N3WBtb*bT.415%"
}

response = requests.post(url, data=payload, headers=headers)

data = response.json()
print(data)
