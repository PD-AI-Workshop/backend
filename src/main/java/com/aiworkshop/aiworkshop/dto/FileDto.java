package com.aiworkshop.aiworkshop.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class FileDto {
    
    @Schema(description = "ID файла", example = "1")
    private Long id;

    @Schema(description = "Название файла", example = "image.png")
    private String name;

    @Schema(description = "URL файла", example = "image.png")
    private String url;

    @Schema(description = "Тип файла", example = "png")
    private String type;

    @Schema(description = "Размер файла", example = "1")
    private Long size;

    @Schema(description = "ID статьи", example = "1")
    private Long articleId;

}
