package com.dorm.controller;
import com.dorm.entity.Room;
import com.dorm.repository.RoomRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/rooms")
public class RoomController extends CrudController<Room, RoomRepository> {
    public RoomController(RoomRepository repo) { super(repo, Room.class); }
}
