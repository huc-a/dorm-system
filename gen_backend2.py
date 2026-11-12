#!/usr/bin/env python3
import os, textwrap
ROOT = os.path.expanduser("~/workspace/dorm-system/backend")
PKG = "src/main/java/com/dorm"
def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)

BASE = f"{PKG}/entity"
HDR = "package com.dorm.entity;\nimport com.fasterxml.jackson.annotation.*;\nimport jakarta.persistence.*;\nimport lombok.*;\nimport java.time.*;\n"

w(f"{BASE}/SysUser.java", HDR + r'''
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
''')

w(f"{BASE}/Student.java", HDR + r'''
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
''')

w(f"{BASE}/Building.java", HDR + r'''
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
''')

w(f"{BASE}/Room.java", HDR + r'''
/** 宿舍房间 */
@Data @Entity @Table(name = "room")
public class Room {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "building_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Building building;
    @Column(nullable = false, length = 20)
    private String roomNo;
    private Integer floor;
    /** 床位总数 */
    private Integer capacity = 4;
    /** 四人间 / 六人间 / 八人间 */
    private String roomType = "四人间";
    /** 男 / 女 */
    private String gender;
    /** 设施描述，如 独卫、空调、阳台 */
    private String facilities;
    /** 正常 / 维修中 / 停用 */
    private String status = "正常";
    private String remark;
}
''')

w(f"{BASE}/Bed.java", HDR + r'''
/** 床位 */
@Data @Entity @Table(name = "bed")
public class Bed {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "room_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Room room;
    @Column(nullable = false, length = 20)
    private String bedNo;
    /** 空闲 / 已入住 / 维修 */
    private String status = "空闲";
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "student_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Student student;
}
''')

w(f"{BASE}/CheckIn.java", HDR + r'''
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
''')

w(f"{BASE}/Repair.java", HDR + r'''
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
''')

w(f"{BASE}/Hygiene.java", HDR + r'''
/** 卫生检查 */
@Data @Entity @Table(name = "hygiene")
public class Hygiene {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne(fetch = FetchType.EAGER) @JoinColumn(name = "room_id")
    @JsonIgnoreProperties({"hibernateLazyInitializer","handler"})
    private Room room;
    private String inspector;
    private LocalDate checkDate;
    /** 总分 0-100 */
    private Integer score;
    /** 优秀 / 良好 / 合格 / 不合格 */
    private String grade;
    private Integer groundScore;
    private Integer bedScore;
    private Integer deskScore;
    private Integer bathroomScore;
    @Column(length = 500)
    private String remark;
}
''')

w(f"{BASE}/Visitor.java", HDR + r'''
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
''')

w(f"{BASE}/Fee.java", HDR + r'''
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
''')

w(f"{BASE}/DormLeave.java", HDR + r'''
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
''')

w(f"{BASE}/Notice.java", HDR + r'''
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
''')
print("PART2 DONE")
