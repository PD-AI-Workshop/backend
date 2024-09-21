package com.aiworkshop.aiworkshop.controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.aiworkshop.aiworkshop.dto.ArticleDto;
import com.aiworkshop.aiworkshop.service.ArticleService;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
@RequestMapping("article")
public class ArticleController {

    private final ArticleService service;

    @GetMapping
    public List<ArticleDto> getAll() {
        return service.getAll();
    }

    @GetMapping("{id}")
    public ArticleDto getById(@PathVariable Long id) {
        return service.getById(id);
    }

    @PostMapping
    public ArticleDto create(@RequestBody ArticleDto dto) {
        return service.create(dto);
    }

    @PutMapping
    public ArticleDto update(@RequestBody ArticleDto dto) {
        return service.update(dto);
    }

    @DeleteMapping("{id}")
    public void delete(@PathVariable Long id) {
        service.delete(id);
    }

}
