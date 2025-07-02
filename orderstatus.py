import requests

def get_order_status(authorization_token):
    url = "https://wss1.mtsp.co.in:15207/orders"

    headers = {
        "Api-Version": "3",
        "Authorization": authorization_token
    }

    response = requests.get(url, headers=headers)
    return response.json()
