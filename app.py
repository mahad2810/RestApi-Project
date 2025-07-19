from flask import Flask, render_template, jsonify, request
import json
import os
from auth import main as auth_main
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Call the auth.py main function
        auth_main()
        return jsonify({
            'status': 'success',
            'message': 'Login successful'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/user-profile', methods=['GET'])
def get_user_profile():
    try:
        # Check if user.json exists
        if not os.path.exists('user.json'):
            return jsonify({
                'status': 'error',
                'message': 'Please login first'
            }), 400
        
        # Read user data from user.json
        with open('user.json', 'r') as f:
            user_data = json.load(f)
        
        return jsonify(user_data)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        # Load order data from JSON file
        with open('order_status.json', 'r') as file:
            data = json.load(file)
        
        # Get filter parameters
        status_filter = request.args.get('status', 'all')
        date_filter = request.args.get('date', '')
        
        orders = data.get('data', [])
        
        # Process and format orders
        formatted_orders = []
        for order in orders:
            # Parse timestamp
            order_time = order.get('order_timestamp', '')
            try:
                if order_time:
                    # Parse timestamp format: 01/07/202510:11:35
                    dt = datetime.strptime(order_time, '%d/%m/%Y%H:%M:%S')
                    formatted_time = dt.strftime('%I:%M %p')
                    order_date = dt.strftime('%Y-%m-%d')
                else:
                    formatted_time = 'N/A'
                    order_date = ''
            except ValueError:
                formatted_time = 'N/A'
                order_date = ''
            
            # Map status
            status_mapping = {
                'Execute': 'complete',
                'Reject': 'rejected',
                'Pending': 'pending'
            }
            
            original_status = order.get('status', '')
            mapped_status = status_mapping.get(original_status, 'pending').lower()
            
            # Format price
            price = float(order.get('price', 0))
            formatted_price = f"₹{price:,.2f}"
            
            # Create formatted order
            formatted_order = {
                'order_id': f"#ORD{order.get('order_id', '')}",
                'symbol': order.get('tradingsymbol', ''),
                'transaction_type': order.get('transaction_type', '').upper(),
                'quantity': int(order.get('quantity', 0)),
                'price': formatted_price,
                'status': mapped_status,
                'status_display': original_status,
                'time': formatted_time,
                'date': order_date,
                'order_type': order.get('order_type', ''),
                'exchange': order.get('exchange', ''),
                'status_message': order.get('status_message', ''),
                'average_price': float(order.get('average_price', 0)),
                'filled_quantity': int(order.get('filled_quantity', 0)),
                'pending_quantity': int(order.get('pending_quantity', 0))
            }
            
            formatted_orders.append(formatted_order)
        
        # Apply filters
        if status_filter != 'all':
            formatted_orders = [order for order in formatted_orders if order['status'] == status_filter]
        
        if date_filter:
            formatted_orders = [order for order in formatted_orders if order['date'] == date_filter]
        
        # Sort by order_id (newest first)
        formatted_orders.sort(key=lambda x: int(x['order_id'].replace('#ORD', '')), reverse=True)
        
        return jsonify({
            'status': 'success',
            'data': formatted_orders,
            'total': len(formatted_orders)
        })
        
    except FileNotFoundError:
        return jsonify({
            'status': 'error',
            'message': 'Order data file not found'
        }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order_details(order_id):
    try:
        with open('order_status.json', 'r') as file:
            data = json.load(file)
        
        # Find specific order
        order_id_clean = order_id.replace('#ORD', '')
        order = next((o for o in data.get('data', []) if o.get('order_id') == order_id_clean), None)
        
        if not order:
            return jsonify({
                'status': 'error',
                'message': 'Order not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': order
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    


from order import place_regular_order
from orderSLBM import place_slbm_order
from orderstatus import get_order_status

@app.route('/place-order', methods=['POST'])
def place_order():
    data = request.get_json()
    
    # Load your api_key and request_token from token.json
    with open('token.json') as f:
        token_data = json.load(f)
    api_key = "ijTLVhyDdou1iyK5MLnJmyAwT"  # your static API key
    request_token = token_data['data']['request_token']

    
    authorization_token = f"{api_key}:{request_token}"

    # Decide between SLBM and regular
    if data.get("exchange") == "NSESLBM":
        result = place_slbm_order(
            tradingsecurity = data["symbol"],
            exchange = data["exchange"],
            transaction_type = data["transaction"],
            order_type = data["orderType"],
            quantity = data["quantity"],
            validity = data["validity"],
            price = data["price"],
            product = data["product"],
            open_close = "Lend",
            userid = "DAPI1",
            authorization_token = authorization_token
        )
    else:
        result = place_regular_order(
            tradingsecurity = data["symbol"],
            exchange = data["exchange"],
            transaction_type = data["transaction"],
            order_type = data["orderType"],
            quantity = data["quantity"],
            validity = data["validity"],
            price = data["price"],
            product = data["product"],
            authorization_token = authorization_token
        )
    
    # After placing order, get order status
    status = get_order_status(authorization_token)

    # Save to order.json
    with open("order_status.json", "w") as outfile:
        json.dump(status, outfile, indent=4)

    return jsonify({
        "order_result": result,
        "order_status": status
    })


from ordercancel import delete_order

@app.route('/api/cancel-order/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    print(f"[cancel_order] Received request to cancel order ID: {order_id}")

    with open('token.json') as f:
        token_data = json.load(f)
    api_key = "ijTLVhyDdou1iyK5MLnJmyAwT"
    request_token = token_data['data']['request_token']
    authorization_token = f"{api_key}:{request_token}"

    print(f"[cancel_order] Using authorization token: {authorization_token}")

    # Call your function from ordercancel.py
    result_text = delete_order(order_id, authorization_token)
    print(f"[cancel_order] Cancel result from broker: {result_text}")

    # Now also remove this order from your local order_status.json
    try:
        with open("order_status.json", "r") as infile:
            orders_data = json.load(infile)

        if "data" in orders_data and isinstance(orders_data["data"], list):
            original_count = len(orders_data["data"])

            updated_data = [
                order for order in orders_data["data"]
                if str(order.get("order_id")) != str(order_id)
            ]

            removed_count = original_count - len(updated_data)
            print(f"[cancel_order] Removed {removed_count} occurrence(s) of order ID: {order_id} from order_status.json")

            orders_data["data"] = updated_data

            with open("order_status.json", "w") as outfile:
                json.dump(orders_data, outfile, indent=4)
        else:
            print("[cancel_order] Unexpected JSON structure: 'data' key missing or not a list")

    except FileNotFoundError:
        print("[cancel_order] order_status.json file not found. Skipping local JSON update.")
    except Exception as e:
        print(f"[cancel_order] Error updating order_status.json: {e}")

    return jsonify({
        "status": "success",
        "message": f"Order {order_id} cancelled on broker and removed from local status.",
        "response": result_text
    })


@app.route('/api/dashboard')
def get_dashboard_data():
    try:
        with open("order_status.json") as f:
            orders_data = json.load(f)
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "order_status.json not found"}), 404

    orders = orders_data.get("data", [])
    
    # Convert timestamps so we can sort
    for order in orders:
        try:
            # parse to datetime object
            order["parsed_time"] = datetime.strptime(order["order_timestamp"], "%d/%m/%Y%H:%M:%S")
        except:
            order["parsed_time"] = datetime.min

    # Sort by most recent
    sorted_orders = sorted(orders, key=lambda o: o["parsed_time"], reverse=True)

    # Take top 3
    recent_orders = sorted_orders[:3]

    # Compute some simple stats
    active_positions = sum(1 for o in orders if o.get("status", "").lower() == "execute")
    # Fake portfolio value and PnL (you can wire actual logic)
    portfolio_value = 245680
    todays_pnl = 8450

    return jsonify({
        "status": "success",
        "portfolio_value": portfolio_value,
        "active_positions": active_positions,
        "todays_pnl": todays_pnl,
        "recent_orders": [
            {
                "symbol": order["tradingsymbol"],
                "transaction_type": order["transaction_type"],
                "quantity": order["quantity"],
                "status": order["status"]
            }
            for order in recent_orders
        ]
    })
@app.route('/trade')
def trade():
    return render_template('trade.html')  # or return some response
if __name__ == '__main__':
    app.run(debug=True, port=5000)