package com.aiworkshop.aiworkshop.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.entity.Article;
import com.aiworkshop.aiworkshop.repository.ArticleRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ArticleService {

    private final ArticleRepository repository;
    
    public List<Article> getAll() {
        return repository.findAll();
    }

    public Article getById(Long id) {
        return repository.findById(id).orElseThrow(() -> new RuntimeException("Article not found"));
    }

    public Article create(Article article) {
        return repository.save(article);
    }

    public Article update(Article article) {
        return repository.save(article);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

}
