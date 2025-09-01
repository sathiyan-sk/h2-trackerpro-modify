package com.tracker.dto;

public class AuthResponse {
    
    private String token;
    private String type = "Bearer";
    private Long userId;
    private String fullName;
    private String empId;
    private String companyEmail;
    private String message;
    
    // Default constructor
    public AuthResponse() {}
    
    // Constructor for successful authentication
    public AuthResponse(String token, Long userId, String fullName, String empId, String companyEmail) {
        this.token = token;
        this.userId = userId;
        this.fullName = fullName;
        this.empId = empId;
        this.companyEmail = companyEmail;
        this.message = "Authentication successful";
    }
    
    // Constructor with message
    public AuthResponse(String message) {
        this.message = message;
    }
    
    // Getters and Setters
    public String getToken() {
        return token;
    }
    
    public void setToken(String token) {
        this.token = token;
    }
    
    public String getType() {
        return type;
    }
    
    public void setType(String type) {
        this.type = type;
    }
    
    public Long getUserId() {
        return userId;
    }
    
    public void setUserId(Long userId) {
        this.userId = userId;
    }
    
    public String getFullName() {
        return fullName;
    }
    
    public void setFullName(String fullName) {
        this.fullName = fullName;
    }
    
    public String getEmpId() {
        return empId;
    }
    
    public void setEmpId(String empId) {
        this.empId = empId;
    }
    
    public String getCompanyEmail() {
        return companyEmail;
    }
    
    public void setCompanyEmail(String companyEmail) {
        this.companyEmail = companyEmail;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
}