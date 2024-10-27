package com.aiworkshop.aiworkshop.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AuthorsRequestDto {

    private Long id;
    
    private String fullName;

    private Long resumeId;

    private Long messageId;

    private Long userId;

}
