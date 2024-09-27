package com.aiworkshop.aiworkshop.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.dto.SignInDto;
import com.aiworkshop.aiworkshop.dto.SignUpDto;
import com.aiworkshop.aiworkshop.dto.TokenResponse;
import com.aiworkshop.aiworkshop.entity.User;
import com.aiworkshop.aiworkshop.repository.RoleRepository;
import com.aiworkshop.aiworkshop.utils.JwtUtils;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService implements UserDetailsService {

    private final JwtUtils utils;
    private final UserService userService;
    @Lazy
    @Autowired
    private AuthenticationManager manager;
    private final BCryptPasswordEncoder encoder;
    private final RoleRepository roleRepository;

    public TokenResponse signIn(SignInDto dto) {
        final var username = dto.getUsername();
        final var password = dto.getPassword();
        final var authorization = manager.authenticate(
                new UsernamePasswordAuthenticationToken(username, password));

        final var jwt = utils.generate(authorization);

        final var response = TokenResponse.builder().token(jwt).build();

        return response;
    }

    public SignUpDto signUp(SignUpDto dto) {
        final var username = dto.getUsername();
        final var password = dto.getPassword();
        final var email = dto.getEmail();

        final var role = roleRepository
                .findByName("ROLE_USER")
                .orElseThrow(() -> new RuntimeException("Role not found"));

        final var isExists = userService.existsByUsername(username);
        final var encryptedPassword = encoder.encode(password);

        if (isExists) {
            throw new RuntimeException("User already exists");
        }

        final var user = User
                .builder()
                .username(username)
                .password(encryptedPassword)
                .email(email)
                .role(role)
                .build();

        userService.create(user);

        return dto;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return userService.getByUsername(username);
    }

}
