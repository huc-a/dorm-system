package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 入住记录：入住分配、调宿（变更床位）、退宿均在此留痕 */
@Data @Entity @Table(name = "check_in")
public class CheckIn {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "student_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Student student;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "room_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Room room;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "bed_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Bed bed;
    private LocalDate checkInDate;
    private LocalDate checkOutDate;
    /** 在住 / 已退宿 */
    private String status = "在住";
    private String remark;
    private LocalDateTime createTime = LocalDateTime.now();
}
