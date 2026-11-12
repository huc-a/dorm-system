package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 通知公告 */
@Data @Entity @Table(name = "notice")
public class Notice {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, length = 100)
    private String title;
    @Column(length = 5000)
    private String content;
    /** 系统公告 / 宿舍通知 / 卫生通报 / 停水停电 */
    private String type = "宿舍通知";
    private String publisher;
    private Boolean top = false;
    private LocalDateTime publishTime = LocalDateTime.now();
}
