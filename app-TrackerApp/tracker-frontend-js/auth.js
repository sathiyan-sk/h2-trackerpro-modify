// Tracker Pro Authentication JavaScript
const API_BASE_URL = 'http://localhost:8080/api';

class AuthService {
    constructor() {
        this.token = localStorage.getItem('tracker_token');
        this.user = JSON.parse(localStorage.getItem('tracker_user') || 'null');
    }

    // API call utility
    async apiCall(endpoint, method = 'GET', data = null) {
        const config = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        // Add authorization header if token exists
        if (this.token) {
            config.headers.Authorization = `Bearer ${this.token}`;
        }

        // Add body for POST/PUT requests
        if (data && (method === 'POST' || method === 'PUT')) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.message || 'API call failed');
            }
            
            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Register new user
    async register(userData) {
        try {
            const result = await this.apiCall('/auth/register', 'POST', userData);
            
            if (result.success && result.data.token) {
                this.setAuthData(result.data.token, result.data);
                return result;
            }
            
            throw new Error(result.message || 'Registration failed');
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    }

    // Login user
    async login(credentials) {
        try {
            const result = await this.apiCall('/auth/login', 'POST', credentials);
            
            if (result.success && result.data.token) {
                this.setAuthData(result.data.token, result.data);
                return result;
            }
            
            throw new Error(result.message || 'Login failed');
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    // Set authentication data
    setAuthData(token, userData) {
        this.token = token;
        this.user = userData;
        localStorage.setItem('tracker_token', token);
        localStorage.setItem('tracker_user', JSON.stringify(userData));
    }

    // Check if user is authenticated
    isAuthenticated() {
        return this.token && this.user;
    }

    // Get current user
    getCurrentUser() {
        return this.user;
    }

    // Logout user
    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('tracker_token');
        localStorage.removeItem('tracker_user');
        window.location.href = 'Index.html';
    }

    // Check if email exists
    async checkEmail(email) {
        try {
            const result = await this.apiCall(`/auth/check-email?email=${encodeURIComponent(email)}`);
            return result.data; // returns boolean
        } catch (error) {
            console.error('Email check error:', error);
            return false;
        }
    }

    // Forgot password
    async forgotPassword(identifier) {
        try {
            const result = await this.apiCall(`/auth/forgot-password?identifier=${encodeURIComponent(identifier)}`, 'POST');
            return result;
        } catch (error) {
            console.error('Forgot password error:', error);
            throw error;
        }
    }
}

// Initialize AuthService
const authService = new AuthService();

// Form Handlers
function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const credentials = {
        identifier: formData.get('identifier') || formData.get('email'),
        password: formData.get('password')
    };

    if (!credentials.identifier || !credentials.password) {
        alert('Please fill in all fields');
        return;
    }

    // Show loading state
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Logging in...';
    submitBtn.disabled = true;

    authService.login(credentials)
        .then(result => {
            alert('Login successful!');
            window.location.href = 'dashboard.html';
        })
        .catch(error => {
            alert('Login failed: ' + error.message);
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
}

function handleRegister(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const userData = {
        fullName: formData.get('fullName'),
        department: formData.get('department'),
        empId: formData.get('empId'),
        password: formData.get('password'),
        confirmPassword: formData.get('confirmPassword'),
        mobileNo: formData.get('mobileNo'),
        companyEmail: formData.get('companyEmail')
    };

    // Client-side validation
    if (userData.password !== userData.confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    if (userData.password.length < 6) {
        alert('Password must be at least 6 characters long');
        return;
    }

    // Check required fields
    const requiredFields = ['fullName', 'department', 'empId', 'password', 'mobileNo', 'companyEmail'];
    for (let field of requiredFields) {
        if (!userData[field]) {
            alert(`Please fill in ${field.replace(/([A-Z])/g, ' $1').toLowerCase()}`);
            return;
        }
    }

    // Show loading state
    const submitBtn = event.target.querySelector('button[type="submit"], .signup-button');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Registering...';
    submitBtn.disabled = true;

    authService.register(userData)
        .then(result => {
            alert('Registration successful!');
            window.location.href = 'success.html';
        })
        .catch(error => {
            alert('Registration failed: ' + error.message);
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
}

function handleForgotPassword(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const identifier = formData.get('identifier') || formData.get('email');

    if (!identifier) {
        alert('Please enter your email or mobile number');
        return;
    }

    // Show loading state
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Processing...';
    submitBtn.disabled = true;

    authService.forgotPassword(identifier)
        .then(result => {
            alert(result.message);
        })
        .catch(error => {
            alert('Failed to process request: ' + error.message);
        })
        .finally(() => {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
}

// Utility functions
function showUserInfo() {
    if (authService.isAuthenticated()) {
        const user = authService.getCurrentUser();
        const userDisplayName = user.fullName || user.companyEmail;
        
        // Find elements to update with user info
        const userNameElements = document.querySelectorAll('.user-name, .username');
        userNameElements.forEach(element => {
            element.textContent = userDisplayName;
        });
    }
}

function requireAuth() {
    if (!authService.isAuthenticated()) {
        alert('Please login to access this page');
        window.location.href = 'Index.html';
        return false;
    }
    return true;
}

// Initialize page based on current location
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop();
    
    // Redirect if already authenticated and on login/register pages
    if (authService.isAuthenticated() && (currentPage.includes('Index') || currentPage.includes('login') || currentPage.includes('Register'))) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    // Require authentication for dashboard
    if (currentPage === 'dashboard.html') {
        requireAuth();
        showUserInfo();
    }
    
    // Attach form handlers
    const loginForm = document.querySelector('#login form, form[onsubmit*="login"]');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    const registerForm = document.querySelector('form[action*="register"], form[onsubmit*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
    
    const forgotForm = document.querySelector('form[action*="forgot"]');
    if (forgotForm) {
        forgotForm.addEventListener('submit', handleForgotPassword);
    }
    
    // Handle logout buttons
    const logoutBtns = document.querySelectorAll('.logout, [onclick*="logout"]');
    logoutBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            authService.logout();
        });
    });
    
    console.log('Tracker Pro Auth initialized for page:', currentPage);
    console.log('Authenticated:', authService.isAuthenticated());
});

// Export for global use
window.authService = authService;