package com.aiworkshop.aiworkshop.entity;

import java.util.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "article")
public class Article {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    private Integer views;

    private Integer likes;

    private Date createdAt;

    @Column(columnDefinition = "TEXT")
    private String content;

    private Integer dislikes;

    private Integer readingTime;

    private Integer imageName;

}
