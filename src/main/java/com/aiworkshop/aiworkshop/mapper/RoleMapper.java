package com.aiworkshop.aiworkshop.mapper;

import java.util.List;

import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.Named;

import com.aiworkshop.aiworkshop.dto.RoleDto;
import com.aiworkshop.aiworkshop.dto.UpdateRoleDto;
import com.aiworkshop.aiworkshop.entity.Role;
import com.aiworkshop.aiworkshop.entity.User;

@Mapper(componentModel = "spring")
public interface RoleMapper {

    @Mapping(target = "userIds", source = "role.users", qualifiedByName = "toUserIds")
    RoleDto toDto(Role role);

    @Named("toUserIds")
    default List<Long> toUserIds(List<User> users) {
        return users
                .stream()
                .map(User::getId)
                .toList();
    }

    Role toEntity(RoleDto dto, List<User> users);

    @Mapping(target = "users", ignore = true)
    void update(UpdateRoleDto dto, @MappingTarget Role role);
}