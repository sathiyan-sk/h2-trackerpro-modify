package com.tracker.controller;

import com.tracker.dto.UserRegistrationDto;
import com.tracker.entity.User;
import com.tracker.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final UserService userService;

    @Autowired
    public AuthController(UserService userService) {
        this.userService = userService;
    }

    /**
     * Register new user
     */
    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@RequestBody UserRegistrationDto dto) {
        try {
            User savedUser = userService.registerUser(dto);
            return ResponseEntity.ok(savedUser);
        } catch (RuntimeException ex) {
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }

    /**
     * Login user (using email or empId + password)
     */
    @PostMapping("/login")
    public ResponseEntity<?> loginUser(@RequestParam String identifier,
                                       @RequestParam String password) {
        try {
            User loggedInUser = userService.loginUser(identifier, password);
            return ResponseEntity.ok(loggedInUser);
        } catch (RuntimeException ex) {
            return ResponseEntity.badRequest().body(ex.getMessage());
        }
    }
}
