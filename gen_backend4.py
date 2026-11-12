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
C = f"{PKG}/controller"

w(f"{C}/AuthController.java", r'''
package com.dorm.controller;
import com.dorm.common.*;
import com.dorm.entity.*;
import com.dorm.repository.*;
import com.dorm.security.JwtUtil;
import jakarta.validation.constraints.NotBlank;
import lombok.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
/** 登录 / 注册 / 当前用户 / 修改密码 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {
    private final SysUserRepository users;
    private final StudentRepository students;
    private final PasswordEncoder encoder;
    private final JwtUtil jwt;

    @Data public static class LoginReq { @NotBlank private String username; @NotBlank private String password; }
    @Data public static class RegisterReq {
        @NotBlank private String studentNo; @NotBlank private String name;
        @NotBlank private String password; private String phone; private String gender;
        private String college; private String major; private String className; private String grade;
    }
    @Data public static class ChangePwdReq { private String oldPassword; private String newPassword; }

    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody LoginReq req) {
        SysUser u = users.findByUsername(req.getUsername())
            .orElseThrow(() -> new BizException("用户名或密码错误"));
        if (u.getStatus() != null && u.getStatus() == 0) throw new BizException("账号已被禁用");
        if (!encoder.matches(req.getPassword(), u.getPassword())) throw new BizException("用户名或密码错误");
        String token = jwt.generate(u.getUsername(), u.getRole(), u.getId());
        return Result.ok(Map.of("token", token, "user", u));
    }
    /** 学生自助注册：创建登录账号与学生档案 */
    @PostMapping("/register")
    public Result<SysUser> register(@RequestBody RegisterReq req) {
        if (users.existsByUsername(req.getStudentNo())) throw new BizException("该学号已注册");
        if (students.findByStudentNo(req.getStudentNo()).isPresent()) throw new BizException("该学号档案已存在");
        SysUser u = new SysUser();
        u.setUsername(req.getStudentNo()); u.setPassword(encoder.encode(req.getPassword()));
        u.setRealName(req.getName()); u.setRole("STUDENT"); u.setPhone(req.getPhone());
        users.save(u);
        Student s = new Student();
        s.setStudentNo(req.getStudentNo()); s.setName(req.getName()); s.setGender(req.getGender());
        s.setCollege(req.getCollege()); s.setMajor(req.getMajor()); s.setClassName(req.getClassName());
        s.setGrade(req.getGrade()); s.setPhone(req.getPhone()); s.setUserId(u.getId());
        students.save(s);
        return Result.ok(u);
    }
    @GetMapping("/me")
    public Result<Map<String, Object>> me(Authentication auth) {
        SysUser u = users.findByUsername(auth.getName()).orElseThrow(() -> new BizException("用户不存在"));
        Student stu = students.findByUserId(u.getId()).orElse(null);
        return Result.ok(Map.of("user", u, "student", stu == null ? Map.of() : stu));
    }
    @PostMapping("/change-password")
    public Result<Void> changePwd(Authentication auth, @RequestBody ChangePwdReq req) {
        SysUser u = users.findByUsername(auth.getName()).orElseThrow(() -> new BizException("用户不存在"));
        if (!encoder.matches(req.getOldPassword(), u.getPassword())) throw new BizException("原密码不正确");
        u.setPassword(encoder.encode(req.getNewPassword()));
        users.save(u);
        return Result.ok();
    }
}
''')

w(f"{C}/CheckInController.java", r'''
package com.dorm.controller;
import com.dorm.common.*;
import com.dorm.entity.*;
import com.dorm.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import java.time.LocalDate;
/**
 * 入住管理：继承通用分页查询，另提供入住分配 / 调宿 / 退宿三个业务接口，
 * 业务规则：床位必须空闲、学生不能重复在住、退宿后自动释放床位。
 */
@RestController
@RequestMapping("/api/checkins")
public class CheckInController extends CrudController<CheckIn, CheckInRepository> {
    private final BedRepository beds;
    private final CheckInRepository checkIns;
    public CheckInController(CheckInRepository repo, BedRepository beds) {
        super(repo, CheckIn.class); this.beds = beds; this.checkIns = repo;
    }
    @RequiredArgsConstructor
    public static class AssignReq { public Long studentId; public Long bedId; public String remark; }

    @PostMapping("/assign")
    @Transactional
    public Result<CheckIn> assign(@RequestBody AssignReq req) {
        Bed bed = beds.findById(req.bedId).orElseThrow(() -> new BizException("床位不存在"));
        if (!"空闲".equals(bed.getStatus())) throw new BizException("该床位不是空闲状态，无法分配");
        if (checkIns.findByStudentIdAndStatus(req.studentId, "在住").isPresent())
            throw new BizException("该学生已在住，不能重复分配");
        Student stu = new Student(); stu.setId(req.studentId);
        bed.setStatus("已入住"); bed.setStudent(stu); beds.save(bed);
        CheckIn ci = new CheckIn();
        ci.setStudent(stu); ci.setRoom(bed.getRoom()); ci.setBed(bed);
        ci.setCheckInDate(LocalDate.now()); ci.setStatus("在住"); ci.setRemark(req.remark);
        return Result.ok(checkIns.save(ci));
    }
    /** 调宿：释放旧床位，占用新床位，更新入住记录 */
    @PostMapping("/{id}/change-bed")
    @Transactional
    public Result<CheckIn> changeBed(@PathVariable Long id, @RequestBody AssignReq req) {
        CheckIn ci = checkIns.findById(id).orElseThrow(() -> new BizException("入住记录不存在"));
        if (!"在住".equals(ci.getStatus())) throw new BizException("该记录已退宿，不能调宿");
        Bed newBed = beds.findById(req.bedId).orElseThrow(() -> new BizException("新床位不存在"));
        if (!"空闲".equals(newBed.getStatus())) throw new BizException("新床位不是空闲状态");
        Bed oldBed = ci.getBed();
        if (oldBed != null) { oldBed.setStatus("空闲"); oldBed.setStudent(null); beds.save(oldBed); }
        newBed.setStatus("已入住"); newBed.setStudent(ci.getStudent()); beds.save(newBed);
        ci.setBed(newBed); ci.setRoom(newBed.getRoom());
        ci.setRemark((ci.getRemark() == null ? "" : ci.getRemark()) + " [调宿于 " + LocalDate.now() + "]");
        return Result.ok(checkIns.save(ci));
    }
    /** 退宿：记录状态改为已退宿并释放床位 */
    @PostMapping("/{id}/checkout")
    @Transactional
    public Result<CheckIn> checkout(@PathVariable Long id) {
        CheckIn ci = checkIns.findById(id).orElseThrow(() -> new BizException("入住记录不存在"));
        if (!"在住".equals(ci.getStatus())) throw new BizException("该记录已退宿");
        ci.setStatus("已退宿"); ci.setCheckOutDate(LocalDate.now());
        Bed bed = ci.getBed();
        if (bed != null) { bed.setStatus("空闲"); bed.setStudent(null); beds.save(bed); }
        return Result.ok(checkIns.save(ci));
    }
    /** 学生端：我的住宿信息 */
    @GetMapping("/my/{studentId}")
    public Result<CheckIn> my(@PathVariable Long studentId) {
        return Result.ok(checkIns.findByStudentIdAndStatus(studentId, "在住").orElse(null));
    }
}
''')

w(f"{C}/DashboardController.java", r'''
package com.dorm.controller;
import com.dorm.common.Result;
import com.dorm.entity.Room;
import com.dorm.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.*;
/** 首页仪表盘统计：总量、入住率、各楼栋入住、报修状态、最新公告、卫生平均分 */
@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {
    private final StudentRepository students;
    private final BuildingRepository buildings;
    private final RoomRepository rooms;
    private final BedRepository beds;
    private final CheckInRepository checkIns;
    private final RepairRepository repairs;
    private final NoticeRepository notices;
    private final HygieneRepository hygienes;
    private final FeeRepository fees;

    @GetMapping("/stats")
    public Result<Map<String, Object>> stats() {
        Map<String, Object> m = new LinkedHashMap<>();
        long bedTotal = beds.count();
        long bedUsed = beds.findAll().stream().filter(b -> "已入住".equals(b.getStatus())).count();
        m.put("studentCount", students.count());
        m.put("buildingCount", buildings.count());
        m.put("roomCount", rooms.count());
        m.put("bedTotal", bedTotal);
        m.put("bedUsed", bedUsed);
        m.put("bedFree", bedTotal - bedUsed);
        m.put("occupancyRate", bedTotal == 0 ? 0 : Math.round(bedUsed * 1000.0 / bedTotal) / 10.0);
        m.put("checkedInCount", checkIns.findByStatus("在住").size());
        m.put("repairPending", repairs.countByStatus("待处理"));
        m.put("repairProcessing", repairs.countByStatus("处理中"));
        m.put("repairDone", repairs.countByStatus("已完成"));
        m.put("unpaidFeeCount", fees.findAll().stream().filter(f -> "未缴费".equals(f.getStatus())).count());
        m.put("avgHygieneScore", hygienes.findAll().stream().mapToInt(h -> h.getScore() == null ? 0 : h.getScore()).average().orElse(0));
        // 各楼栋入住情况
        List<Map<String, Object>> byBuilding = new ArrayList<>();
        buildings.findAll().forEach(b -> {
            List<Room> rs = rooms.findByBuildingId(b.getId());
            long total = rs.stream().mapToLong(r -> beds.findByRoomId(r.getId()).size()).sum();
            long used = rs.stream().mapToLong(r -> beds.countByRoomIdAndStatus(r.getId(), "已入住")).sum();
            byBuilding.add(Map.of("building", b.getName(), "total", total, "used", used, "free", total - used));
        });
        m.put("byBuilding", byBuilding);
        m.put("latestNotices", notices.findTop5ByOrderByTopDescPublishTimeDesc());
        return Result.ok(m);
    }
}
''')
print("PART4 DONE")
