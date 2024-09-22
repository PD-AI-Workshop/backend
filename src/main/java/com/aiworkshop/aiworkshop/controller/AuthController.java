package com.aiworkshop.aiworkshop.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.aiworkshop.aiworkshop.dto.SignInDto;
import com.aiworkshop.aiworkshop.dto.SignUpDto;
import com.aiworkshop.aiworkshop.entity.User;
import com.aiworkshop.aiworkshop.service.AuthService;


import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService service;
    
    @PostMapping("/signin")
    public String signIn(@RequestBody SignInDto dto) {
        return service.signIn(dto);
    }

    @PostMapping("/signup")
    public User signUp(@RequestBody SignUpDto dto) {
        return service.signUp(dto);
    }

}
