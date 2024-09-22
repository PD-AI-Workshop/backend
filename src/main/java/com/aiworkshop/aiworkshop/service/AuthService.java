package com.aiworkshop.aiworkshop.service;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.dto.SignInDto;
import com.aiworkshop.aiworkshop.dto.SignUpDto;
import com.aiworkshop.aiworkshop.entity.User;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService implements UserDetailsService {

    private final UserService userService;
    private final BCryptPasswordEncoder encoder;

    public String signIn(SignInDto dto) {
        final var username = dto.getUsername();
        final var password = dto.getPassword();

        final var user = userService.getByUsername(username);

        final var isMatches = encoder.matches(password, user.getPassword());

        if (isMatches) {
            return user.getUsername();
        }

        throw new RuntimeException("Wrong password");
    }

    public User signUp(SignUpDto dto) {
        final var username = dto.getUsername();
        final var password = dto.getPassword();
        final var email = dto.getEmail();

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
                .build();

        return userService.create(user);
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return userService.getByUsername(username);
    }

}
