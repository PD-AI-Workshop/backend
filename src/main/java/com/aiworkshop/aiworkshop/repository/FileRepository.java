package com.aiworkshop.aiworkshop.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.aiworkshop.aiworkshop.entity.File;

public interface FileRepository extends JpaRepository<File, Long> {
}
