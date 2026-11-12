package com.dorm.repository;
import com.dorm.entity.Bed;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.*;
public interface BedRepository extends JpaRepository<Bed, Long>, JpaSpecificationExecutor<Bed> {
    List<Bed> findByRoomId(Long roomId);
    long countByRoomIdAndStatus(Long roomId, String status);
}
