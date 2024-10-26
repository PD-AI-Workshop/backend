package com.aiworkshop.aiworkshop.controller;

import java.util.List;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.aiworkshop.aiworkshop.dto.FileDto;
import com.aiworkshop.aiworkshop.service.FileService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("files")
@RequiredArgsConstructor
public class FileController {
    
    private final FileService service; 

    @GetMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Получение списка файлов", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = FileDto.class))))
    @Operation(summary = "Получить список файлов", description = "Возвращает список DTO всех файлов")
    public List<FileDto> getAll() {
        return service.getAll();
    }

    @GetMapping("{id}")
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Получение файла", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = FileDto.class))))
    @Operation(summary = "Получить файл", description = "Возвращает DTO файла по ID")
    public FileDto getById(@PathVariable Long id) {
        return service.getById(id);
    }

    @PostMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Создание файла", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE, schema = @Schema(implementation = FileDto.class))))
    @Operation(summary = "Создать файл", description = "Возвращает DTO созданного файла")
    public FileDto create(@RequestParam MultipartFile file) {
        return service.create(file);
    }

    @DeleteMapping("{id}")
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Удаление файла", content = @Content(mediaType = MediaType.APPLICATION_JSON_VALUE)))
    @Operation(summary = "Удалить файл", description = "Удаляет файл по ID")
    public void delete(@PathVariable Long id) {
        service.delete(id);
    }

}
