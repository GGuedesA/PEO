package com.PASN.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.PASN.model.Teacher;

public interface TeacherRepository extends JpaRepository<Teacher, Long>{
    
}

