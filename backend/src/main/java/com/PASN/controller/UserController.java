package com.PASN.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.PASN.model.User;
import com.PASN.service.UserService;

@RestController
@RequestMapping("/user")
public class UserController {
    
    @Autowired
    private UserService service;

    @GetMapping("/")
    public ResponseEntity<List<User>> getAll() {
        List<User> allUsers = service.getAll();
        return new ResponseEntity<>(allUsers, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getById(@PathVariable Long id) {
        User instance = service.getById(id);
        return new ResponseEntity<>(instance, HttpStatus.OK);
    }

    @PostMapping("/")
    public ResponseEntity<User> insert(@RequestBody User object) {
        User instance = service.save(object);
        return new ResponseEntity<>(instance, HttpStatus.CREATED);
    }

    @PutMapping("/")
    public ResponseEntity<User> update(@RequestBody User object) {
        User instance = service.save(object);
        return new ResponseEntity<>(instance, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> delete(@PathVariable Long id) {
        service.delete(id);
        return new ResponseEntity<>(HttpStatus.OK);
    }
}
