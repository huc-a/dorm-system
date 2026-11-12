package com.dorm.controller;
import com.dorm.entity.Bed;
import com.dorm.repository.BedRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/beds")
public class BedController extends CrudController<Bed, BedRepository> {
    public BedController(BedRepository repo) { super(repo, Bed.class); }
}
