package com.tracker.service;

import com.tracker.dto.UserRegistrationDto;
import com.tracker.entity.User;

public interface UserService {
    User registerUser(UserRegistrationDto dto);
    User loginUser(String identifier, String password);
}
