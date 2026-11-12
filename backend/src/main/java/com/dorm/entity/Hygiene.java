package com.dorm.entity;
import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.*;
import java.time.*;

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
