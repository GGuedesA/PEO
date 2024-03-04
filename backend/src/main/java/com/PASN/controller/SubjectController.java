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

import com.PASN.model.Subject;
import com.PASN.service.SubjectService;

@RestController
@RequestMapping("/subject")
public class SubjectController {
    
    @Autowired
    private SubjectService service;

    @GetMapping("/")
    public ResponseEntity<List<Subject>> getAll() {
        List<Subject> allSubjects = service.getAll();
        return new ResponseEntity<>(allSubjects, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Subject> getById(@PathVariable Long id) {
        Subject instance = service.getById(id);
        return new ResponseEntity<>(instance, HttpStatus.OK);
    }

    @PostMapping("/")
    public ResponseEntity<Subject> insert(@RequestBody Subject object) {
        Subject instance = service.save(object);
        return new ResponseEntity<>(instance, HttpStatus.CREATED);
    }

    @PutMapping("/")
    public ResponseEntity<Subject> update(@RequestBody Subject object) {
        Subject instance = service.save(object);
        return new ResponseEntity<>(instance, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> delete(@PathVariable Long id) {
        service.delete(id);
        return new ResponseEntity<>(HttpStatus.OK);
    }
}
