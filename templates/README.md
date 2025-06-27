# Trade2Algo Web Interface

This is a modern, clean, and professional HTML/CSS/JS implementation of the Trade2Algo trading platform interface.

## Project Structure

```
templates/
├── css/
│   └── styles.css        # Main stylesheet
├── js/
│   └── script.js         # JavaScript functionality
├── images/
│   ├── logo.png          # Small logo for header
│   ├── logo-small.png    # Small logo for modals
│   └── logo-large.png    # Large logo for welcome screen
├── home.html             # Branding landing page
├── index.html            # Login page
├── place-order.html      # Order placement page
├── order-book.html       # Order history page
├── trade-book.html       # Trade history page
├── positions-book.html   # Positions summary page
└── help.html             # Help documentation
```

## Features

- **Modern UI**: Clean, professional design with responsive layout
- **Interactive Components**: Form validation, table sorting, and modal dialogs
- **Consistent Design**: Unified color scheme and component styling
- **Responsive**: Works on desktop and mobile devices

## Pages

1. **Home Page**: Branding landing page with features, pricing, and company information
2. **Login Page**: User authentication with remember me functionality
3. **Place Order**: Form for placing equity and options orders
4. **Order Book**: View and manage order history
5. **Trade Book**: View executed trades
6. **Positions Book**: View current positions and P&L
7. **Help**: Documentation and support information

## How to Use

1. Open `home.html` in a web browser to start at the branding landing page
2. Navigate to the login page by clicking "Get Started" or "Login"
3. Use any username/password to simulate login
4. Navigate between different sections using the top navigation bar

## Customization

- **Colors**: Edit CSS variables in the `:root` section of `styles.css`
- **Logos**: Replace the logo files in the `images` directory
- **Data**: Update sample data in the HTML tables

## Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- No server-side requirements (static HTML/CSS/JS)

## Notes

This is a front-end implementation only. In a production environment, you would need to:

1. Connect to backend APIs for authentication and data
2. Implement proper security measures
3. Add error handling for API failures
4. Optimize assets for production 