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

w(f"{PKG}/config/DataInitializer.java", r'''
package com.dorm.config;
import com.dorm.entity.*;
import com.dorm.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import java.time.*;
import java.util.*;
/** 首次启动初始化演示数据：账号、楼栋、房间、床位、学生、入住、报修、卫生、访客、水电费、请假、公告 */
@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {
    private final SysUserRepository users;
    private final StudentRepository students;
    private final BuildingRepository buildings;
    private final RoomRepository rooms;
    private final BedRepository beds;
    private final CheckInRepository checkIns;
    private final RepairRepository repairs;
    private final HygieneRepository hygienes;
    private final VisitorRepository visitors;
    private final FeeRepository fees;
    private final DormLeaveRepository leaves;
    private final NoticeRepository notices;
    private final PasswordEncoder encoder;

    @Override
    public void run(String... args) {
        if (users.count() > 0) return;
        log.info("初始化演示数据...");
        // ---------- 账号 ----------
        SysUser admin = user("admin", "admin123", "系统管理员", "ADMIN", "13800000001");
        user("manager", "manager123", "王宿管", "DORM_MANAGER", "13800000002");
        // ---------- 楼栋 / 房间 / 床位 ----------
        Building b1 = building("B01", "1号宿舍楼", "男生宿舍", "张建国", 6);
        Building b2 = building("B02", "2号宿舍楼", "女生宿舍", "李秀英", 6);
        List<Room> allRooms = new ArrayList<>();
        for (Building b : List.of(b1, b2)) {
            boolean male = "男生宿舍".equals(b.getGenderType());
            for (int floor = 1; floor <= 3; floor++) {
                for (int rn = 1; rn <= 4; rn++) {
                    Room r = new Room();
                    r.setBuilding(b); r.setRoomNo(floor + "0" + rn); r.setFloor(floor);
                    r.setCapacity(4); r.setRoomType("四人间"); r.setGender(male ? "男" : "女");
                    r.setFacilities("独卫、空调、阳台、书桌");
                    rooms.save(r); allRooms.add(r);
                    for (int bn = 1; bn <= 4; bn++) {
                        Bed bed = new Bed(); bed.setRoom(r); bed.setBedNo(bn + "号床");
                        beds.save(bed);
                    }
                }
            }
        }
        // ---------- 学生 ----------
        String[][] stuData = {
            {"20230101","陈小明","男","计算机学院","软件工程","软工2301"},
            {"20230102","刘子轩","男","计算机学院","软件工程","软工2301"},
            {"20230103","杨浩然","男","计算机学院","计算机科学与技术","计科2302"},
            {"20230104","赵子豪","男","信息工程学院","电子信息工程","电信2301"},
            {"20230105","周俊杰","男","信息工程学院","通信工程","通信2301"},
            {"20230106","吴天宇","男","机电工程学院","机械设计制造","机制2302"},
            {"20230201","林小雨","女","计算机学院","软件工程","软工2301"},
            {"20230202","黄思琪","女","外国语学院","英语","英语2301"},
            {"20230203","徐梦婷","女","经济管理学院","会计学","会计2302"},
            {"20230204","孙雅婷","女","经济管理学院","市场营销","营销2301"},
            {"20230205","胡欣怡","女","艺术学院","视觉传达设计","视传2301"},
            {"20230206","朱丽娜","女","外国语学院","日语","日语2301"},
        };
        List<Student> stuList = new ArrayList<>();
        for (String[] d : stuData) {
            SysUser u = user(d[0], "123456", d[1], "STUDENT", "139" + d[0].substring(4));
            Student s = new Student();
            s.setStudentNo(d[0]); s.setName(d[1]); s.setGender(d[2]); s.setCollege(d[3]);
            s.setMajor(d[4]); s.setClassName(d[5]); s.setGrade("2023级");
            s.setPhone("139" + d[0].substring(4)); s.setUserId(u.getId());
            students.save(s); stuList.add(s);
        }
        // ---------- 入住：前10名学生依次入住前3间房等 ----------
        List<Bed> freeBeds = beds.findAll().stream().filter(b -> "空闲".equals(b.getStatus())).toList();
        int bi = 0;
        for (int i = 0; i < 10 && bi < freeBeds.size(); i++) {
            Student s = stuList.get(i);
            // 男生住1号楼（床位序号0-47），女生住2号楼（48-95）
            Bed bed = freeBeds.get("男".equals(s.getGender()) ? bi : 48 + (bi - 6 >= 0 ? bi - 6 : bi));
            if ("已入住".equals(bed.getStatus())) continue;
            bed.setStatus("已入住"); bed.setStudent(s); beds.save(bed);
            CheckIn ci = new CheckIn();
            ci.setStudent(s); ci.setRoom(bed.getRoom()); ci.setBed(bed);
            ci.setCheckInDate(LocalDate.of(2026, 9, 1)); ci.setStatus("在住");
            checkIns.save(ci); bi++;
        }
        // ---------- 报修 ----------
        repair(stuList.get(0), allRooms.get(0), "水龙头漏水", "卫生间水龙头关不紧，持续滴水", "水电", "高", "处理中", "张维修");
        repair(stuList.get(2), allRooms.get(0), "宿舍门锁损坏", "门锁把手松动，关门后容易自动弹开", "门窗", "紧急", "待处理", null);
        repair(stuList.get(6), allRooms.get(12), "空调不制冷", "空调开机后只吹风不制冷", "水电", "普通", "已完成", "李维修");
        repair(stuList.get(8), allRooms.get(13), "椅子损坏", "书桌椅一条腿断裂", "家具", "低", "待处理", null);
        // ---------- 卫生检查 ----------
        hygiene(allRooms.get(0), "王宿管", 92, "地面干净，物品摆放整齐");
        hygiene(allRooms.get(1), "王宿管", 78, "地面基本干净，桌面略乱");
        hygiene(allRooms.get(12), "李秀英", 96, "整体优秀，可评文明宿舍");
        hygiene(allRooms.get(13), "李秀英", 65, "卫生间有异味，需整改");
        // ---------- 访客 ----------
        Visitor v = new Visitor();
        v.setVisitorName("陈建国"); v.setVisitorPhone("13711112222"); v.setVisitedStudent(stuList.get(0));
        v.setRoom(allRooms.get(0)); v.setVisitTime(LocalDateTime.now().minusHours(2));
        v.setReason("家长探望"); v.setStatus("在访"); visitors.save(v);
        // ---------- 水电费 ----------
        for (int i = 0; i < 6; i++) {
            Fee f = new Fee();
            f.setRoom(allRooms.get(i)); f.setPeriod("2026-10");
            f.setElectricityUsage(80.0 + i * 13); f.setWaterUsage(6.0 + i);
            f.setElectricityFee(Math.round((80.0 + i * 13) * 0.55 * 100) / 100.0);
            f.setWaterFee(Math.round((6.0 + i) * 3.5 * 100) / 100.0);
            f.setTotalAmount(Math.round((f.getElectricityFee() + f.getWaterFee()) * 100) / 100.0);
            f.setStatus(i % 2 == 0 ? "已缴费" : "未缴费");
            f.setDueDate(LocalDate.of(2026, 11, 15));
            if ("已缴费".equals(f.getStatus())) f.setPayTime(LocalDateTime.now().minusDays(2));
            fees.save(f);
        }
        // ---------- 请假 ----------
        DormLeave lv = new DormLeave();
        lv.setStudent(stuList.get(1)); lv.setType("请假离校");
        lv.setStartTime(LocalDateTime.of(2026, 11, 14, 8, 0)); lv.setEndTime(LocalDateTime.of(2026, 11, 16, 20, 0));
        lv.setReason("回家探亲"); lv.setStatus("待审批"); leaves.save(lv);
        DormLeave lv2 = new DormLeave();
        lv2.setStudent(stuList.get(6)); lv2.setType("晚归");
        lv2.setStartTime(LocalDateTime.of(2026, 11, 10, 22, 30)); lv2.setEndTime(LocalDateTime.of(2026, 11, 10, 23, 30));
        lv2.setReason("社团活动排练"); lv2.setStatus("已批准"); lv2.setApprover("王宿管"); leaves.save(lv2);
        // ---------- 公告 ----------
        notice("关于开展宿舍安全大检查的通知", "本周五下午14:00起，后勤处将联合保卫处对全校宿舍开展安全大检查，请各宿舍提前整理内务，严禁使用违章电器。", "宿舍通知", true);
        notice("停水通知", "因市政管网维修，11月13日 8:00-12:00 全校宿舍停水，请提前储水。", "停水停电", true);
        notice("十月卫生评比结果通报", "十月卫生评比中，1号楼101、2号楼101宿舍获评文明宿舍，特此通报。", "卫生通报", false);
        log.info("演示数据初始化完成");
    }
    private SysUser user(String username, String pwd, String realName, String role, String phone) {
        SysUser u = new SysUser();
        u.setUsername(username); u.setPassword(encoder.encode(pwd));
        u.setRealName(realName); u.setRole(role); u.setPhone(phone);
        return users.save(u);
    }
    private Building building(String code, String name, String genderType, String manager, int floors) {
        Building b = new Building();
        b.setCode(code); b.setName(name); b.setGenderType(genderType);
        b.setManagerName(manager); b.setManagerPhone("13800000002"); b.setFloors(floors);
        b.setAddress("校园生活区"); return buildings.save(b);
    }
    private void repair(Student s, Room r, String title, String desc, String cat, String pri, String status, String repairer) {
        Repair rp = new Repair();
        rp.setStudent(s); rp.setRoom(r); rp.setTitle(title); rp.setDescription(desc);
        rp.setCategory(cat); rp.setPriority(pri); rp.setStatus(status); rp.setRepairer(repairer);
        if ("已完成".equals(status)) { rp.setResult("已维修完成，验收正常"); rp.setFinishTime(LocalDateTime.now().minusDays(1)); }
        repairs.save(rp);
    }
    private void hygiene(Room r, String inspector, int score, String remark) {
        Hygiene h = new Hygiene();
        h.setRoom(r); h.setInspector(inspector); h.setCheckDate(LocalDate.now().minusDays(3));
        h.setScore(score);
        h.setGrade(score >= 90 ? "优秀" : score >= 80 ? "良好" : score >= 60 ? "合格" : "不合格");
        h.setGroundScore(score); h.setBedScore(Math.max(0, score - 2)); h.setDeskScore(Math.max(0, score - 4)); h.setBathroomScore(Math.max(0, score - 6));
        h.setRemark(remark); hygienes.save(h);
    }
    private void notice(String title, String content, String type, boolean top) {
        Notice n = new Notice();
        n.setTitle(title); n.setContent(content); n.setType(type); n.setTop(top); n.setPublisher("后勤处");
        notices.save(n);
    }
}
''')
print("PART5 DONE")
