package com.aiworkshop.aiworkshop.service;

import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.entity.User;
import com.aiworkshop.aiworkshop.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository repository;

    public User getById(Long id) {
        return repository
                .findById(id)
                .orElseThrow(() -> new RuntimeException("User not found"));
    }

    public User getByUsername(String username) {
        return repository
                .findByUsername(username)
                .orElseThrow(() -> new RuntimeException("User not found"));
    }

    public Boolean existsByUsername(String username) {
        return repository
                .existsByUsername(username)
                .orElseThrow(() -> new RuntimeException("User not found"));
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
