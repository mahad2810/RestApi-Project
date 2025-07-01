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

if __name__ == '__main__':
    app.run(debug=True, port=5000)