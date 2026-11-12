package com.dorm.controller;
import com.dorm.entity.Building;
import com.dorm.repository.BuildingRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/buildings")
public class BuildingController extends CrudController<Building, BuildingRepository> {
    public BuildingController(BuildingRepository repo) { super(repo, Building.class); }
}
