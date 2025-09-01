#!/usr/bin/env python3
"""
Tracker Pro Backend API Testing Suite
Tests all authentication endpoints with comprehensive scenarios
"""

import requests
import json
import sys
from datetime import datetime
import time

class TrackerProAPITester:
    def __init__(self, base_url="http://localhost:8080/api"):
        self.base_url = base_url
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, message="", response_data=None):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}: PASSED - {message}")
        else:
            print(f"❌ {name}: FAILED - {message}")
        
        self.test_results.append({
            'test': name,
            'success': success,
            'message': message,
            'response_data': response_data
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        
        if headers:
            default_headers.update(headers)
        
        if self.token and 'Authorization' not in default_headers:
            default_headers['Authorization'] = f'Bearer {self.token}'

        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        print(f"   Method: {method}")
        if data:
            print(f"   Data: {json.dumps(data, indent=2)}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=default_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=default_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=default_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=default_headers, timeout=10)

            print(f"   Response Status: {response.status_code}")
            
            try:
                response_json = response.json()
                print(f"   Response: {json.dumps(response_json, indent=2)}")
            except:
                response_json = {"raw_response": response.text}
                print(f"   Raw Response: {response.text}")

            success = response.status_code == expected_status
            message = f"Status: {response.status_code}"
            
            if success and response_json.get('success'):
                message += f" - {response_json.get('message', 'Success')}"
            elif not success:
                message += f" (Expected: {expected_status})"
                if response_json.get('message'):
                    message += f" - {response_json.get('message')}"

            self.log_test(name, success, message, response_json)
            return success, response_json

        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {str(e)}"
            print(f"   Error: {error_msg}")
            self.log_test(name, False, error_msg)
            return False, {}

    def test_health_check(self):
        """Test health check endpoint"""
        return self.run_test(
            "Health Check",
            "GET",
            "auth/health",
            200
        )

    def test_user_registration(self):
        """Test user registration with valid data"""
        timestamp = datetime.now().strftime('%H%M%S')
        test_user = {
            "fullName": f"Test User {timestamp}",
            "department": "IT",
            "empId": f"EMP{timestamp}",
            "password": "TestPass123!",
            "confirmPassword": "TestPass123!",
            "mobileNo": f"9876543{timestamp[-3:]}",
            "companyEmail": f"test{timestamp}@company.com"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=test_user
        )
        
        if success and response.get('success') and response.get('data', {}).get('token'):
            self.token = response['data']['token']
            self.user_data = response['data']
            print(f"   ✅ Token received: {self.token[:20]}...")
        
        return success, response

    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        if not self.user_data:
            print("⚠️  Skipping duplicate email test - no previous user data")
            return True, {}
            
        duplicate_user = {
            "fullName": "Duplicate User",
            "department": "HR",
            "empId": "EMP999999",
            "password": "TestPass123!",
            "confirmPassword": "TestPass123!",
            "mobileNo": "9876543999",
            "companyEmail": self.user_data.get('companyEmail', 'test@company.com')
        }
        
        return self.run_test(
            "Registration with Duplicate Email",
            "POST",
            "auth/register",
            400,
            data=duplicate_user
        )

    def test_user_registration_invalid_data(self):
        """Test registration with invalid data"""
        invalid_user = {
            "fullName": "",  # Empty name
            "department": "IT",
            "empId": "123",
            "password": "123",  # Too short
            "confirmPassword": "456",  # Doesn't match
            "mobileNo": "123",  # Too short
            "companyEmail": "invalid-email"  # Invalid format
        }
        
        return self.run_test(
            "Registration with Invalid Data",
            "POST",
            "auth/register",
            400,
            data=invalid_user
        )

    def test_user_login_with_email(self):
        """Test login with email"""
        if not self.user_data:
            print("⚠️  Skipping email login test - no user data available")
            return True, {}
            
        login_data = {
            "identifier": self.user_data.get('companyEmail'),
            "password": "TestPass123!"
        }
        
        success, response = self.run_test(
            "Login with Email",
            "POST",
            "auth/login",
            200,
            data=login_data
        )
        
        if success and response.get('success') and response.get('data', {}).get('token'):
            self.token = response['data']['token']
            print(f"   ✅ New token received: {self.token[:20]}...")
        
        return success, response

    def test_user_login_with_emp_id(self):
        """Test login with employee ID"""
        if not self.user_data:
            print("⚠️  Skipping employee ID login test - no user data available")
            return True, {}
            
        login_data = {
            "identifier": self.user_data.get('empId'),
            "password": "TestPass123!"
        }
        
        return self.run_test(
            "Login with Employee ID",
            "POST",
            "auth/login",
            200,
            data=login_data
        )

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "identifier": "nonexistent@company.com",
            "password": "WrongPassword123!"
        }
        
        return self.run_test(
            "Login with Invalid Credentials",
            "POST",
            "auth/login",
            401,
            data=login_data
        )

    def test_token_validation(self):
        """Test JWT token validation"""
        if not self.token:
            print("⚠️  Skipping token validation test - no token available")
            return True, {}
            
        headers = {'Authorization': f'Bearer {self.token}'}
        
        return self.run_test(
            "Token Validation",
            "POST",
            "auth/validate-token",
            200,
            headers=headers
        )

    def test_token_validation_invalid(self):
        """Test token validation with invalid token"""
        headers = {'Authorization': 'Bearer invalid.token.here'}
        
        return self.run_test(
            "Invalid Token Validation",
            "POST",
            "auth/validate-token",
            401,
            headers=headers
        )

    def test_check_email_exists(self):
        """Test email existence check"""
        if not self.user_data:
            print("⚠️  Skipping email check test - no user data available")
            return True, {}
            
        return self.run_test(
            "Check Email Exists",
            "GET",
            f"auth/check-email?email={self.user_data.get('companyEmail')}",
            200
        )

    def test_check_email_not_exists(self):
        """Test email existence check for non-existent email"""
        return self.run_test(
            "Check Non-existent Email",
            "GET",
            "auth/check-email?email=nonexistent@company.com",
            200
        )

    def test_forgot_password(self):
        """Test forgot password functionality"""
        if not self.user_data:
            print("⚠️  Skipping forgot password test - no user data available")
            return True, {}
            
        return self.run_test(
            "Forgot Password",
            "POST",
            f"auth/forgot-password?identifier={self.user_data.get('companyEmail')}",
            200
        )

    def test_get_user_profile(self):
        """Test getting user profile (requires authentication)"""
        if not self.token:
            print("⚠️  Skipping profile test - no token available")
            return True, {}
            
        return self.run_test(
            "Get User Profile",
            "GET",
            "auth/profile",
            200
        )

    def run_all_tests(self):
        """Run all API tests in sequence"""
        print("🚀 Starting Tracker Pro Backend API Tests")
        print("=" * 60)
        
        # Basic connectivity
        self.test_health_check()
        
        # Registration tests
        self.test_user_registration()
        self.test_user_registration_duplicate_email()
        self.test_user_registration_invalid_data()
        
        # Login tests
        self.test_user_login_with_email()
        self.test_user_login_with_emp_id()
        self.test_user_login_invalid_credentials()
        
        # Token validation tests
        self.test_token_validation()
        self.test_token_validation_invalid()
        
        # Utility endpoint tests
        self.test_check_email_exists()
        self.test_check_email_not_exists()
        self.test_forgot_password()
        
        # Protected endpoint tests
        self.test_get_user_profile()
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Show failed tests
        failed_tests = [r for r in self.test_results if not r['success']]
        if failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['message']}")
        
        print("\n" + "=" * 60)
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    print("🔧 Tracker Pro Backend API Testing Suite")
    print("Testing Spring Boot backend on http://localhost:8080/api")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    tester = TrackerProAPITester()
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())