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

import com.PASN.model.Teacher;
import com.PASN.service.TeacherService;

@RestController
@RequestMapping("/teacher")
public class TeacherController {
    
    @Autowired
    private TeacherService service;

    @GetMapping("/")
    public ResponseEntity<List<Teacher>> getAll() {
        List<Teacher> allTeachers = service.getAll();
        return new ResponseEntity<>(allTeachers, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Teacher> getById(@PathVariable Long id) {
        Teacher instance = service.getById(id);
        return new ResponseEntity<>(instance, HttpStatus.OK);
    }

    @PostMapping("/")
    public ResponseEntity<Teacher> insert(@RequestBody Teacher object) {
        Teacher instance = service.save(object);
        return new ResponseEntity<>(instance, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Teacher> update(@PathVariable Long id, @RequestBody Teacher partialTeacher) {
        Teacher existingTeacher = service.getById(id);

    if (existingTeacher == null) {
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }

    if (partialTeacher.getPerson() != null) {
        existingTeacher.setPerson(partialTeacher.getPerson());
    }

    if (partialTeacher.getEstimatedPrice() != null) {
        existingTeacher.setEstimatedPrice(partialTeacher.getEstimatedPrice());
    }

    if (partialTeacher.getSubjects() != null) {
        existingTeacher.setSubjects(partialTeacher.getSubjects());
    }

    if (partialTeacher.getRating() != null) {
        existingTeacher.setRating(partialTeacher.getRating());
    }

    Teacher updatedTeacher = service.save(existingTeacher);

    return new ResponseEntity<>(updatedTeacher, HttpStatus.OK);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> delete(@PathVariable Long id) {
        service.delete(id);
        return new ResponseEntity<>(HttpStatus.OK);
    }
}
