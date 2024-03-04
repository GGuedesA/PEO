package com.PASN.model;

import java.io.Serializable;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
@Table(name = "teachers_ratings")
public class TeacherRating implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(nullable = false, updatable = false)
    private Long id;

    @ManyToOne(optional = false)
    private Class classRated;

    @ManyToOne(optional = false)
    private User student;

    @Column
    private String comment;

    @Column(nullable = false)
    private Integer rating; 

    @Column(nullable = false)
    private String rating_date;

}
