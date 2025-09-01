package com.tracker.service;

import com.tracker.dto.UserRegistrationDto;
import com.tracker.entity.User;
import com.tracker.repository.UserRepository;
import com.tracker.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public UserServiceImpl(UserRepository userRepository,
                           PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public User registerUser(UserRegistrationDto dto) {
        // Check if email exists
        if (userRepository.existsByCompanyEmail(dto.getCompanyEmail())) {
            throw new RuntimeException("Email already registered!");
        }

        // Check if empId exists
        if (userRepository.existsByEmpId(dto.getEmpId())) {
            throw new RuntimeException("Employee ID already registered!");
        }

        // Check password match
        if (!dto.getPassword().equals(dto.getConfirmPassword())) {
            throw new RuntimeException("Passwords do not match!");
        }

        // Create new user entity
        User user = new User();
        user.setFullName(dto.getFullName());
        user.setDepartment(dto.getDepartment());
        user.setEmpId(dto.getEmpId());
        user.setPassword(passwordEncoder.encode(dto.getPassword())); // encrypt password
        user.setMobileNo(dto.getMobileNo());
        user.setCompanyEmail(dto.getCompanyEmail());

        return userRepository.save(user);
    }

    @Override
    public User loginUser(String identifier, String password) {
        Optional<User> userOpt = userRepository.findByEmailOrEmpId(identifier);

        if (userOpt.isEmpty()) {
            throw new RuntimeException("Invalid email/employee ID!");
        }

        User user = userOpt.get();

        // Check password match
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new RuntimeException("Invalid password!");
        }

        return user;
    }
}
