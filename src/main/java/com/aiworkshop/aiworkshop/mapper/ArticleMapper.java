package com.aiworkshop.aiworkshop.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.MappingTarget;

import com.aiworkshop.aiworkshop.dto.ArticleDto;
import com.aiworkshop.aiworkshop.entity.Article;

@Mapper(componentModel = "spring")
public interface ArticleMapper {
    
    ArticleDto toDto(Article article);

    Article toEntity(ArticleDto articleDto);

    void update(ArticleDto articleDto, @MappingTarget Article article);

}
