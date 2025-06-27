import requests

url = "https://wss1.mtsp.co.in:15207/orders/regular/22"

payload={}
headers = {
  'Api-Version': '3',
  'Authorization': 'ijTLVhyDdou1iyK5MLnJmyAwT:T>k53|N3WBtb*bT.415%'
}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)
