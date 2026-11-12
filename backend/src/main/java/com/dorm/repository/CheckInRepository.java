package com.dorm.repository;
import com.dorm.entity.CheckIn;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.*;
public interface CheckInRepository extends JpaRepository<CheckIn, Long>, JpaSpecificationExecutor<CheckIn> {
    Optional<CheckIn> findByStudentIdAndStatus(Long studentId, String status);
    List<CheckIn> findByStatus(String status);
}
