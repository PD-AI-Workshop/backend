package com.aiworkshop.aiworkshop.dto;

import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ArticleDto {

    @Schema(description = "ID статьи", example = "1")
    private Long id;

    @Schema(description = "Заголовок статьи", example = "title")
    private String title;

    @Schema(description = "Количество просмотров статьи", example = "1")
    private Integer views;

    @Schema(description = "Количество лайков статьи", example = "1")
    private Integer likes;

    @Schema(description = "Дата создания статьи", example = "2022-01-01")
    private Date createdAt;

    @Schema(description = "Содержание статьи", example = "content")
    private String content;

    @Schema(description = "Количество дизлайков статьи", example = "1")
    private Integer dislikes;

    @Schema(description = "Время чтения статьи", example = "1")
    private Integer readingTime;

    @Schema(description = "Изображение статьи", example = "1")
    private Integer imageName;
}
