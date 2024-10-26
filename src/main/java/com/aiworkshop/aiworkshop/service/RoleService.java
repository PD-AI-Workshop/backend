package com.aiworkshop.aiworkshop.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.aiworkshop.aiworkshop.dto.RoleDto;
import com.aiworkshop.aiworkshop.dto.UpdateRoleDto;
import com.aiworkshop.aiworkshop.dto.UpdateUserRoleDto;
import com.aiworkshop.aiworkshop.exception.ResourceNotFoundException;
import com.aiworkshop.aiworkshop.mapper.RoleMapper;
import com.aiworkshop.aiworkshop.repository.RoleRepository;
import com.aiworkshop.aiworkshop.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class RoleService {

    private final RoleMapper mapper;
    private final RoleRepository repository;
    private final UserRepository userRepository;

    @Transactional
    public List<RoleDto> getAll() {
        return repository
                .findAll()
                .stream()
                .map(mapper::toDto)
                .toList();
    }

    public RoleDto getById(Long id) {
        return mapper.toDto(repository
                .findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Role not found")));
    }

    public RoleDto create(RoleDto dto) {
        final var ids = dto.getUserIds();
        final var users = userRepository.findAllById(ids);
        final var role = mapper.toEntity(dto, users);
        final var savedRole = repository.save(role);

        return mapper.toDto(savedRole);
    }

    public UpdateRoleDto update(UpdateRoleDto dto) {
        final var id = dto.getId();
        final var role = repository
                .findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Role not found"));

        mapper.update(dto, role);

        repository.save(role);

        return dto;
    }

    public UpdateUserRoleDto updateRole(UpdateUserRoleDto dto) {
        final var id = dto.getUserId();
        final var newRole = dto.getNewRole();
        final var user = userRepository
                .findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found"));
        final var role = repository
                .findByName(newRole)
                .orElseThrow(() -> new ResourceNotFoundException("Role not found"));

        user.setRole(role);

        userRepository.save(user);

        return dto;
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

}
