package com.dorm.repository;
import com.dorm.entity.Hygiene;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.*;
public interface HygieneRepository extends JpaRepository<Hygiene, Long>, JpaSpecificationExecutor<Hygiene> {
    List<Hygiene> findByRoomId(Long roomId);
}
