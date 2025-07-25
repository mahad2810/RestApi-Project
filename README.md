# Trade2Algo Trading Platform

## Overview

Trade2Algo is a professional web-based trading platform that provides a comprehensive interface for trading operations. The platform includes features for order placement, order management, trade tracking, position management, and user authentication.

## Features

- **User Authentication**: Secure login/logout functionality with token-based authentication
- **Order Placement**: Place market and limit orders across multiple exchanges
- **Order Book**: View and manage all your orders in one place
- **Trade Book**: Track all executed trades with detailed information
- **Positions**: Monitor your current positions with real-time P&L tracking
- **User Profile**: View and manage your account details
- **API Integration**: Ready-to-use integration with trading APIs

## Technical Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: JWT (JSON Web Tokens)
- **Data Storage**: JSON files (can be extended to databases)

## Project Structure

```
RestApi Project/
├── app.py                  # Main Flask application
├── auth.py                 # Authentication module
├── data.py                 # Data handling functions
├── users.json              # User credentials storage
├── sessions.json           # Active sessions storage
├── orders.json             # Order data storage
├── user.json               # User profile data
├── static/                 # Static assets
│   ├── css/                # CSS stylesheets
│   └── images/             # Image assets
├── templates/              # HTML templates
│   ├── home.html           # Main application interface
│   └── positions.html      # Positions management page
└── LiveData/               # API integration scripts
    ├── login.py            # API login script
    ├── logout.py           # API logout script
    ├── LTP.py              # Last traded price fetching
    ├── order.py            # Order placement script
    ├── ordercancel.py      # Order cancellation script
    ├── orderstatus.py      # Order status checking script
    ├── session.py          # Session management script
    └── user.py             # User profile fetching script
```

## Setup and Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install flask flask-session bcrypt PyJWT
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Access the application at `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/register` - Register new user
- `POST /api/auth/change-password` - Change user password

### User Data

- `GET /api/user/profile` - Get user profile
- `GET /api/user/exchanges` - Get available exchanges
- `GET /api/user/products` - Get available products
- `GET /api/user/order-types` - Get available order types

### Orders

- `GET /api/orders/status` - Get all orders
- `GET /api/orders/<order_id>` - Get specific order
- `POST /api/orders/place` - Place new order
- `DELETE /api/orders/cancel/<order_id>` - Cancel order

### Trades

- `GET /api/orders/trades` - Get all trades

### Positions

- `GET /api/positions` - Get current positions

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Token expiration and validation
- Protected API endpoints

## Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- Real-time data with WebSockets
- Advanced charting capabilities
- Portfolio analytics
- Mobile responsive design
- Two-factor authentication #   R e s t A p i - P r o j e c t 
 
 