package com.aiworkshop.aiworkshop.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.aiworkshop.aiworkshop.dto.ArticleDto;
import com.aiworkshop.aiworkshop.exception.ResourceNotFoundException;
import com.aiworkshop.aiworkshop.mapper.ArticleMapper;
import com.aiworkshop.aiworkshop.repository.ArticleRepository;
import com.aiworkshop.aiworkshop.repository.FileRepository;
import com.aiworkshop.aiworkshop.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ArticleService {

    private final ArticleMapper mapper;
    private final FileService fileService;
    private final ArticleRepository repository;
    private final FileRepository fileRepository;
    private final UserRepository userRepository;

    public List<ArticleDto> getAll() {
        return repository
                .findAll()
                .stream()
                .map(mapper::toDto)
                .toList();
    }

    public ArticleDto getById(Long id) {
        final var article = repository
                .findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Article not found"));

        return mapper.toDto(article);
    }

    public ArticleDto create(ArticleDto dto) {
        final var username = dto.getUsername();
        final var imageIds = dto.getImageIds();
        final var contentId = dto.getContentId();
        final var isEmpty = imageIds.isEmpty();

        if (isEmpty) {
            throw new ResourceNotFoundException("Image not found");
        }

        final var user = userRepository
                .findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        final var images = fileRepository.findAllById(imageIds);
        final var article = mapper.toEntity(dto, user, images);
        final var savedArticle = repository.save(article);
        final var id = savedArticle.getId();
        final var content = fileRepository
                .findById(contentId)
                .orElseThrow(() -> new ResourceNotFoundException("Content not found"));

        content.setArticle(savedArticle);
        fileRepository.save(content);
        fileService.updateAll(id, imageIds);

        return mapper.toDto(savedArticle);
    }

    public ArticleDto update(ArticleDto dto) {
        final var id = dto.getId();
        final var username = dto.getUsername();
        final var user = userRepository
                .findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        final var article = repository
                .findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Article not found"));
        final var images = fileRepository.findAllById(dto.getImageIds());

        mapper.update(dto, images, user, article);

        final var savedArticle = repository.save(article);

        return mapper.toDto(savedArticle);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

}
