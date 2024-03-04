package com.PASN.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
@Table(name = "classes")
public class Class implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, updatable = false)
    private Long id;

    @ManyToOne(optional = false)
    private Teacher teacher;

    @ManyToMany
    @JoinTable(name = "class_students",
        joinColumns = @JoinColumn(name = "class_id"),
        inverseJoinColumns = @JoinColumn(name = "student_id"))
    private List<User> students;

    @Column(nullable = false)
    private String status = "MARCADO";

    @Column(columnDefinition = "DECIMAL(3, 1)")
    private BigDecimal rating;
    
}
