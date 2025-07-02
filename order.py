import requests

def place_regular_order(tradingsecurity, exchange, transaction_type, order_type, quantity, validity, price, product, authorization_token):
    url = "https://wss1.mtsp.co.in:15207/orders/regular"

    payload = {
        "tradingsecurity": tradingsecurity,
        "exchange": exchange,
        "transaction_type": transaction_type,
        "order_type": order_type,
        "quantity": quantity,
        "validity": validity,
        "price": price,
        "product": product
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Api-Version": "3",
        "Authorization": authorization_token
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()
