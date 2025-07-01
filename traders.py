import requests
import time
import json
from datetime import datetime
import random

# Configuration
API_KEY = "ijTLVhyDdou1iyK5MLnJmyAwT"
BASE_URL = "https://wss1.mtsp.co.in:15207"

# Valid securities (update with your actual valid security IDs)
VALID_REGULAR_SECURITIES = {
    "NSECM": ["3045", "1333", "2475"],  # NSE Cash Market securities
    "BSECM": ["500112", "500325"]       # BSE Cash Market securities
}

VALID_SLBM_SECURITIES = ["150013", "150014"]  # NSESLBM securities

def get_auth_token():
    """Load authentication token from token.json"""
    try:
        with open('token.json', 'r') as f:
            token_data = json.load(f)
            return f"{API_KEY}:{token_data['data']['request_token']}"
    except Exception as e:
        raise Exception(f"Failed to load token: {str(e)}")

def generate_regular_order():
    """Generate parameters for regular order"""
    exchange = random.choice(["NSECM", "BSECM"])
    return {
        "tradingsecurity": random.choice(VALID_REGULAR_SECURITIES[exchange]),
        "exchange": exchange,
        "transaction_type": random.choice(["BUY", "SELL"]),
        "order_type": random.choice(["MARKET", "LIMIT"]),
        "quantity": str(random.randint(1, 20)),
        "validity": "DAY",
        "price": str(round(random.uniform(100, 1000), 2)),
        "product": "CNC",
        "userid": "DAPI1"
    }

def generate_slbm_order():
    """Generate parameters for SLBM order"""
    return {
        "tradingsecurity": random.choice(VALID_SLBM_SECURITIES),
        "exchange": "NSESLBM",
        "transaction_type": random.choice(["BUY", "SELL"]),
        "order_type": random.choice(["MARKET", "LIMIT"]),
        "quantity": str(random.randint(1, 15)),
        "validity": "DAY",
        "price": str(round(random.uniform(100, 1000), 2)),
        "product": "NRML",
        "open_close": "Borrow" if random.random() > 0.5 else "Lend",
        "userid": "DAPI1"
    }

def place_order(order_type, auth_token):
    """Place an order with proper error handling"""
    if order_type == "REGULAR":
        url = f"{BASE_URL}/orders/regular"
        payload = generate_regular_order()
    else:  # SLBM
        url = f"{BASE_URL}/orders/regular"
        payload = generate_slbm_order()
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Api-Version": "3",
        "Authorization": auth_token
    }
    
    try:
        print(f"\nPlacing {order_type} order:", {k:v for k,v in payload.items() if k != 'userid'})
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and data.get('status') == 'successful':
            print("Order successful!")
            return True
        else:
            error = data.get('data', {}).get('error', 'Unknown error')
            print(f"Order failed: {error}")
            return False
            
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return False

def save_order_status(auth_token):
    """Save current order status to file"""
    try:
        response = requests.get(
            f"{BASE_URL}/orders",
            headers={"Authorization": auth_token, "Api-Version": "3"},
            timeout=10
        )
        with open('order_status.json', 'w') as f:
            json.dump(response.json(), f, indent=2)
        print("Order status saved")
    except Exception as e:
        print(f"Failed to save order status: {str(e)}")

def main():
    print("Starting trading bot with proper exchange handling")
    
    try:
        auth_token = get_auth_token()
        
        while True:
            print("\n" + "="*50)
            print(f"Cycle started at {datetime.now().strftime('%H:%M:%S')}")
            
            # Place regular order
            place_order("REGULAR", auth_token)
            time.sleep(60)  # Wait 1 minute
            
            # Place SLBM order
            place_order("SLBM", auth_token)
            time.sleep(60)  # Wait 1 minute
            
            # Save order status
            save_order_status(auth_token)
            
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")

if __name__ == "__main__":
    main()