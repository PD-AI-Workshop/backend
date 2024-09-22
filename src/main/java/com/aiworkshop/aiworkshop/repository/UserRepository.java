package com.aiworkshop.aiworkshop.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.aiworkshop.aiworkshop.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
    
    Optional<User> findByUsername(String username);

    Optional<Boolean> existsByUsername(String username);
    
}
