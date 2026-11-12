package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 宿舍楼 */
@Data @Entity @Table(name = "building")
public class Building {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, unique = true, length = 20)
    private String code;
    @Column(nullable = false, length = 50)
    private String name;
    private Integer floors;
    /** 男生宿舍 / 女生宿舍 / 混合宿舍 */
    private String genderType;
    private String managerName;
    private String managerPhone;
    private String address;
    private String remark;
}
