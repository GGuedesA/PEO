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

import com.PASN.model.Class;
import com.PASN.service.ClassService;

@RestController
@RequestMapping("/class")
public class ClassController {
    
    @Autowired
    private ClassService service;

    @GetMapping("/")
    public ResponseEntity<List<Class>> getAll() {
        List<Class> allClasss = service.getAll();
        return new ResponseEntity<>(allClasss, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Class> getById(@PathVariable Long id) {
        Class instance = service.getById(id);
        return new ResponseEntity<>(instance, HttpStatus.OK);
    }

    @PostMapping("/")
    public ResponseEntity<Class> insert(@RequestBody Class object) {
        Class instance = service.save(object);
        return new ResponseEntity<>(instance, HttpStatus.CREATED);
    }

    @PutMapping("/")
    public ResponseEntity<Class> update(@RequestBody Class object) {
        Class instance = service.save(object);
        return new ResponseEntity<>(instance, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> delete(@PathVariable Long id) {
        service.delete(id);
        return new ResponseEntity<>(HttpStatus.OK);
    }
}