#!/usr/bin/env python3
# Generator for dorm-system backend (part 1: pom/config/common/security)
import os, textwrap
ROOT = os.path.expanduser("~/workspace/dorm-system/backend")
PKG = "src/main/java/com/dorm"
def w(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("wrote", rel)

w("pom.xml", r'''
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.5</version>
        <relativePath/>
    </parent>
    <groupId>com.dorm</groupId>
    <artifactId>dorm-system</artifactId>
    <version>1.0.0</version>
    <name>dorm-system</name>
    <description>基于Spring Boot+Vue的宿舍管理系统（毕业设计）</description>
    <properties>
        <java.version>21</java.version>
        <jjwt.version>0.12.6</jjwt.version>
        <springdoc.version>2.6.0</springdoc.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>${jjwt.version}</version>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>${jjwt.version}</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
            <version>${springdoc.version}</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
''')

w("src/main/resources/application.yml", r'''
server:
  port: 8081
spring:
  application:
    name: dorm-system
  datasource:
    url: jdbc:mysql://127.0.0.1:3306/dorm_db?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&createDatabaseIfNotExist=true
    username: ${DB_USERNAME:dorm}
    password: ${DB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.MySQLDialect
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: Asia/Shanghai
dorm:
  jwt:
    secret: ${JWT_SECRET:dorm-system-graduation-design-secret-key-2026-please-change-in-production}
    expire-hours: 24
logging:
  level:
    com.dorm: info
''')

w(f"{PKG}/DormApplication.java", r'''
package com.dorm;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication
public class DormApplication {
    public static void main(String[] args) {
        SpringApplication.run(DormApplication.class, args);
    }
}
''')

w(f"{PKG}/common/Result.java", r'''
package com.dorm.common;
import lombok.Data;
@Data
public class Result<T> {
    private int code;
    private String msg;
    private T data;
    public static <T> Result<T> ok(T data) { Result<T> r = new Result<>(); r.code = 200; r.msg = "操作成功"; r.data = data; return r; }
    public static <T> Result<T> ok() { return ok(null); }
    public static <T> Result<T> fail(int code, String msg) { Result<T> r = new Result<>(); r.code = code; r.msg = msg; return r; }
    public static <T> Result<T> fail(String msg) { return fail(400, msg); }
}
''')

w(f"{PKG}/common/PageResult.java", r'''
package com.dorm.common;
import lombok.Data;
import org.springframework.data.domain.Page;
import java.util.List;
@Data
public class PageResult<T> {
    private List<T> records;
    private long total;
    private int page;
    private int size;
    public static <T> PageResult<T> of(Page<T> p) {
        PageResult<T> r = new PageResult<>();
        r.records = p.getContent(); r.total = p.getTotalElements();
        r.page = p.getNumber() + 1; r.size = p.getSize();
        return r;
    }
}
''')

w(f"{PKG}/common/BizException.java", r'''
package com.dorm.common;
public class BizException extends RuntimeException {
    public BizException(String msg) { super(msg); }
}
''')

w(f"{PKG}/common/GlobalExceptionHandler.java", r'''
package com.dorm.common;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(BizException.class)
    @ResponseStatus(HttpStatus.OK)
    public Result<Void> biz(BizException e) { return Result.fail(e.getMessage()); }
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.OK)
    public Result<Void> valid(MethodArgumentNotValidException e) {
        String m = e.getBindingResult().getFieldErrors().isEmpty() ? "参数校验失败"
            : e.getBindingResult().getFieldErrors().get(0).getDefaultMessage();
        return Result.fail(m);
    }
    @ExceptionHandler(AccessDeniedException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public Result<Void> denied(AccessDeniedException e) { return Result.fail(403, "无权访问该资源"); }
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.OK)
    public Result<Void> other(Exception e) { return Result.fail(500, "服务器内部错误: " + e.getMessage()); }
}
''')

w(f"{PKG}/security/JwtUtil.java", r'''
package com.dorm.security;
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
@Component
public class JwtUtil {
    @Value("${dorm.jwt.secret}") private String secret;
    @Value("${dorm.jwt.expire-hours}") private long expireHours;
    private SecretKey key() { return Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8)); }
    public String generate(String username, String role, Long userId) {
        Date now = new Date();
        return Jwts.builder().subject(username)
            .claim("role", role).claim("userId", userId)
            .issuedAt(now).expiration(new Date(now.getTime() + expireHours * 3600_000L))
            .signWith(key()).compact();
    }
    public Claims parse(String token) {
        return Jwts.parser().verifyWith(key()).build().parseSignedClaims(token).getPayload();
    }
}
''')

w(f"{PKG}/security/JwtFilter.java", r'''
package com.dorm.security;
import io.jsonwebtoken.Claims;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import java.io.IOException;
import java.util.List;
@Component
@RequiredArgsConstructor
public class JwtFilter extends OncePerRequestFilter {
    private final JwtUtil jwtUtil;
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {
        String h = req.getHeader("Authorization");
        if (h != null && h.startsWith("Bearer ") && SecurityContextHolder.getContext().getAuthentication() == null) {
            try {
                Claims c = jwtUtil.parse(h.substring(7));
                var auth = new UsernamePasswordAuthenticationToken(
                    c.getSubject(), null,
                    List.of(new SimpleGrantedAuthority("ROLE_" + c.get("role", String.class))));
                auth.setDetails(c.get("userId", Long.class));
                SecurityContextHolder.getContext().setAuthentication(auth);
            } catch (Exception ignored) { /* 无效令牌按未登录处理 */ }
        }
        chain.doFilter(req, res);
    }
}
''')

w(f"{PKG}/config/SecurityConfig.java", r'''
package com.dorm.config;
import com.dorm.security.JwtFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.*;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.*;
import java.util.List;
@Configuration
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {
    private final JwtFilter jwtFilter;
    @Bean public PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }
    @Bean
    public SecurityFilterChain chain(HttpSecurity http) throws Exception {
        http.csrf(c -> c.disable())
            .cors(c -> c.configurationSource(corsSource()))
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(a -> a
                .requestMatchers("/api/auth/login", "/api/auth/register").permitAll()
                .requestMatchers("/", "/index.html", "/assets/**", "/favicon.ico", "/swagger-ui/**", "/v3/api-docs/**").permitAll()
                .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                .anyRequest().authenticated())
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
    @Bean
    public CorsConfigurationSource corsSource() {
        CorsConfiguration cfg = new CorsConfiguration();
        cfg.setAllowedOriginPatterns(List.of("*"));
        cfg.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        cfg.setAllowedHeaders(List.of("*"));
        cfg.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
        src.registerCorsConfiguration("/**", cfg);
        return src;
    }
}
''')
print("PART1 DONE")
