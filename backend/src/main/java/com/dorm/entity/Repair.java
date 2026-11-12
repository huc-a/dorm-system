package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 报修工单 */
@Data @Entity @Table(name = "repair")
public class Repair {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "student_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Student student;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "room_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Room room;
    @Column(nullable = false, length = 100)
    private String title;
    @Column(length = 1000)
    private String description;
    /** 水电 / 家具 / 门窗 / 网络 / 其他 */
    private String category;
    /** 低 / 普通 / 高 / 紧急 */
    private String priority = "普通";
    /** 待处理 / 处理中 / 已完成 / 已关闭 */
    private String status = "待处理";
    private String repairer;
    @Column(length = 500)
    private String result;
    private LocalDateTime createTime = LocalDateTime.now();
    private LocalDateTime finishTime;
}
