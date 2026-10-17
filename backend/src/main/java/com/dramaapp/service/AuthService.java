package com.dramaapp.service;

import com.dramaapp.dto.LoginRequestDto;
import com.dramaapp.dto.LoginResponseDto;
import com.dramaapp.model.User;
import com.dramaapp.model.UserRole;
import com.dramaapp.repository.UserRepository;
import com.dramaapp.security.JwtTokenProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;
    private final AuditService auditService;

    @Value("${dramaapp.admin.default-username:admin}")
    private String defaultAdminUsername;

    @Value("${dramaapp.admin.default-password:admin123}")
    private String defaultAdminPassword;

    public LoginResponseDto login(LoginRequestDto loginRequest) {
        User user = userRepository.findByUsername(loginRequest.getUsername())
                .orElseThrow(() -> new BadCredentialsException("Invalid username or password"));

        if (!passwordEncoder.matches(loginRequest.getPassword(), user.getPasswordHash())) {
            log.warn("Failed login attempt for user: {}", loginRequest.getUsername());
            throw new BadCredentialsException("Invalid username or password");
        }

        user.setLastLoginAt(Instant.now());
        userRepository.save(user);

        String role = user.getRole().name();
        String token = jwtTokenProvider.generateToken(user.getUsername(), role);

        auditService.logAction(user.getUsername(), "LOGIN", "USER", user.getId(), "User logged in successfully");

        return LoginResponseDto.builder()
                .token(token)
                .tokenType("Bearer")
                .username(user.getUsername())
                .role(role)
                .expiresInMs(jwtTokenProvider.getExpirationMs())
                .build();
    }

    public void initDefaultAdmin() {
        if (!userRepository.existsByUsername(defaultAdminUsername)) {
            User admin = User.builder()
                    .username(defaultAdminUsername)
                    .passwordHash(passwordEncoder.encode(defaultAdminPassword))
                    .role(UserRole.ADMIN)
                    .createdAt(Instant.now())
                    .build();
            userRepository.save(admin);
            log.info("Default admin user created with username: {}", defaultAdminUsername);
        } else {
            log.info("Admin user '{}' already exists", defaultAdminUsername);
        }
    }
}
