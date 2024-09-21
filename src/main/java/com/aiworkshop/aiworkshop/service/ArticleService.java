package com.aiworkshop.aiworkshop.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.dto.ArticleDto;
import com.aiworkshop.aiworkshop.mapper.ArticleMapper;
import com.aiworkshop.aiworkshop.repository.ArticleRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ArticleService {

    private final ArticleRepository repository;
    private final ArticleMapper mapper;

    public List<ArticleDto> getAll() {
        return repository
                .findAll()
                .stream()
                .map(mapper::toDto)
                .toList();
    }

    public ArticleDto getById(Long id) {
        final var article = repository.findById(id).orElseThrow(() -> new RuntimeException("Article not found"));

        return mapper.toDto(article);
    }

    public ArticleDto create(ArticleDto dto) {
        final var article = mapper.toEntity(dto);
        final var savedArticle = repository.save(article);

        return mapper.toDto(savedArticle);
    }

    public ArticleDto update(ArticleDto dto) {
        final var id = dto.getId();
        final var article = repository.findById(id).orElseThrow(
                () -> new RuntimeException("Article not found"));

        mapper.update(dto, article);

        final var savedArticle = repository.save(article);

        return mapper.toDto(savedArticle);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

}
