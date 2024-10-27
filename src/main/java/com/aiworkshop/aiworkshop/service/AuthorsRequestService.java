package com.aiworkshop.aiworkshop.service;

import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.repository.AuthorsRequestRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthorsRequestService {
    
    private final AuthorsRequestRepository repository;

    public List<AuthorsRequestDto> getAll() {
        
    } 

}
