import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://wss1.mtsp.co.in:15207/connect/login"

payload = {
  "api_key": "ijTLVhyDdou1iyK5MLnJmyAwT",
  "api_secrets": "QrRH7NxkphBg6Z#|eIsjRN<8"
}

headers = {
  "Content-Type": "application/x-www-form-urlencoded",
  "Api-Version": "3"
}

response = requests.post(url, data=payload, headers=headers, verify=False)

print("Status Code:", response.status_code)
print("Response Text:", response.text)

try:
    data = response.json()
    print("JSON Response:", data)
except Exception as e:
    print("Error parsing JSON:", e)
