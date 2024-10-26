package com.aiworkshop.aiworkshop.controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.aiworkshop.aiworkshop.dto.RoleDto;
import com.aiworkshop.aiworkshop.dto.UpdateRoleDto;
import com.aiworkshop.aiworkshop.dto.UpdateUserRoleDto;
import com.aiworkshop.aiworkshop.service.RoleService;

import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("roles")
@RequiredArgsConstructor
@Tag(name = "Методы для работы с ролями", description = "Методы для получения всех ролей, получения роли по ID, создание роли, обновление роли у пользователя и удаления роли")
public class RoleController {

    private final RoleService service;
    
    @GetMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Успешное получение всех ролей"))
    @Operation(summary = "Получить список ролей", description = "Возвращает список DTO всех ролей")
    public List<RoleDto> getAll() {
        return service.getAll();
    }

    @GetMapping("{id}")
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Успешное получение роли по ID"))
    @Operation(summary = "Получить роль по ID", description = "Возвращает DTO роли по ID")
    public RoleDto getById(@PathVariable Long id) {
        return service.getById(id);
    }

    @PostMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Успешное создание роли"))
    @Operation(summary = "Создать роль", description = "Возвращает DTO созданной роли")
    public RoleDto create(@RequestBody RoleDto dto) {
        return service.create(dto);
    }

    @PutMapping("user")
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Успешное обновление роли для пользователя"))
    @Operation(summary = "Обновить роль пользователя", description = "Возвращает DTO обновленной роли пользователя")
    public UpdateUserRoleDto updateUsersRole(@RequestBody UpdateUserRoleDto dto) {
        return service.updateRole(dto);
    }

    @PutMapping
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Успешное обновление роли"))
    @Operation(summary = "Обновить роль", description = "Возвращает DTO обновленной роли")
    public UpdateRoleDto update(@RequestBody UpdateRoleDto dto) {
        return service.update(dto);
    }

    @DeleteMapping("{id}")
    @ApiResponses(@ApiResponse(responseCode = "200", description = "Успешное удаление роли по ID"))
    @Operation(summary = "Удалить роль по ID", description = "Удаляет роль по ID")
    public void delete(@PathVariable Long id) {
        service.delete(id);
    }

}
