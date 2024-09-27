package com.aiworkshop.aiworkshop.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.aiworkshop.aiworkshop.entity.Role;

public interface RoleRepository extends JpaRepository<Role, Long> {

    Optional<Role> findByName(String name);

}
