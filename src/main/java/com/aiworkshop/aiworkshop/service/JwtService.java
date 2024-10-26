package com.aiworkshop.aiworkshop.service;

import java.io.IOException;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Service;
import org.springframework.web.filter.OncePerRequestFilter;

import com.aiworkshop.aiworkshop.utils.JwtUtils;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class JwtService extends OncePerRequestFilter {

    private final JwtUtils utils;
    private final UserDetailsServiceImpl userDetailsServiceImpl;

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
            final var user = userDetailsServiceImpl.loadUserByUsername(username);
            final var authentication = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
            final var details = new WebAuthenticationDetailsSource().buildDetails(request);

            authentication.setDetails(details);

            SecurityContextHolder.getContext().setAuthentication(authentication);
        }

        filterChain.doFilter(request, response);
    }
    
}
