package com.PASN.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.PASN.model.Teacher;
import com.PASN.repository.TeacherRatingRepository;
import com.PASN.repository.TeacherRepository;

@Service
@SuppressWarnings("null")
public class TeacherService {
    
    @Autowired
    private TeacherRepository repository;

    @Autowired
    private TeacherRatingRepository ratingRepository;

    public List<Teacher> getAll() {
        return repository.findAll();
    }
    
    public Teacher getById(Long id) {
        return repository.findById(id).orElse(null);
    }

    public Teacher save(Teacher object) {
        return repository.save(object);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
    
}
