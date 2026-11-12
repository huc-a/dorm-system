package com.dorm.controller;
import com.dorm.entity.DormLeave;
import com.dorm.repository.DormLeaveRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/leaves")
public class DormLeaveController extends CrudController<DormLeave, DormLeaveRepository> {
    public DormLeaveController(DormLeaveRepository repo) { super(repo, DormLeave.class); }
}
