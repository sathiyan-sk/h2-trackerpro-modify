package com.tracker.repository;

import com.tracker.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * Find user by company email
     */
    Optional<User> findByCompanyEmail(String companyEmail);

    /**
     * Find user by employee ID
     */
    Optional<User> findByEmpId(String empId);

    /**
     * Check if email already exists
     */
    boolean existsByCompanyEmail(String companyEmail);

    /**
     * Check if employee ID already exists
     */
    boolean existsByEmpId(String empId);

    /**
     * Find user by email or employee ID for login
     */
    @Query("SELECT u FROM User u WHERE u.companyEmail = :identifier OR u.empId = :identifier")
    Optional<User> findByEmailOrEmpId(@Param("identifier") String identifier);

    /**
     * Find user by mobile number (for password reset)
     */
    Optional<User> findByMobileNo(String mobileNo);
}