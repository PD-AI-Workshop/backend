package com.aiworkshop.aiworkshop.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class UpdateRoleDto {
    
    @Schema(description = "ID роли", example = "1")
    private Long id;

    @Schema(description = "Название роли", example = "ROLE_USER")
    private String name;

}
