package com.aiworkshop.aiworkshop.service;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.dto.SignInDto;
import com.aiworkshop.aiworkshop.dto.SignUpDto;
import com.aiworkshop.aiworkshop.dto.response.TokenResponse;
import com.aiworkshop.aiworkshop.entity.User;
import com.aiworkshop.aiworkshop.exception.ResourceNotFoundException;
import com.aiworkshop.aiworkshop.exception.UserAlreadyExistsException;
import com.aiworkshop.aiworkshop.repository.RoleRepository;
import com.aiworkshop.aiworkshop.repository.UserRepository;
import com.aiworkshop.aiworkshop.utils.JwtUtils;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final JwtUtils utils;
    private final UserRepository userRepository;
    private final AuthenticationManager manager;
    private final BCryptPasswordEncoder encoder;
    private final RoleRepository roleRepository;

    public TokenResponse signIn(SignInDto dto) {
        final var username = dto.getUsername();
        final var password = dto.getPassword();
        final var usernamePasswordAuthenticationToken = new UsernamePasswordAuthenticationToken(username, password);
        final var authorization = manager.authenticate(usernamePasswordAuthenticationToken);
        final var jwt = utils.generate(authorization);

        return TokenResponse
                .builder()
                .token(jwt)
                .build();
    }

    public SignUpDto signUp(SignUpDto dto) {
        final var username = dto.getUsername();
        final var password = dto.getPassword();
        final var email = dto.getEmail();
        final var role = roleRepository
                .findByName("ROLE_USER")
                .orElseThrow(() -> new ResourceNotFoundException("Role not found"));
        final var isExists = userRepository
                .existsByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        final var encryptedPassword = encoder.encode(password);

        if (Boolean.TRUE.equals(isExists)) {
            throw new UserAlreadyExistsException("User already exists");
        }

        final var user = User
                .builder()
                .username(username)
                .password(encryptedPassword)
                .email(email)
                .role(role)
                .build();

        userRepository.save(user);

        return dto;
    }

}
