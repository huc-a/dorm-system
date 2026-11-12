package com.dorm.controller;
import com.dorm.entity.Student;
import com.dorm.repository.StudentRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/students")
public class StudentController extends CrudController<Student, StudentRepository> {
    public StudentController(StudentRepository repo) { super(repo, Student.class); }
}
