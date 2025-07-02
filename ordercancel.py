import requests

def delete_order(order_id, authorization_token):
    """
    Deletes a regular order by ID using the provided API endpoint.

    Args:
        order_id (int or str): The ID of the order to delete.
        authorization_token (str): The authorization token in the format 'key:secret'.

    Returns:
        str: The response text from the server.
    """
    url = f"https://wss1.mtsp.co.in:15207/orders/regular/{order_id}"

    headers = {
        'Api-Version': '3',
        'Authorization': authorization_token
    }

    print(f"[delete_order] Sending DELETE request to: {url}")
    print(f"[delete_order] Headers: {headers}")

    response = requests.request("DELETE", url, headers=headers)

    print(f"[delete_order] Status code: {response.status_code}")
    print(f"[delete_order] Response text: {response.text}")

    return response.text
