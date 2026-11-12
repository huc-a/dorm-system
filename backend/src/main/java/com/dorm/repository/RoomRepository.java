package com.dorm.repository;
import com.dorm.entity.Room;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.*;
public interface RoomRepository extends JpaRepository<Room, Long>, JpaSpecificationExecutor<Room> {
    List<Room> findByBuildingId(Long buildingId);
    long countByBuildingId(Long buildingId);
}
