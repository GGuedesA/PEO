package com.PASN.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.PASN.model.Class;
import com.PASN.repository.ClassRatingRepository;
import com.PASN.repository.ClassRepository;

@Service
@SuppressWarnings("null")
public class ClassService {
    
    @Autowired
    private ClassRepository repository;

    @Autowired 
    private ClassRatingRepository ratingRepository;

    public List<Class> getAll() {
        return repository.findAll();
    }
    
    public Class getById(Long id) {
        return repository.findById(id).orElse(null);
    }

    public Class save(Class object) {
        return repository.save(object);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

    
}
