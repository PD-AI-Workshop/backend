package com.aiworkshop.aiworkshop.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class ErrorResponse {
    
    @Schema(description = "Код ошибки", example = "400")
    private String message;

    @Schema(description = "URL", example = "/api/article")
    private String url;

    @Schema(description = "Пользователь", example = "login")
    private String user;

    @Schema(description = "Дата", example = "2022-01-01")
    private String date;

}
