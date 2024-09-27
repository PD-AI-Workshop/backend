package com.aiworkshop.aiworkshop.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class UpdateUserRoleDto {
    
    @Schema(description = "ID пользователя", example = "1")
    private Long userId;

    @Schema(description = "Новая роль пользователя", example = "ROLE_USER")
    private String newRole;

}
