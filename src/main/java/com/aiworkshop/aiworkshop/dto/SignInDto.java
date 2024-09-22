package com.aiworkshop.aiworkshop.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SignInDto {

    @Schema(description = "Имя пользователя", example = "login")
    private String username;

    @Schema(description = "Пароль пользователя", example = "password")
    private String password;

}
