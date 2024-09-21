package com.aiworkshop.aiworkshop.dto;

import java.util.Date;

import lombok.Data;

@Data
public class ArticleDto {
    private Long id;

    private String title;

    private Integer views;

    private Integer likes;

    private Date createdAt;

    private String content;

    private Integer dislikes;

    private Integer readingTime;

    private Integer imageName;
}
