import requests
import json

def run_login_and_save_token():
    # Step 1: Run login.py equivalent and save request token
    login_url = "https://wss1.mtsp.co.in:15207/connect/login"
    login_payload = {
        "api_key": "ijTLVhyDdou1iyK5MLnJmyAwT",
        "api_secrets": "QrRH7NxkphBg6Z#|eIsjRN<8"
    }
    login_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Api-Version": "3"
    }

    login_response = requests.post(login_url, data=login_payload, headers=login_headers)
    login_data = login_response.json()
    
    # Save the login response to token.json
    with open('token.json', 'w') as f:
        json.dump(login_data, f, indent=2)
    
    if login_data.get('status') != 'successful':
        raise Exception("Login failed: " + str(login_data))
    
    return login_data['data']['request_token']

def run_session_with_token(request_token):
    # Step 2: Use the request token with session.py
    session_url = "https://wss1.mtsp.co.in:15207/session/token"
    session_headers = {
        "Api-Version": "3",
        "Authorization": f"ijTLVhyDdou1iyK5MLnJmyAwT:{request_token}"
    }

    session_response = requests.get(session_url, headers=session_headers)
    session_data = session_response.json()
    
    # The session response might contain additional tokens if needed
    return session_data

def run_user_profile(request_token):
    # Step 3: Get user profile with the request token
    user_url = "https://wss1.mtsp.co.in:15207/user/profile"
    user_headers = {
        "Api-Version": "3",
        "Authorization": f"ijTLVhyDdou1iyK5MLnJmyAwT:{request_token}"
    }

    user_response = requests.get(user_url, headers=user_headers)
    user_data = user_response.json()
    
    # Save user data to user.json
    with open('user.json', 'w') as f:
        json.dump(user_data, f, indent=2)
    
    return user_data

def main():
    try:
        # Step 1: Login and get request token
        print("Logging in to get request token...")
        request_token = run_login_and_save_token()
        print(f"Request token obtained and saved to token.json: {request_token}")
        
        # Step 2: Use request token with session API
        print("Using request token with session API...")
        session_data = run_session_with_token(request_token)
        print("Session API response:", session_data)
        
        # Step 3: Get user profile
        print("Getting user profile...")
        user_data = run_user_profile(request_token)
        print("User profile data saved to user.json")
        print("User data:", user_data)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()