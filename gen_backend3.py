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

R = f"{PKG}/repository"
repos = {
 "SysUserRepository": ("SysUser", "Optional<SysUser> findByUsername(String username);\n    boolean existsByUsername(String username);"),
 "StudentRepository": ("Student", "Optional<Student> findByStudentNo(String studentNo);\n    Optional<Student> findByUserId(Long userId);"),
 "BuildingRepository": ("Building", "Optional<Building> findByCode(String code);"),
 "RoomRepository": ("Room", "List<Room> findByBuildingId(Long buildingId);\n    long countByBuildingId(Long buildingId);"),
 "BedRepository": ("Bed", "List<Bed> findByRoomId(Long roomId);\n    long countByRoomIdAndStatus(Long roomId, String status);"),
 "CheckInRepository": ("CheckIn", "Optional<CheckIn> findByStudentIdAndStatus(Long studentId, String status);\n    List<CheckIn> findByStatus(String status);"),
 "RepairRepository": ("Repair", "List<Repair> findByStudentId(Long studentId);\n    long countByStatus(String status);"),
 "HygieneRepository": ("Hygiene", "List<Hygiene> findByRoomId(Long roomId);"),
 "VisitorRepository": ("Visitor", ""),
 "FeeRepository": ("Fee", "List<Fee> findByRoomId(Long roomId);"),
 "DormLeaveRepository": ("DormLeave", "List<DormLeave> findByStudentId(Long studentId);"),
 "NoticeRepository": ("Notice", "List<Notice> findTop5ByOrderByTopDescPublishTimeDesc();"),
}
for name,(ent,extra) in repos.items():
    w(f"{R}/{name}.java", f"""
package com.dorm.repository;
import com.dorm.entity.{ent};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import java.util.*;
public interface {name} extends JpaRepository<{ent}, Long>, JpaSpecificationExecutor<{ent}> {{
    {extra}
}}
""")

C = f"{PKG}/controller"
w(f"{C}/CrudController.java", r'''
package com.dorm.controller;
import com.dorm.common.*;
import jakarta.persistence.criteria.Predicate;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.*;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.web.bind.annotation.*;
import java.lang.reflect.Field;
import java.util.*;
/**
 * 通用 CRUD 控制器基类：子类只需声明实体与仓库，即获得
 * 分页查询（支持任意字符串字段模糊匹配）、全量列表、详情、新增、修改、删除接口。
 */
@RequiredArgsConstructor
public abstract class CrudController<T, R extends JpaRepository<T, Long> & JpaSpecificationExecutor<T>> {
    protected final R repo;
    protected final Class<T> entityClass;

    @GetMapping
    public Result<PageResult<T>> page(@RequestParam(defaultValue = "1") int page,
                                      @RequestParam(defaultValue = "10") int size,
                                      @RequestParam Map<String, String> params) {
        Specification<T> spec = (root, q, cb) -> {
            List<Predicate> ps = new ArrayList<>();
            params.forEach((k, v) -> {
                if (v == null || v.isBlank() || k.equals("page") || k.equals("size")) return;
                try {
                    Field f = findField(entityClass, k);
                    if (f != null && f.getType() == String.class) {
                        ps.add(cb.like(root.get(k), "%" + v + "%"));
                    }
                } catch (Exception ignored) {}
            });
            return cb.and(ps.toArray(new Predicate[0]));
        };
        Page<T> p = repo.findAll(spec, PageRequest.of(page - 1, size, Sort.by(Sort.Direction.DESC, "id")));
        return Result.ok(PageResult.of(p));
    }
    private Field findField(Class<?> c, String name) {
        while (c != null) {
            try { return c.getDeclaredField(name); } catch (NoSuchFieldException e) { c = c.getSuperclass(); }
        }
        return null;
    }
    @GetMapping("/all")
    public Result<List<T>> all() { return Result.ok(repo.findAll(Sort.by(Sort.Direction.ASC, "id"))); }
    @GetMapping("/{id}")
    public Result<T> get(@PathVariable Long id) {
        return Result.ok(repo.findById(id).orElseThrow(() -> new BizException("记录不存在")));
    }
    @PostMapping
    public Result<T> create(@RequestBody T entity) { beforeSave(entity, true); return Result.ok(repo.save(entity)); }
    @PutMapping("/{id}")
    public Result<T> update(@PathVariable Long id, @RequestBody T entity) {
        if (!repo.existsById(id)) throw new BizException("记录不存在");
        setId(entity, id);
        beforeSave(entity, false);
        return Result.ok(repo.save(entity));
    }
    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) { repo.deleteById(id); return Result.ok(); }
    /** 子类业务校验钩子 */
    protected void beforeSave(T entity, boolean isCreate) {}
    private void setId(T entity, Long id) {
        try { Field f = findField(entityClass, "id"); f.setAccessible(true); f.set(entity, id); }
        catch (Exception ignored) {}
    }
}
''')

ctrls = [
 ("StudentController","/api/students","Student","StudentRepository"),
 ("BuildingController","/api/buildings","Building","BuildingRepository"),
 ("RoomController","/api/rooms","Room","RoomRepository"),
 ("BedController","/api/beds","Bed","BedRepository"),
 ("RepairController","/api/repairs","Repair","RepairRepository"),
 ("HygieneController","/api/hygiene","Hygiene","HygieneRepository"),
 ("VisitorController","/api/visitors","Visitor","VisitorRepository"),
 ("FeeController","/api/fees","Fee","FeeRepository"),
 ("DormLeaveController","/api/leaves","DormLeave","DormLeaveRepository"),
 ("NoticeController","/api/notices","Notice","NoticeRepository"),
]
for name,path,ent,repo in ctrls:
    w(f"{C}/{name}.java", f"""
package com.dorm.controller;
import com.dorm.entity.{ent};
import com.dorm.repository.{repo};
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("{path}")
public class {name} extends CrudController<{ent}, {repo}> {{
    public {name}({repo} repo) {{ super(repo, {ent}.class); }}
}}
""")

w(f"{C}/SysUserController.java", r'''
package com.dorm.controller;
import com.dorm.common.*;
import com.dorm.entity.SysUser;
import com.dorm.repository.SysUserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import java.util.List;
/** 系统账号管理（仅管理员） */
@RestController
@RequestMapping("/api/users")
@PreAuthorize("hasRole('ADMIN')")
@RequiredArgsConstructor
public class SysUserController {
    private final SysUserRepository repo;
    private final PasswordEncoder encoder;
    @GetMapping
    public Result<List<SysUser>> list() { return Result.ok(repo.findAll()); }
    @PostMapping
    public Result<SysUser> create(@RequestBody SysUser u) {
        if (repo.existsByUsername(u.getUsername())) throw new BizException("用户名已存在");
        u.setPassword(encoder.encode(u.getPassword() == null ? "123456" : u.getPassword()));
        return Result.ok(repo.save(u));
    }
    @PutMapping("/{id}")
    public Result<SysUser> update(@PathVariable Long id, @RequestBody SysUser u) {
        SysUser old = repo.findById(id).orElseThrow(() -> new BizException("用户不存在"));
        u.setId(id);
        u.setPassword(u.getPassword() == null || u.getPassword().isBlank() ? old.getPassword() : encoder.encode(u.getPassword()));
        if (u.getCreateTime() == null) u.setCreateTime(old.getCreateTime());
        return Result.ok(repo.save(u));
    }
    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) { repo.deleteById(id); return Result.ok(); }
    @PostMapping("/{id}/reset-password")
    public Result<Void> reset(@PathVariable Long id) {
        SysUser u = repo.findById(id).orElseThrow(() -> new BizException("用户不存在"));
        u.setPassword(encoder.encode("123456"));
        repo.save(u);
        return Result.ok();
    }
}
''')
print("PART3 DONE")
