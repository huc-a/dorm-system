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
