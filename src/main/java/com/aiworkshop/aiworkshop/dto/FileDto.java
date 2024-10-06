package com.aiworkshop.aiworkshop.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class FileDto {
    
    private Long id;

    private String name;

    private String url;

    private String type;

    private Long size;

    private Long articleId;

}
