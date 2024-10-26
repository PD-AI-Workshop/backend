package com.aiworkshop.aiworkshop.dto;

import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class RoleDto {

    @Schema(description = "ID роли", example = "1")
    private Long id;

    @Schema(description = "Название роли", example = "ROLE_USER")
    private String name;

    @Schema(description = "ID пользователей", example = "1")
    private List<Long> userIds;
    
}
