package com.dorm.controller;
import com.dorm.entity.Notice;
import com.dorm.repository.NoticeRepository;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api/notices")
public class NoticeController extends CrudController<Notice, NoticeRepository> {
    public NoticeController(NoticeRepository repo) { super(repo, Notice.class); }
}
