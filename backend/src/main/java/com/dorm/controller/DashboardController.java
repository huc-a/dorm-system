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
