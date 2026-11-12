package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

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
