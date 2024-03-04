package com.PASN.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.PASN.model.User;
import com.PASN.repository.UserRepository;

@Service
@SuppressWarnings("null")
public class UserService {
    
    @Autowired
    private UserRepository repository;

    public List<User> getAll() {
        return repository.findAll();
    }
    
    public User getById(Long id) {
        return repository.findById(id).orElse(null);
    }

    public User save(User object) {
        return repository.save(object);
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }

    
}
