import json
import os
from random import randint, uniform, choice
from datetime import datetime, timedelta

# Function to generate random order data
def generate_order(order_id):
    tradingsymbols = ["SBIN", "INFY", "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK"]
    products = ["CNC", "NRML"]
    transaction_types = ["Buy", "Sell"]
    order_types = ["MARKET", "LIMIT"]
    tags = ["ReferenceTag", "MTS", "Equity"]
    
    tradingsymbol = choice(tradingsymbols)
    transaction_type = choice(transaction_types)
    product = choice(products)
    order_type = choice(order_types)
    tag = choice(tags)
    
    price = round(uniform(500, 3000), 2)
    average_price = round(price - uniform(10, 50), 2)
    trigger_price = round(price - uniform(1, 5), 2) if transaction_type == "Sell" else 0.0
    quantity = randint(1, 20)
    
    order_timestamp = datetime.now() - timedelta(minutes=randint(1, 1440))
    exchange_timestamp = order_timestamp + timedelta(minutes=randint(1, 60))
    
    return {
        "order_id": str(order_id),
        "parent_order_id": str(order_id),
        "exchange_order_id": f"O{randint(10000000, 99999999)}",
        "placed_by": "DAPI1",
        "tradingsymbol": tradingsymbol,
        "exchange": "NSECM",
        "instrument_token": str(randint(1000, 9999)),
        "transaction_type": transaction_type,
        "order_type": order_type,
        "status": "Execute",
        "product": product,
        "validity": "DAY",
        "price": f"{price:.6f}",
        "userid": "DAPI1",
        "quantity": str(quantity),
        "trigger_price": f"{trigger_price:.6f}",
        "average_price": f"{average_price:.6f}",
        "pending_quantity": "0",
        "filled_quantity": str(quantity),
        "disclosed_quantity": "0",
        "market_protection": "0.00",
        "order_timestamp": order_timestamp.strftime("%d/%m/%Y%H:%M:%S"),
        "exchange_timestamp": exchange_timestamp.strftime("%d/%m/%Y%H:%M:%S"),
        "status_message": "",
        "tag": tag
    }

# Generate 15 orders
orders = [generate_order(order_id) for order_id in range(2918, 2933)]

# Wrap in JSON structure
data = {
    "status": "successful",
    "data": orders
}

# Write to a JSON file
with open("orders.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file with 15 orders created successfully!")

# Helper functions for data operations

def load_json_file(file_path):
    """
    Load and parse a JSON file
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

# Helper function to save JSON file
def save_json_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {str(e)}")
        return False

def get_user_data():
    """
    Get user data from user.json
    """
    user_data = load_json_file('user.json')
    if user_data and user_data.get('status') == 'successful':
        return user_data
    return {"status": "error", "message": "Failed to load user data"}

def get_orders_data():
    """
    Get orders data from orders.json
    """
    orders_data = load_json_file('orders.json')
    if orders_data and orders_data.get('status') == 'successful':
        return orders_data
    return {"status": "error", "message": "Failed to load orders data"}

# Function to save orders data
def save_orders_data(orders):
    return save_json_file('orders.json', orders)

def get_user_exchanges():
    """
    Get list of exchanges available to the user
    """
    user_data = get_user_data()
    if user_data.get('status') == 'successful' and 'data' in user_data:
        return user_data['data'].get('exchanges', [])
    return []

def get_user_products():
    """
    Get list of products available to the user
    """
    user_data = get_user_data()
    if user_data.get('status') == 'successful' and 'data' in user_data:
        return user_data['data'].get('products', [])
    return []

def get_user_order_types():
    """
    Get list of order types available to the user
    """
    user_data = get_user_data()
    if user_data.get('status') == 'successful' and 'data' in user_data:
        return user_data['data'].get('order-types', [])
    return []

def get_completed_orders():
    """
    Get list of completed orders
    """
    orders_data = get_orders_data()
    if orders_data.get('status') == 'successful' and 'data' in orders_data:
        return [order for order in orders_data['data'] if order.get('status') == 'Execute']
    return []

def get_pending_orders():
    """
    Get list of pending orders
    """
    orders_data = get_orders_data()
    if orders_data.get('status') == 'successful' and 'data' in orders_data:
        return [order for order in orders_data['data'] if order.get('status') != 'Execute']
    return []

def get_order_by_id(order_id):
    """
    Get order details by order ID
    """
    orders_data = get_orders_data()
    if orders_data.get('status') == 'successful' and 'data' in orders_data:
        for order in orders_data['data']:
            if order.get('order_id') == order_id:
                return order
    return None

# Function to generate random order data (for testing)
def generate_random_orders(count=10):
    exchanges = ['NSE', 'BSE', 'MCX']
    symbols = ['RELIANCE', 'TCS', 'INFY', 'HDFC', 'ICICI', 'SBIN', 'TATAMOTORS', 'WIPRO', 'AXISBANK', 'HCLTECH']
    transaction_types = ['BUY', 'SELL']
    order_types = ['MARKET', 'LIMIT', 'SL', 'SL-M']
    statuses = ['PENDING', 'EXECUTE', 'REJECTED', 'CANCELLED']
    
    orders = []
    for i in range(count):
        # Generate random timestamps within the last 7 days
        order_time = datetime.now() - timedelta(days=random.randint(0, 7), 
                                              hours=random.randint(0, 23), 
                                              minutes=random.randint(0, 59))
        update_time = order_time + timedelta(minutes=random.randint(1, 60))
        
        # Format timestamps as ISO format strings
        order_timestamp = order_time.isoformat()
        update_timestamp = update_time.isoformat()
        
        order = {
            "order_id": f"ORDER{random.randint(10000, 99999)}",
            "tradingsymbol": random.choice(symbols),
            "exchange": random.choice(exchanges),
            "transaction_type": random.choice(transaction_types),
            "order_type": random.choice(order_types),
            "price": round(random.uniform(100, 5000), 2),
            "trigger_price": round(random.uniform(100, 5000), 2),
            "quantity": random.randint(1, 100),
            "status": random.choice(statuses),
            "order_timestamp": order_timestamp,
            "update_timestamp": update_timestamp
        }
        orders.append(order)
    
    return orders

# Function to generate and save random orders
def generate_and_save_random_orders(count=10):
    orders = generate_random_orders(count)
    save_orders_data(orders)
    return orders

# Function to get trades data
def get_trades_data():
    """
    Get trades data from completed orders
    """
    orders_data = get_orders_data()
    trades = []
    
    if orders_data and 'data' in orders_data:
        for order in orders_data['data']:
            if order.get('status', '').upper() == 'EXECUTE':
                # Convert order to trade
                trade = {
                    "trade_id": f"T{order.get('order_id', '').replace('ORDER', '')}",
                    "order_id": order.get('order_id', ''),
                    "tradingsymbol": order.get('tradingsymbol', ''),
                    "exchange": order.get('exchange', ''),
                    "transaction_type": order.get('transaction_type', ''),
                    "product": order.get('product', ''),
                    "quantity": order.get('quantity', 0),
                    "price": order.get('price', 0),
                    "trade_time": order.get('update_timestamp', datetime.now().isoformat())
                }
                trades.append(trade)
    
    return trades

# Function to get positions data
def get_positions_data():
    """
    Get positions data by aggregating trades
    """
    trades = get_trades_data()
    positions = {}
    
    # Group trades by symbol and product
    for trade in trades:
        key = f"{trade['tradingsymbol']}_{trade['exchange']}_{trade['product']}"
        
        if key not in positions:
            positions[key] = {
                "tradingsymbol": trade['tradingsymbol'],
                "exchange": trade['exchange'],
                "product": trade['product'],
                "quantity": 0,
                "average_price": 0,
                "last_price": 0,  # This would come from market data in a real app
                "pnl": 0,
                "day_change": 0,
                "day_change_percentage": 0
            }
        
        # Update position quantity based on transaction type
        quantity = float(trade['quantity'])
        if trade['transaction_type'].upper() == 'BUY':
            positions[key]['quantity'] += quantity
        else:  # SELL
            positions[key]['quantity'] -= quantity
        
        # Update average price (simplified calculation)
        positions[key]['average_price'] = float(trade['price'])
    
    # Calculate PnL and other metrics (simplified)
    for key, position in positions.items():
        # In a real app, you would get the last price from market data
        # For this example, we'll use a random price close to the average price
        position['last_price'] = round(position['average_price'] * (1 + uniform(-0.05, 0.05)), 2)
        
        # Calculate PnL
        position['pnl'] = round((position['last_price'] - position['average_price']) * position['quantity'], 2)
        
        # Calculate day change (simplified)
        position['day_change'] = round(position['last_price'] * uniform(-0.02, 0.02), 2)
        if position['last_price'] > 0:
            position['day_change_percentage'] = round((position['day_change'] / position['last_price']) * 100, 2)
    
    # Convert to list and filter out closed positions
    positions_list = [pos for pos in positions.values() if pos['quantity'] != 0]
    
    return positions_list
