package com.aiworkshop.aiworkshop.service;

import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.aiworkshop.aiworkshop.dto.FileDto;
import com.aiworkshop.aiworkshop.entity.File;
import com.aiworkshop.aiworkshop.mapper.FileMapper;
import com.aiworkshop.aiworkshop.repository.ArticleRepository;
import com.aiworkshop.aiworkshop.repository.FileRepository;

import io.minio.GetPresignedObjectUrlArgs;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import io.minio.RemoveObjectArgs;
import io.minio.http.Method;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class FileService {

    private final FileMapper mapper;
    private final MinioClient minioClient;
    private final FileRepository repository;
    private final ArticleRepository articleRepository;

    public List<FileDto> getAll() {
        return repository
                .findAll()
                .stream()
                .map(mapper::toDto)
                .toList();
    }

    public FileDto getById(Long id) {
        final var file = repository
                .findById(id)
                .orElseThrow(() -> new RuntimeException("File not found"));

        return mapper.toDto(file);
    }

    public FileDto create(MultipartFile incomingFile) {
        try {
            final var name = incomingFile.getOriginalFilename();
            final var type = incomingFile.getContentType();
            final var size = incomingFile.getSize();
            final var inputStream = incomingFile.getInputStream();

            minioClient.putObject(
                    PutObjectArgs
                            .builder()
                            .bucket("aiworkshop")
                            .object(name)
                            .contentType(type)
                            .stream(inputStream, inputStream.available(), -1)
                            .build());

            final var url = minioClient.getPresignedObjectUrl(
                    GetPresignedObjectUrlArgs
                            .builder()
                            .bucket("aiworkshop")
                            .method(Method.GET)
                            .object(name)
                            .build());

            final var file = File
                    .builder()
                    .name(name)
                    .url(url)
                    .type(type)
                    .size(size)
                    .build();

            final var savedFile = repository.save(file);

            return mapper.toDto(savedFile);
        }

        catch (Exception e) {
            e.printStackTrace();
            return null;
        }

    }

    public void updateAll(Long articleId, List<Long> fileIds) {

        final var files = repository.findAllById(fileIds);

        final var article = articleRepository
                .findById(articleId)
                .orElseThrow(() -> new RuntimeException("Article not found"));

        files.forEach(f -> f.setArticle(article));

        repository.saveAll(files);

    }

    public void delete(Long id) {
        final var file = repository
                .findById(id)
                .orElseThrow(() -> new RuntimeException("File not found"));

        final var name = file.getName();

        try {
            minioClient.removeObject(
                    RemoveObjectArgs
                            .builder()
                            .bucket("aiworkshop")
                            .object(name)
                            .build());

            repository.delete(file);
        }

        catch (Exception e) {
            e.printStackTrace();
        }

    }

}
