package com.dorm.controller;
import com.dorm.entity.Hygiene;
import com.dorm.repository.HygieneRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/hygiene")
public class HygieneController extends CrudController<Hygiene, HygieneRepository> {
    public HygieneController(HygieneRepository repo) { super(repo, Hygiene.class); }
}
