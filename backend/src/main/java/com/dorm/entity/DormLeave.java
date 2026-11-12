package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 请假 / 晚归申请 */
@Data @Entity @Table(name = "dorm_leave")
public class DormLeave {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "student_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Student student;
    /** 请假离校 / 晚归 */
    private String type = "请假离校";
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    @Column(length = 500)
    private String reason;
    /** 待审批 / 已批准 / 已驳回 */
    private String status = "待审批";
    private String approver;
    @Column(length = 300)
    private String approveRemark;
    private LocalDateTime createTime = LocalDateTime.now();
}
