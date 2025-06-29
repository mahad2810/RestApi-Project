from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static')

# Base URL for the API
API_BASE_URL = "https://wss1.mtsp.co.in:15207"

# API credentials
API_KEY = "ijTLVhyDdou1iyK5MLnJmyAwT"
API_SECRETS = "QrRH7NxkphBg6Z#|eIsjRN<8"

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Login proxy endpoint
@app.route('/api/login', methods=['POST'])
def login_proxy():
    url = f"{API_BASE_URL}/connect/login"
    
    # Use the credentials from the constants
    payload = {
        "api_key": API_KEY,
        "api_secrets": API_SECRETS
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Api-Version": "3"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Session token proxy endpoint
@app.route('/api/session/token', methods=['GET'])
def session_token_proxy():
    url = f"{API_BASE_URL}/session/token"
    
    # Get the authorization token from the request
    auth_token = request.headers.get('Authorization', '')
    
    headers = {
        "Api-Version": "3",
        "Authorization": auth_token
    }
    
    try:
        response = requests.get(url, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Logout proxy endpoint
@app.route('/api/logout', methods=['DELETE'])
def logout_proxy():
    url = f"{API_BASE_URL}/connect/login"
    
    # Get the authorization token from the request
    auth_token = request.headers.get('Authorization', '')
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Api-Version": "3"
    }
    
    # Add Authorization header if provided
    if auth_token:
        headers["Authorization"] = auth_token
    
    payload = {
        "api_key": API_KEY
    }
    
    # Add api_secrets only if no auth token is provided
    if not auth_token:
        payload["api_secrets"] = API_SECRETS
    
    try:
        response = requests.delete(url, data=payload, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Order placement proxy endpoint
@app.route('/api/orders', methods=['POST'])
def place_order_proxy():
    url = f"{API_BASE_URL}/orders/regular"
    
    # Get the authorization token from the request
    auth_token = request.headers.get('Authorization', '')
    
    # Get the order data from the request
    order_data = request.json
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Api-Version": "3",
        "Authorization": auth_token
    }
    
    try:
        response = requests.post(url, data=order_data, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Order status proxy endpoint
@app.route('/api/orders', methods=['GET'])
def order_status_proxy():
    url = f"{API_BASE_URL}/orders"
    
    # Get the authorization token from the request
    auth_token = request.headers.get('Authorization', '')
    
    headers = {
        "Api-Version": "3",
        "Authorization": auth_token
    }
    
    try:
        response = requests.get(url, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Order cancellation proxy endpoint
@app.route('/api/orders/<order_id>', methods=['DELETE'])
def cancel_order_proxy(order_id):
    url = f"{API_BASE_URL}/orders/regular/{order_id}"
    
    # Get the authorization token from the request
    auth_token = request.headers.get('Authorization', '')
    
    headers = {
        "Api-Version": "3",
        "Authorization": auth_token
    }
    
    try:
        response = requests.delete(url, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# User profile proxy endpoint
@app.route('/api/user/profile', methods=['GET'])
def user_profile_proxy():
    url = f"{API_BASE_URL}/user/profile"
    
    # Get the authorization token from the request
    auth_token = request.headers.get('Authorization', '')
    
    headers = {
        "Api-Version": "3",
        "Authorization": auth_token
    }
    
    try:
        response = requests.get(url, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)