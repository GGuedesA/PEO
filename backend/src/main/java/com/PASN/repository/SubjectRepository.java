package com.PASN.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.PASN.model.Subject;

public interface SubjectRepository extends JpaRepository<Subject, Long>{
    
}

