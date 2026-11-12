package com.dorm.controller;
import com.dorm.common.*;
import com.dorm.entity.*;
import com.dorm.repository.*;
import com.dorm.security.JwtUtil;
import jakarta.validation.constraints.NotBlank;
import lombok.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
/** 登录 / 注册 / 当前用户 / 修改密码 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {
    private final SysUserRepository users;
    private final StudentRepository students;
    private final PasswordEncoder encoder;
    private final JwtUtil jwt;

    @Data public static class LoginReq { @NotBlank private String username; @NotBlank private String password; }
    @Data public static class RegisterReq {
        @NotBlank private String studentNo; @NotBlank private String name;
        @NotBlank private String password; private String phone; private String gender;
        private String college; private String major; private String className; private String grade;
    }
    @Data public static class ChangePwdReq { private String oldPassword; private String newPassword; }

    @PostMapping("/login")
    public Result<Map<String, Object>> login(@RequestBody LoginReq req) {
        SysUser u = users.findByUsername(req.getUsername())
            .orElseThrow(() -> new BizException("用户名或密码错误"));
        if (u.getStatus() != null && u.getStatus() == 0) throw new BizException("账号已被禁用");
        if (!encoder.matches(req.getPassword(), u.getPassword())) throw new BizException("用户名或密码错误");
        String token = jwt.generate(u.getUsername(), u.getRole(), u.getId());
        return Result.ok(Map.of("token", token, "user", u));
    }
    /** 学生自助注册：创建登录账号与学生档案 */
    @PostMapping("/register")
    public Result<SysUser> register(@RequestBody RegisterReq req) {
        if (users.existsByUsername(req.getStudentNo())) throw new BizException("该学号已注册");
        if (students.findByStudentNo(req.getStudentNo()).isPresent()) throw new BizException("该学号档案已存在");
        SysUser u = new SysUser();
        u.setUsername(req.getStudentNo()); u.setPassword(encoder.encode(req.getPassword()));
        u.setRealName(req.getName()); u.setRole("STUDENT"); u.setPhone(req.getPhone());
        users.save(u);
        Student s = new Student();
        s.setStudentNo(req.getStudentNo()); s.setName(req.getName()); s.setGender(req.getGender());
        s.setCollege(req.getCollege()); s.setMajor(req.getMajor()); s.setClassName(req.getClassName());
        s.setGrade(req.getGrade()); s.setPhone(req.getPhone()); s.setUserId(u.getId());
        students.save(s);
        return Result.ok(u);
    }
    @GetMapping("/me")
    public Result<Map<String, Object>> me(Authentication auth) {
        SysUser u = users.findByUsername(auth.getName()).orElseThrow(() -> new BizException("用户不存在"));
        Student stu = students.findByUserId(u.getId()).orElse(null);
        return Result.ok(Map.of("user", u, "student", stu == null ? Map.of() : stu));
    }
    @PostMapping("/change-password")
    public Result<Void> changePwd(Authentication auth, @RequestBody ChangePwdReq req) {
        SysUser u = users.findByUsername(auth.getName()).orElseThrow(() -> new BizException("用户不存在"));
        if (!encoder.matches(req.getOldPassword(), u.getPassword())) throw new BizException("原密码不正确");
        u.setPassword(encoder.encode(req.getNewPassword()));
        users.save(u);
        return Result.ok();
    }
}
