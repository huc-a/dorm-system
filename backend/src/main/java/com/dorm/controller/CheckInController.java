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
    private final StudentRepository students;
    public CheckInController(CheckInRepository repo, BedRepository beds, StudentRepository students) {
        super(repo, CheckIn.class); this.beds = beds; this.checkIns = repo; this.students = students;
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
        Student stu = students.findById(req.studentId).orElseThrow(() -> new BizException("学生不存在"));
        bed.setStatus("已入住"); bed.setStudent(stu); beds.save(bed);
        CheckIn ci = new CheckIn();
        ci.setStudent(stu); ci.setRoom(bed.getRoom()); ci.setBed(bed);
        ci.setCheckInDate(LocalDate.now()); ci.setStatus("在住"); ci.setRemark(req.remark);
        CheckIn saved = checkIns.save(ci);
        return Result.ok(checkIns.findById(saved.getId()).orElse(saved));
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
        CheckIn saved = checkIns.save(ci);
        return Result.ok(checkIns.findById(saved.getId()).orElse(saved));
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
        CheckIn saved = checkIns.save(ci);
        return Result.ok(checkIns.findById(saved.getId()).orElse(saved));
    }
    /** 学生端：我的住宿信息 */
    @GetMapping("/my/{studentId}")
    public Result<CheckIn> my(@PathVariable Long studentId) {
        return Result.ok(checkIns.findByStudentIdAndStatus(studentId, "在住").orElse(null));
    }
}
