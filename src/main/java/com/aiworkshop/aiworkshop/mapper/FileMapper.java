package com.aiworkshop.aiworkshop.mapper;

import org.mapstruct.Mapper;

import com.aiworkshop.aiworkshop.dto.FileDto;
import com.aiworkshop.aiworkshop.entity.File;

@Mapper(componentModel = "spring")
public interface FileMapper {
    
    FileDto toDto(File file);

}
