package com.aiworkshop.aiworkshop.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.aiworkshop.aiworkshop.dto.SignInDto;
import com.aiworkshop.aiworkshop.dto.SignUpDto;
import com.aiworkshop.aiworkshop.dto.TokenResponse;
import com.aiworkshop.aiworkshop.entity.User;
import com.aiworkshop.aiworkshop.service.AuthService;

import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("auth")
@RequiredArgsConstructor
@Tag(name = "Методы для работы с пользователями", description = "Методы для авторизации, регистрации пользователей")
public class AuthController {

    private final AuthService service;
    
    @PostMapping("/sign-in")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Авторизация пользователя", content = @Content(mediaType = "application/json", schema = @Schema(implementation = String.class)))
    })
    @Operation(summary = "Авторизация пользователя", description = "Возвращает JWT token")
    public TokenResponse signIn(@RequestBody SignInDto dto) {
        return service.signIn(dto);
    }

    @PostMapping("/sign-up")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Регистрация пользователя", content = @Content(mediaType = "application/json", schema = @Schema(implementation = User.class)))
    })
    @Operation(summary = "Регистрация пользователя", description = "Возвращает зарегистрированного пользователя")
    public SignUpDto signUp(@RequestBody SignUpDto dto) {
        return service.signUp(dto);
    }

}
