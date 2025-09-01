# Tracker Pro - Complete Setup Guide

## Overview
This project provides a complete Spring Boot backend with JWT authentication and integrated HTML frontend for the Tracker Pro application.

## Technology Stack
- **Backend**: Spring Boot 3.2.1, MySQL, JWT Authentication
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: MySQL/MariaDB
- **Authentication**: JWT Tokens

## Project Structure

```
/app/
├── tracker-backend/                 # Spring Boot Backend
│   ├── pom.xml                     # Maven dependencies
│   ├── src/main/java/com/tracker/
│   │   ├── TrackerProApplication.java
│   │   ├── config/                 # Security configurations
│   │   ├── controller/             # REST controllers
│   │   ├── dto/                    # Data transfer objects
│   │   ├── entity/                 # JPA entities
│   │   ├── repository/             # Data repositories
│   │   ├── service/                # Business logic
│   │   └── util/                   # JWT utilities
│   └── src/main/resources/
│       └── application.properties   # Configuration
├── tracker-frontend-integrated/     # HTML Frontend with JS Integration
│   ├── Index.html                  # Main login page
│   ├── Register.html               # Registration page  
│   ├── dashboard.html              # Dashboard page
│   ├── success.html                # Success page
│   └── *.png                       # Images
└── tracker-pro.github.io-main/    # Original HTML files
```

## Backend Features

### 1. User Management
- User registration with validation
- Login with email or employee ID
- JWT token-based authentication
- Password encryption with BCrypt

### 2. API Endpoints

#### Authentication Endpoints
- `GET /api/auth/health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/validate-token` - Token validation
- `GET /api/auth/check-email` - Check if email exists
- `POST /api/auth/forgot-password` - Password reset request

### 3. Security Features
- CORS configuration for frontend integration
- JWT token with 24-hour expiration
- Secure password hashing
- Protected endpoints with authentication

### 4. Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    emp_id VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    mobile_no VARCHAR(15) NOT NULL,
    company_email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);
```

## Frontend Features

### 1. Authentication Pages
- **Index.html**: Main login page with dual login options
- **Register.html**: User registration with form validation
- **dashboard.html**: Protected dashboard with user info
- **success.html**: Registration success confirmation

### 2. JavaScript Integration
- Real-time API communication
- Token-based session management
- Form validation and error handling
- Automatic redirects and authentication checks

### 3. User Experience
- Responsive design for all devices
- Loading states and error messages
- Automatic token validation
- Seamless authentication flow

## Installation & Setup

### Prerequisites
- Java 17+
- Maven 3.6+
- MySQL/MariaDB
- Modern web browser

### Step 1: Database Setup
```bash
# Start MySQL service
sudo service mariadb start

# Set root password
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'password'; FLUSH PRIVILEGES;"

# Database will be auto-created by Spring Boot
```

### Step 2: Backend Setup
```bash
# Navigate to backend directory
cd /app/tracker-backend

# Compile the application
mvn clean compile

# Run the application
mvn spring-boot:run

# Backend will be available at: http://localhost:8080
```

### Step 3: Frontend Setup
```bash
# Navigate to frontend directory
cd /app/tracker-frontend-integrated

# Open in web browser or serve via HTTP server
# Files can be opened directly in browser or served via:
# python3 -m http.server 8000
# Then access: http://localhost:8000
```

## Configuration

### Backend Configuration (`application.properties`)
```properties
# Database
spring.datasource.url=jdbc:mysql://localhost:3306/tracker_pro_db?createDatabaseIfNotExist=true
spring.datasource.username=root
spring.datasource.password=password

# Server
server.port=8080
server.servlet.context-path=/api

# JWT
jwt.secret=TrYcK3rPr0S3cur3K3yF0rJWTAu7h3n7ic@7i0n2025!@#$%^&*()
jwt.expiration=86400000

# CORS
cors.allowed.origins=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5500,http://127.0.0.1:5500
```

### Frontend Configuration
- API base URL is set to `http://localhost:8080/api`
- Authentication tokens stored in localStorage
- Automatic session management

## API Usage Examples

### 1. Register New User
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "John Doe",
    "department": "IT",
    "empId": "EMP001",
    "password": "password123",
    "confirmPassword": "password123",
    "mobileNo": "+91-9876543210",
    "companyEmail": "john.doe@company.com"
  }'
```

### 2. Login User
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "john.doe@company.com",
    "password": "password123"
  }'
```

### 3. Access Protected Resource
```bash
curl -X GET http://localhost:8080/api/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Authentication Flow

1. **Registration**: User fills registration form → Data sent to `/auth/register` → JWT token returned → User redirected to success page
2. **Login**: User enters credentials → Data sent to `/auth/login` → JWT token returned → User redirected to dashboard  
3. **Dashboard Access**: Token validated → User data displayed → Protected resources accessible
4. **Session Management**: Token stored in localStorage → Automatic validation on page load → Logout clears session

## Security Considerations

### Backend Security
- Passwords hashed with BCrypt
- JWT tokens signed with secure secret
- CORS properly configured
- Input validation on all endpoints
- Protected routes require authentication

### Frontend Security
- Tokens stored securely in localStorage
- Automatic token validation
- Session timeout handling
- No sensitive data in client-side code

## Testing

### Backend Testing
```bash
# Health check
curl http://localhost:8080/api/auth/health

# Test registration (should succeed)
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Test User","department":"HR","empId":"TEST001","password":"test123","confirmPassword":"test123","mobileNo":"+91-1234567890","companyEmail":"test@test.com"}'

# Test login (should succeed)  
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"test@test.com","password":"test123"}'
```

### Frontend Testing
1. Open `Index.html` in browser
2. Try registration with valid data
3. Try login with registered credentials
4. Access dashboard and verify user info
5. Test logout functionality

## Troubleshooting

### Common Issues

1. **Backend won't start**
   - Check MySQL is running: `service mariadb status`
   - Verify database credentials in application.properties
   - Check port 8080 is available

2. **Frontend can't connect to backend**
   - Verify backend is running on port 8080
   - Check CORS configuration includes your frontend URL
   - Verify API_BASE_URL in frontend JavaScript

3. **Authentication fails**
   - Check JWT secret is properly set
   - Verify token format in Authorization header
   - Check token expiration time

4. **Database connection errors**
   - Ensure MySQL is running and accessible
   - Verify database credentials
   - Check database name and connection string

### Logs
- Backend logs: Check console output when running `mvn spring-boot:run`
- Frontend logs: Check browser developer console (F12)
- Database logs: Check MySQL error log

## Next Steps

### Potential Enhancements
1. **Role-based Access Control**: Add user roles (Admin, Employee, Student)
2. **Password Reset**: Implement email-based password reset
3. **Profile Management**: Allow users to update their profiles
4. **Advanced Dashboard**: Add reports, analytics, and user management
5. **Mobile App**: Create React Native or Flutter mobile application

### Production Deployment
1. **Security**: Update JWT secret, use HTTPS, implement rate limiting
2. **Database**: Use production MySQL instance with proper backups
3. **Monitoring**: Add application monitoring and logging
4. **Scalability**: Implement load balancing and database connection pooling

## Support
For issues or questions, refer to the Spring Boot documentation and ensure all dependencies are properly installed.

---
**Tracker Pro - Complete Authentication System**
*Built with Spring Boot, JWT, and Modern Frontend Integration*