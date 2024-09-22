package com.aiworkshop.aiworkshop.utils;

import java.util.Date;

import javax.crypto.SecretKey;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "jwt")
public class JwtUtils {

    private String secret;
    private int expirationMs;

    public String generate(Authentication authentication) {
        final var userDetails = (UserDetails) authentication.getPrincipal();
        final var fastTime = new Date().getTime() + expirationMs;
        final var date = new Date(fastTime);

        return Jwts
                .builder()
                .subject(userDetails.getUsername())
                .issuedAt(new Date())
                .expiration(date)
                .signWith(key())
                .compact();
    }

    public String getUsername(String token) {
        return Jwts
                .parser()
                .verifyWith(key())
                .build()
                .parseSignedClaims(token)
                .getPayload()
                .getSubject();
    }

    public boolean validate(String token) {
        try {
            Jwts
                    .parser()
                    .verifyWith(key())
                    .build()
                    .parse(token);

            return true;
        } 
        
        catch (Exception e) {
            return false;
        }
    }

    private SecretKey key() {
        return Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    }

}
