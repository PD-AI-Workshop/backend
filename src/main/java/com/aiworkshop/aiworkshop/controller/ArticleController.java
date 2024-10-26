package com.aiworkshop.aiworkshop.controller;

import java.util.List;

import org.springframework.http.MediaType;
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

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
@RequestMapping("article")
@Tag(name = "Методы для работы с статьями", description = "Методы для получения статей, создания статьи, обновления статьи и удаления статьи")
public class ArticleController {

    private final ArticleService service;

    @GetMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Список статей получены", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = ArticleDto.class))))
    @Operation(summary = "Получить список статей", description = "Возвращает список DTO всех статей")
    public List<ArticleDto> getAll() {
        return service.getAll();
    }

    @GetMapping("{id}")
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Статья получена", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = ArticleDto.class))))
    @Operation(summary = "Получить статью по ID", description = "Возвращает DTO статьи по ID")
    public ArticleDto getById(@PathVariable Long id) {
        return service.getById(id);
    }

    @PostMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Статья создана", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = ArticleDto.class))))
    @Operation(summary = "Создать статью", description = "Возвращает DTO созданной статьи")
    public ArticleDto create(@RequestBody ArticleDto dto) {
        return service.create(dto);
    }

    @PutMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Статья обновлена", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = ArticleDto.class))))
    @Operation(summary = "Обновить статью", description = "Возвращает DTO обновленной статьи")
    public ArticleDto update(@RequestBody ArticleDto dto) {
        return service.update(dto);
    }

    @DeleteMapping("{id}")
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Статья удалена", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = ArticleDto.class))))
    @Operation(summary = "Удалить статью", description = "Удаляет статью по ID")
    public void delete(@PathVariable Long id) {
        service.delete(id);
    }

}
