package com.aiworkshop.aiworkshop.mapper;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Named;
import org.springframework.data.util.Pair;

import com.aiworkshop.aiworkshop.dto.AuthorsRequestDto;
import com.aiworkshop.aiworkshop.entity.AuthorsRequest;
import com.aiworkshop.aiworkshop.entity.File;

@Mapper(componentModel = "spring")
public interface AuthorsRequestMapper {
    
    @Mapping(target = "resume", source = "files.first")
    @Mapping(target = "messageId", source = "files.second")
    @Mapping(target = "name", source = ".", qualifiedByName = "toName")
    @Mapping(target = "surname", source = ".", qualifiedByName = "toSurname")
    @Mapping(target = "middleName", source = ".", qualifiedByName = "toMiddleName")
    AuthorsRequest toEntity(AuthorsRequestDto dto, Pair<File, File> files);

    @Named("toName")
    default String toName(AuthorsRequestDto dto) {
        return dto.getFullName().split(" ")[0];
    }

    @Named("toMiddleName")
    default String toMiddleName(AuthorsRequestDto dto) {
        return dto.getFullName().split(" ")[1];
    }

    @Named("toSurname")
    default String toSurname(AuthorsRequestDto dto) {
        return dto.getFullName().split(" ")[2];
    }

}
