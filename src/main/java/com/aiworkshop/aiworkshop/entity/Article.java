package com.aiworkshop.aiworkshop.entity;

import java.util.Date;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
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

    @Column(columnDefinition = "TEXT")
    @Schema(description = "Заголовок статьи", example = "Как зарегистрировать ChatGPT?")
    private String title;

    @Column(name = "views")
    @Schema(description = "Количество просмотров статьи", example = "1")
    private Integer views;

    @Column(name = "likes")
    @Schema(description = "Количество лайков статьи", example = "1")
    private Integer likes;

    @Column(name = "created_at")
    @Schema(description = "Дата создания статьи", example = "2022-01-01")
    private Date createdAt;

    @ManyToOne
    @JoinColumn(name = "content_id")
    @Schema(description = "Содержание статьи", example = "1")
    private File content;

    @Column(name = "dislikes")
    @Schema(description = "Количество дизлайков статьи", example = "1")
    private Integer dislikes;

    @ManyToOne
    @JoinColumn(name = "main_image_id")
    @Schema(description = "Изображение статьи", example = "1")
    private File mainImage;

    @OneToMany(mappedBy = "article")
    private List<File> images;

    @ManyToOne
    @JoinColumn(name = "user_id")
    @Schema(description = "Автор статьи")
    private User user;
    
}
