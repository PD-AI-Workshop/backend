package com.aiworkshop.aiworkshop.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

import com.aiworkshop.aiworkshop.dto.ArticleDto;
import com.aiworkshop.aiworkshop.entity.Article;
import com.aiworkshop.aiworkshop.entity.User;

@Mapper(componentModel = "spring")
public interface ArticleMapper {
    
    @Mapping(target = "username", source = "user.username")
    ArticleDto toDto(Article article);

    @Mapping(target = "id", source = "articleDto.id")
    @Mapping(target = "user.id", source = "user.id")
    @Mapping(target = "user", source = "user")
    Article toEntity(ArticleDto articleDto, User user);

    @Mapping(target = "user", source = "user")
    @Mapping(target = "user.id", source = "user.id")
    @Mapping(target = "article.id", source = "articleDto.id")
    void update(ArticleDto articleDto, User user, @MappingTarget Article article);

}
