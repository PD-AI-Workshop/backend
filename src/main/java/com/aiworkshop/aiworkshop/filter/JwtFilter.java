package com.aiworkshop.aiworkshop.filter;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.web.filter.OncePerRequestFilter;

import com.aiworkshop.aiworkshop.service.AuthService;
import com.aiworkshop.aiworkshop.utils.JwtUtils;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.var;

@RequiredArgsConstructor
public class JwtFilter extends OncePerRequestFilter {

    private final JwtUtils utils;
    @Autowired
    private AuthService authService;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        final var authorizationHeader = request.getHeader("Authorization");
        final var prefix = "Bearer ";
        final var prefixLength = prefix.length();
        final var isBearer = authorizationHeader != null && authorizationHeader.startsWith(prefix);

        if (!isBearer) {
            filterChain.doFilter(request, response);
            return;
        }

        final var jwt = authorizationHeader.substring(prefixLength);
        final var isValidate = utils.validate(jwt);

        if (isValidate) {

            final var username = utils.getUsername(jwt);
            final var user = authService.loadUserByUsername(username);

            final var authentication = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
            final var details = new WebAuthenticationDetailsSource().buildDetails(request);

            authentication.setDetails(details);

            SecurityContextHolder.getContext().setAuthentication(authentication);
        }

        filterChain.doFilter(request, response);
    }
    
}
