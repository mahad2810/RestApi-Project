document.addEventListener('DOMContentLoaded', function() {
    // Update date and time in footer
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute
    
    // Modal functionality
    setupModals();
    
    // Setup form change events
    setupFormEvents();
    
    // Setup table sorting
    setupTableSorting();
    
    // Setup login form
    setupLoginForm();
    
    // Setup home page specific functionality
    setupHomePage();
    
    // Setup login modal triggers
    setupLoginModal();
    
    // Setup sidebar functionality
    setupSidebar();
    
    // Check login status and update UI
    checkLoginStatus();
});

// Setup sidebar toggle functionality
function setupSidebar() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    
    // Check if sidebar elements exist
    if (sidebar && mainContent) {
        // Check for saved state
        const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        
        // Apply initial state - sidebar is visible by default, but may be collapsed
        if (sidebarCollapsed) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('expanded');
        }
        
        // Toggle sidebar width on sidebar toggle button click
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('expanded');
                
                // Save state to localStorage
                localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
            });
        }
        
        // Close sidebar when clicking on overlay (mobile)
        if (sidebarOverlay) {
            sidebarOverlay.addEventListener('click', function() {
                sidebar.classList.remove('active');
                sidebarOverlay.classList.remove('active');
            });
        }
        
        // Handle sidebar menu items
        const menuItems = document.querySelectorAll('.side-nav a');
        menuItems.forEach(item => {
            item.addEventListener('click', function() {
                // Remove active class from all items
                menuItems.forEach(i => i.classList.remove('active'));
                
                // Add active class to clicked item
                this.classList.add('active');
                
                // On mobile, hide sidebar after click
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('active');
                    if (sidebarOverlay) {
                        sidebarOverlay.classList.remove('active');
                    }
                }
            });
        });
    }
}

// Check if user is logged in and update UI accordingly
function checkLoginStatus() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');
    
    if (isLoggedIn) {
        // Change login link to show user is logged in
        if (loginLink) {
            loginLink.innerHTML = '<i class="fas fa-user"></i> <span>My Account</span>';
        }
        
        // Setup logout link
        if (logoutLink) {
            logoutLink.style.display = 'block';
            logoutLink.addEventListener('click', function(e) {
                e.preventDefault();
                localStorage.removeItem('isLoggedIn');
                window.location.reload();
            });
        }
    } else {
        // Hide logout link when not logged in
        if (logoutLink) {
            logoutLink.style.display = 'none';
        }
        
        // Ensure login link shows login text
        if (loginLink) {
            loginLink.innerHTML = '<i class="fas fa-sign-in-alt"></i> <span>Login</span>';
        }
    }
    
    // We're no longer hiding trading links based on login status
    // All menu items are now visible by default
}

// Setup login modal functionality
function setupLoginModal() {
    const loginModal = document.getElementById('login-modal');
    if (loginModal) {
        // Get all login trigger buttons
        const loginTriggers = [
            document.getElementById('login-link'),
            document.getElementById('hero-login-btn'),
            ...document.querySelectorAll('.pricing-login-btn')
        ].filter(el => el !== null);
        
        // Add click event to each login trigger
        loginTriggers.forEach(trigger => {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                
                // If user is already logged in, log them out
                if (localStorage.getItem('isLoggedIn') === 'true') {
                    localStorage.removeItem('isLoggedIn');
                    window.location.reload();
                    return;
                }
                
                loginModal.style.display = 'block';
            });
        });
        
        // Close button functionality
        const closeButton = loginModal.querySelector('.close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                loginModal.style.display = 'none';
            });
        }
        
        // Close modal when clicking outside
        window.addEventListener('click', function(e) {
            if (e.target === loginModal) {
                loginModal.style.display = 'none';
            }
        });
    }
}

// Update date and time in the footer
function updateDateTime() {
    const now = new Date();
    const timeElement = document.querySelector('.footer-info .time');
    const dateElement = document.querySelector('.footer-info .date');
    
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString('en-GB', { 
            day: '2-digit', 
            month: '2-digit', 
            year: 'numeric' 
        }).replace(/\//g, '-');
    }
}

// Setup home page functionality
function setupHomePage() {
    // Check if we're on the home page
    if (document.body.classList.contains('home-page')) {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80, // Offset for header
                        behavior: 'smooth'
                    });
                }
            });
        });
        
        // Add scroll animation for elements
        const animateOnScroll = () => {
            const elements = document.querySelectorAll('.feature-card, .pricing-card, .testimonial-card, .about-content');
            
            elements.forEach(element => {
                const elementPosition = element.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (elementPosition < windowHeight - 100) {
                    element.classList.add('animate-in');
                }
            });
        };
        
        // Initial check on page load
        animateOnScroll();
        
        // Check on scroll
        window.addEventListener('scroll', animateOnScroll);
    }
}

// Setup login form functionality
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const remember = document.getElementById('remember').checked;
            
            // Basic validation
            if (!username || !password) {
                alert('Please enter both username and password');
                return;
            }
            
            // Simulate API call for login
            console.log('Logging in with:', { username, password, remember });
            
            // Show loading indicator
            const loginButton = document.querySelector('.btn-login');
            const originalText = loginButton.textContent;
            loginButton.textContent = 'Logging in...';
            loginButton.disabled = true;
            
            // Simulate API delay
            setTimeout(() => {
                // Simulate successful login
                localStorage.setItem('isLoggedIn', 'true');
                if (remember) {
                    localStorage.setItem('username', username);
                } else {
                    localStorage.removeItem('username');
                }
                
                // Close the login modal
                const loginModal = document.getElementById('login-modal');
                if (loginModal) {
                    loginModal.style.display = 'none';
                }
                
                // Update UI based on login status
                checkLoginStatus();
                
                // Reset button state
                loginButton.textContent = originalText;
                loginButton.disabled = false;
                
                // Redirect to place order page if not on home page
                if (!document.body.classList.contains('home-page')) {
                    window.location.href = 'place-order.html';
                }
            }, 1500);
        });
        
        // Auto-fill remembered username
        const rememberedUsername = localStorage.getItem('username');
        if (rememberedUsername) {
            document.getElementById('username').value = rememberedUsername;
            document.getElementById('remember').checked = true;
        }
    }
}

// Setup modal functionality
function setupModals() {
    // Get all modal triggers and modals
    const modalTriggers = {
        'place-order-link': document.getElementById('place-order-modal'),
        'order-book-link': document.getElementById('order-book-modal'),
        'trade-book-link': document.getElementById('trade-book-modal')
    };
    
    // Add click event to each trigger
    for (const [triggerId, modal] of Object.entries(modalTriggers)) {
        const trigger = document.getElementById(triggerId);
        if (trigger && modal) {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                modal.style.display = 'block';
            });
        }
    }
    
    // Close button functionality
    const closeButtons = document.querySelectorAll('.close, .btn-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                modal.style.display = 'none';
            });
        }
    });
}

// Setup form events
function setupFormEvents() {
    const instrumentTypeSelect = document.getElementById('instrument-type');
    const exchangeSelect = document.getElementById('exchange');
    const symbolSelect = document.getElementById('symbol');
    
    if (instrumentTypeSelect && exchangeSelect) {
        // Update available options based on selections
        instrumentTypeSelect.addEventListener('change', updateFormOptions);
        exchangeSelect.addEventListener('change', updateFormOptions);
    }
    
    // Place order form submission
    const placeOrderForm = document.getElementById('place-order-form');
    if (placeOrderForm) {
        placeOrderForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(placeOrderForm);
            const orderData = {};
            
            for (const [key, value] of formData.entries()) {
                orderData[key] = value;
            }
            
            // Validate form data
            if (validateOrderForm(orderData)) {
                // Simulate API call
                submitOrder(orderData);
            }
        });
    }
}

// Update form options based on selected values
function updateFormOptions() {
    const instrumentType = document.getElementById('instrument-type').value;
    const exchange = document.getElementById('exchange').value;
    const symbolSelect = document.getElementById('symbol');
    const optionTypeSelect = document.getElementById('option-type');
    const expiryDateSelect = document.getElementById('expiry-date');
    const strikePriceSelect = document.getElementById('strike-price');
    
    // Reset dependent fields
    optionTypeSelect.innerHTML = '<option value=""></option>';
    expiryDateSelect.innerHTML = '<option value=""></option>';
    strikePriceSelect.innerHTML = '<option value=""></option>';
    
    // Update symbol options based on exchange and instrument type
    symbolSelect.innerHTML = '';
    
    if (exchange === 'nse_cm' && instrumentType === 'EQ') {
        // Add equity symbols
        addOption(symbolSelect, 'RELIANCE', 'RELIANCE');
        addOption(symbolSelect, 'TCS', 'TCS');
        addOption(symbolSelect, 'IDEA', 'IDEA');
    } else if (exchange === 'nse_fo' && instrumentType === 'OPTIDX') {
        // Add index options
        addOption(symbolSelect, 'NIFTY', 'NIFTY');
        addOption(symbolSelect, 'BANKNIFTY', 'BANKNIFTY');
        
        // Add option types
        addOption(optionTypeSelect, 'CE', 'CE');
        addOption(optionTypeSelect, 'PE', 'PE');
        
        // Add expiry dates
        addOption(expiryDateSelect, '12JUN2025', '12JUN2025');
        addOption(expiryDateSelect, '26JUN2025', '26JUN2025');
        
        // Add strike prices
        addOption(strikePriceSelect, '26800', '26800');
        addOption(strikePriceSelect, '27000', '27000');
        addOption(strikePriceSelect, '27200', '27200');
    }
    
    // Show/hide option-specific fields
    const optionFields = document.querySelectorAll('.option-field');
    if (instrumentType === 'OPTIDX') {
        optionFields.forEach(field => field.style.display = 'flex');
    } else {
        optionFields.forEach(field => field.style.display = 'none');
    }
}

// Helper function to add options to select
function addOption(selectElement, value, text) {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = text;
    selectElement.appendChild(option);
}

// Validate order form
function validateOrderForm(data) {
    // Basic validation
    if (!data.symbol) {
        alert('Please select a symbol');
        return false;
    }
    
    if (!data.quantity || isNaN(data.quantity) || data.quantity <= 0) {
        alert('Please enter a valid quantity');
        return false;
    }
    
    // Additional validation for options
    if (data['instrument-type'] === 'OPTIDX') {
        if (!data['option-type']) {
            alert('Please select an option type');
            return false;
        }
        
        if (!data['expiry-date']) {
            alert('Please select an expiry date');
            return false;
        }
        
        if (!data['strike-price']) {
            alert('Please select a strike price');
            return false;
        }
    }
    
    return true;
}

// Submit order to API
function submitOrder(orderData) {
    console.log('Submitting order:', orderData);
    
    // Simulate API call with timeout
    setTimeout(() => {
        // Simulate success response
        const response = {
            status: 'success',
            orderId: Math.floor(Math.random() * 1000000000000),
            message: 'Order placed successfully'
        };
        
        // Show success message
        alert(`Order placed successfully! Order ID: ${response.orderId}`);
        
        // Close modal
        const modal = document.getElementById('place-order-modal');
        if (modal) {
            modal.style.display = 'none';
        }
        
        // Reset form
        const form = document.getElementById('place-order-form');
        if (form) {
            form.reset();
        }
    }, 1000);
}

// Setup table sorting
function setupTableSorting() {
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        const headers = table.querySelectorAll('thead th');
        
        headers.forEach((header, index) => {
            header.addEventListener('click', function() {
                sortTable(table, index);
            });
            
            // Add sort indicator and cursor
            header.style.cursor = 'pointer';
            header.setAttribute('data-sort', 'none');
        });
    });
}

// Sort table by column
function sortTable(table, columnIndex) {
    const header = table.querySelectorAll('thead th')[columnIndex];
    const currentSort = header.getAttribute('data-sort');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Reset all headers
    table.querySelectorAll('thead th').forEach(th => {
        th.setAttribute('data-sort', 'none');
    });
    
    // Determine sort direction
    const direction = currentSort === 'asc' ? 'desc' : 'asc';
    header.setAttribute('data-sort', direction);
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Check if values are numbers
        if (!isNaN(aValue) && !isNaN(bValue)) {
            return direction === 'asc' 
                ? parseFloat(aValue) - parseFloat(bValue)
                : parseFloat(bValue) - parseFloat(aValue);
        }
        
        // Sort as strings
        return direction === 'asc'
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
    });
    
    // Reorder rows in the table
    rows.forEach(row => tbody.appendChild(row));
} 