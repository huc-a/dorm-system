package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 访客登记 */
@Data @Entity @Table(name = "visitor")
public class Visitor {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, length = 50)
    private String visitorName;
    private String visitorPhone;
    private String idCard;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "student_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Student visitedStudent;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "room_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Room room;
    private LocalDateTime visitTime;
    private LocalDateTime leaveTime;
    @Column(length = 300)
    private String reason;
    /** 在访 / 已离开 */
    private String status = "在访";
}
