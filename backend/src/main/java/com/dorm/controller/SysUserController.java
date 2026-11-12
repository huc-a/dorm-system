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
