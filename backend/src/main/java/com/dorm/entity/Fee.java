package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 水电费账单（按房间按月） */
@Data @Entity @Table(name = "fee")
public class Fee {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "room_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Room room;
    /** 账期，如 2026-09 */
    @Column(length = 10)
    private String period;
    private Double electricityUsage;
    private Double waterUsage;
    private Double electricityFee;
    private Double waterFee;
    private Double totalAmount;
    /** 未缴费 / 已缴费 */
    private String status = "未缴费";
    private LocalDate dueDate;
    private LocalDateTime payTime;
}
