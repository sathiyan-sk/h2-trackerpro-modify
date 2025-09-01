package com.tracker.dto;

public class UserRegistrationDto {
    private String fullName;
    private String department;
    private String empId;
    private String password;
    private String confirmPassword;
    private String mobileNo;
    private String companyEmail;

    public UserRegistrationDto() {}

    public UserRegistrationDto(String fullName, String department, String empId,
                               String password, String confirmPassword, String mobileNo, String companyEmail) {
        this.fullName = fullName;
        this.department = department;
        this.empId = empId;
        this.password = password;
        this.confirmPassword = confirmPassword;
        this.mobileNo = mobileNo;
        this.companyEmail = companyEmail;
    }

    // getters and setters
    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }
    public String getEmpId() { return empId; }
    public void setEmpId(String empId) { this.empId = empId; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getConfirmPassword() { return confirmPassword; }
    public void setConfirmPassword(String confirmPassword) { this.confirmPassword = confirmPassword; }
    public String getMobileNo() { return mobileNo; }
    public void setMobileNo(String mobileNo) { this.mobileNo = mobileNo; }
    public String getCompanyEmail() { return companyEmail; }
    public void setCompanyEmail(String companyEmail) { this.companyEmail = companyEmail; }
}
