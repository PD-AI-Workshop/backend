package com.aiworkshop.aiworkshop.entity;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "files")
public class File {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Schema(description = "ID файла", example = "1")
    private Long id;

    @Column(name = "name", columnDefinition = "TEXT")
    @Schema(description = "Название файла", example = "image.png")
    private String name;

    @Column(name = "url", columnDefinition = "TEXT")
    @Schema(description = "URL файла", example = "image.png")
    private String url;

    @Column(name = "type")
    @Schema(description = "Тип файла", example = "png")
    private String type;

    @Column(name = "size")
    @Schema(description = "Размер файла", example = "1")
    private Long size;

    @ManyToOne
    @JoinColumn(name = "article_id")
    private Article article;

}
