import requests

url = "https://wss1.mtsp.co.in:15207/connect/login"

payload = {
  "api_key": "ijTLVhyDdou1iyK5MLnJmyAwT",
  "api_secrets": "QrRH7NxkphBg6Z#|eIsjRN<8"
}

headers = {
  "Content-Type": "application/x-www-form-urlencoded",
  "Api-Version": "3"
}

response = requests.post(url, data=payload, headers=headers)

data = response.json()
print(data)
