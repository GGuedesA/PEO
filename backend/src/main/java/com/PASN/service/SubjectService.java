package com.PASN.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.PASN.model.Subject;
import com.PASN.repository.SubjectRepository;

@Service
@SuppressWarnings("null")
public class SubjectService {
    
    @Autowired
    private SubjectRepository repository;

    public List<Subject> getAll() {
        return repository.findAll();
    }
    
    public Subject getById(Long id) {
        return repository.findById(id).orElse(null);
    }

    public Subject save(Subject object) {
        return repository.save(object);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

    
}
