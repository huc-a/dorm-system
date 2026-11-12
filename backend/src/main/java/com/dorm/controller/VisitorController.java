package com.dorm.controller;
import com.dorm.entity.Visitor;
import com.dorm.repository.VisitorRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/visitors")
public class VisitorController extends CrudController<Visitor, VisitorRepository> {
    public VisitorController(VisitorRepository repo) { super(repo, Visitor.class); }
}
