package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 学生基本信息 */
@Data @Entity @Table(name = "student")
public class Student {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, unique = true, length = 20)
    private String studentNo;
    @Column(nullable = false, length = 50)
    private String name;
    /** 男 / 女 */
    private String gender;
    private String college;
    private String major;
    private String className;
    private String grade;
    private String phone;
    private String email;
    private String idCard;
    private String homeAddress;
    /** 在读 / 毕业 / 休学 */
    private String status = "在读";
    /** 关联登录账号，可为空 */
    private Long userId;
    private LocalDateTime createTime = LocalDateTime.now();
}
