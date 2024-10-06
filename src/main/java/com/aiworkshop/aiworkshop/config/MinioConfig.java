package com.aiworkshop.aiworkshop.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.minio.MinioClient;
import lombok.Data;

@Data
@Configuration
@ConfigurationProperties(prefix = "minio")
public class MinioConfig {

    private String url;
    private String region;
    private String accessKey;
    private String secretKey;

    @Bean
    MinioClient minioClient() throws Exception {

        final var client = MinioClient
                .builder()
                .endpoint(url)
                .credentials(accessKey, secretKey)
                .build();

        return client;

    }

}
