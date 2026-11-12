package com.dorm.controller;
import com.dorm.entity.Repair;
import com.dorm.repository.RepairRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/repairs")
public class RepairController extends CrudController<Repair, RepairRepository> {
    public RepairController(RepairRepository repo) { super(repo, Repair.class); }
}
