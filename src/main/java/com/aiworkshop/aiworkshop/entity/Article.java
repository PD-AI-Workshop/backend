package com.aiworkshop.aiworkshop.entity;

import java.util.Date;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "articles")
@Schema(description = "Статья")
public class Article {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Schema(description = "ID статьи", example = "1")
    private Long id;

    @Schema(description = "Заголовок статьи", example = "Как зарегестрировать ChatGPT?")
    private String title;

    @Schema(description = "Количество просмотров статьи", example = "1")
    private Integer views;

    @Schema(description = "Количество лайков статьи", example = "1")
    private Integer likes;

    @Schema(description = "Дата создания статьи", example = "2022-01-01")
    private Date createdAt;

    @Schema(description = "Содержание статьи", example = "1")
    private Long contentId;

    @Schema(description = "Количество дизлайков статьи", example = "1")
    private Integer dislikes;

    @Schema(description = "Время чтения статьи", example = "1")
    private Integer readingTime;

    @Schema(description = "Изображение статьи", example = "1")
    private Long mainImageId;

    @OneToMany(mappedBy = "article")
    private List<File> images;

    @ManyToOne
    @JoinColumn(name = "user_id")
    @Schema(description = "Автор статьи")
    private User user;
    
}
