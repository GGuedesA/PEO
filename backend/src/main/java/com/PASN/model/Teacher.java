package com.PASN.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
@Table(name = "teachers")
public class Teacher implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, updatable = false)
    private Long id;

    @OneToOne(optional = false)
    private User person;

    @Column
    private BigDecimal estimatedPrice;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(name = "TEACHERS_SUBJECTS", 
        joinColumns = @JoinColumn(name = "teacher_id"), 
        inverseJoinColumns = @JoinColumn(name = "subject_id"))
    private List<Subject> subjects;

    @Column(columnDefinition = "DECIMAL(3, 1)")
    private BigDecimal rating;

}
