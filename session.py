import requests
url = "https://wss1.mtsp.co.in:15207/session/token"
headers = {
  "Api-Version": "3",
  "Authorization": "ijTLVhyDdou1iyK5MLnJmyAwT:T>k53|N3WBtb*bT.415%"
}
response = requests.get(url, headers=headers)
data = response.json()
print(data)
