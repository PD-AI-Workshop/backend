package com.aiworkshop.aiworkshop.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.aiworkshop.aiworkshop.entity.AuthorsRequest;

public interface AuthorsRequestRepository extends JpaRepository<AuthorsRequest, Long> {
}
