package com.aiworkshop.aiworkshop.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SignUpDto {

    @Schema(description = "Имя пользователя", example = "login")
    private String username;
    
    @Schema(description = "Email пользователя", example = "email")
    private String email;

    @Schema(description = "Пароль пользователя", example = "password")
    private String password;

}
