package com.tracker.entity;

// src/main/java/com/example/app/model/User.java

import jakarta.persistence.*;

@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fullName;
    private String department;
    private String empId;
    private String password;
    private String mobileNo;
    private String companyEmail;

    public User() {}

    public User(String fullName, String department, String empId, String password,
                String mobileNo, String companyEmail) {
        this.fullName = fullName;
        this.department = department;
        this.empId = empId;
        this.password = password;
        this.mobileNo = mobileNo;
        this.companyEmail = companyEmail;
    }

    // getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }

    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }

    public String getEmpId() { return empId; }
    public void setEmpId(String empId) { this.empId = empId; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getMobileNo() { return mobileNo; }
    public void setMobileNo(String mobileNo) { this.mobileNo = mobileNo; }

    public String getCompanyEmail() { return companyEmail; }
    public void setCompanyEmail(String companyEmail) { this.companyEmail = companyEmail; }
}
