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
