package com.aiworkshop.aiworkshop.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

import com.aiworkshop.aiworkshop.dto.FileDto;
import com.aiworkshop.aiworkshop.entity.File;

@Mapper(componentModel = "spring")
public interface FileMapper {
    
    @Mapping(target = "articleId", source = "article.id")
    FileDto toDto(File file);

}
