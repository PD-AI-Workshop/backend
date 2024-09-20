package com.aiworkshop.aiworkshop.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.aiworkshop.aiworkshop.entity.Article;

public interface ArticleRepository extends JpaRepository<Article, Long> {
    
}
