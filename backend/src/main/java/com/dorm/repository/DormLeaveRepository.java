package com.dorm.repository;
import com.dorm.entity.DormLeave;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.*;
public interface DormLeaveRepository extends JpaRepository<DormLeave, Long>, JpaSpecificationExecutor<DormLeave> {
    List<DormLeave> findByStudentId(Long studentId);
}
