package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

/** 系统用户：管理员 ADMIN / 宿管 DORM_MANAGER / 学生 STUDENT */
@Data @Entity @Table(name = "sys_user")
public class SysUser {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, unique = true, length = 50)
    private String username;
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    @Column(nullable = false)
    private String password;
    private String realName;
    @Column(nullable = false, length = 20)
    private String role;
    private String phone;
    private String email;
    /** 1 启用 0 禁用 */
    private Integer status = 1;
    private LocalDateTime createTime = LocalDateTime.now();
}
