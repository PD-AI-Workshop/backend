package com.aiworkshop.aiworkshop.service;

import java.util.Collections;

import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.entity.User;
import com.aiworkshop.aiworkshop.exception.ResourceNotFoundException;
import com.aiworkshop.aiworkshop.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository repository;

    public User getById(Long id) {
        return repository
                .findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }

    public UserDetails getByUsername(String username) {
        final var user = repository
                .findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        final var password = user.getPassword();
        final var role = user.getRole();

        return new org.springframework.security.core.userdetails.User(
                username,
                password,
                Collections.singletonList(new SimpleGrantedAuthority(role.getName())));
    }

    public User create(User user) {
        return repository.save(user);
    }

    public User update(User user) {
        return repository.save(user);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

}
