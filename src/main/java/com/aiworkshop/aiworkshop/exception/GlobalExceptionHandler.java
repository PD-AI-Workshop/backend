package com.aiworkshop.aiworkshop.exception;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import org.springframework.http.HttpStatus;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.servlet.NoHandlerFoundException;

import com.aiworkshop.aiworkshop.dto.ErrorResponse;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@ResponseBody
@ControllerAdvice
public class GlobalExceptionHandler implements AuthenticationEntryPoint {

    // 400: Bad Request
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ErrorResponse handleBadRequestException(HttpMessageNotReadableException exception, HttpServletRequest request, HttpServletResponse response) {
        return handleException(request, response, exception);
    }

    // 401: Unauthorized
    @Override
    public void commence(HttpServletRequest request, HttpServletResponse response, AuthenticationException authenticationException) throws IOException, ServletException {
        final var errorResponse = handleException(request, response, authenticationException);
        final var jsonResponse = new ObjectMapper().writeValueAsString(errorResponse);

        response.setStatus(HttpStatus.UNAUTHORIZED.value());
        response.setContentType("application/json");
        response.getWriter().write(jsonResponse);
    }

    // 404: Not found
    @ResponseStatus(HttpStatus.NOT_FOUND)
    @ExceptionHandler(NoHandlerFoundException.class)
    public ErrorResponse handleNotFoundException(NoHandlerFoundException exception, HttpServletRequest request, HttpServletResponse response) {
        return handleException(request, response, exception);
    }

    // 405: Method not allowed
    @ResponseStatus(HttpStatus.METHOD_NOT_ALLOWED)
    @ExceptionHandler(HttpRequestMethodNotSupportedException.class)
    public ErrorResponse handleMethodNotAllowedException(HttpRequestMethodNotSupportedException exception, HttpServletRequest request, HttpServletResponse response) {
        return handleException(request, response, exception);
    }

    // 500: Internal server error
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleInternalServerException(Exception exception, HttpServletRequest request, HttpServletResponse response) {
        return handleException(request, response, exception);
    }

    private ErrorResponse handleException(HttpServletRequest request, HttpServletResponse response, Exception exception) {
        final var currentTime = LocalDateTime.now();
        final var formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss.SSS");
        final var formattedTime = currentTime.format(formatter);

        final var url = request.getRequestURI();
        final var message = exception.getMessage();
        final var user = SecurityContextHolder.getContext().getAuthentication();

        final var isAuthenticated = user != null && user.isAuthenticated();

        if (!isAuthenticated) {
            return ErrorResponse
                    .builder()
                    .date(formattedTime)
                    .message(message)
                    .url(url)
                    .user(null)
                    .build();
        }

        final var username = user.getName();

        return ErrorResponse
                .builder()
                .date(formattedTime)
                .message(message)
                .url(url)
                .user(username)
                .build();
    }
}
