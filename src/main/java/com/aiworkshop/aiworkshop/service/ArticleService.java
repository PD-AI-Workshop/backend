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

    private final ArticleMapper mapper;
    private final UserService userService;
    private final ArticleRepository repository;

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
        final var username = dto.getUsername();
        final var user = userService.getByUsername(username);
        final var article = mapper.toEntity(dto, user);
        final var savedArticle = repository.save(article);

        return mapper.toDto(savedArticle);
    }

    public ArticleDto update(ArticleDto dto) {
        final var id = dto.getId();
        final var username = dto.getUsername();
        final var user = userService.getByUsername(username);
        final var article = repository.findById(id).orElseThrow(
                () -> new RuntimeException("Article not found"));

        mapper.update(dto, user, article);

        final var savedArticle = repository.save(article);

        return mapper.toDto(savedArticle);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

}
