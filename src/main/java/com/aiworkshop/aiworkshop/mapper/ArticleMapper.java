package com.aiworkshop.aiworkshop.mapper;

import java.util.List;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.Named;

import com.aiworkshop.aiworkshop.dto.ArticleDto;
import com.aiworkshop.aiworkshop.entity.Article;
import com.aiworkshop.aiworkshop.entity.File;
import com.aiworkshop.aiworkshop.entity.User;

@Mapper(componentModel = "spring")
public interface ArticleMapper {
    
    @Mapping(target = "contentId", source = "article.content.id")
    @Mapping(target = "username", source = "article.user.username")
    @Mapping(target = "imageIds", source = "article.images", qualifiedByName = "toImageIds")
    ArticleDto toDto(Article article);

    @Named("toImageIds")
    default List<Long> toImageIds(List<File> images) {
        return images
                .stream()
                .map(File::getId)
                .toList();
    }

    @Mapping(target = "id", source = "articleDto.id")
    Article toEntity(ArticleDto articleDto, User user, List<File> images, File content);

    @Mapping(target = "user", source = "user")
    @Mapping(target = "user.id", source = "user.id")
    @Mapping(target = "article.id", source = "articleDto.id")
    void update(ArticleDto articleDto, List<File> images, User user, @MappingTarget Article article);

}
