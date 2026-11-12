package com.dorm.controller;
import com.dorm.entity.Fee;
import com.dorm.repository.FeeRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/fees")
public class FeeController extends CrudController<Fee, FeeRepository> {
    public FeeController(FeeRepository repo) { super(repo, Fee.class); }
}
