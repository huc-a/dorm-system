package com.dorm.repository;
import com.dorm.entity.Repair;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.*;
public interface RepairRepository extends JpaRepository<Repair, Long>, JpaSpecificationExecutor<Repair> {
    List<Repair> findByStudentId(Long studentId);
    long countByStatus(String status);
}
