package com.licenta.userAuthentification.exception;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.context.request.WebRequest;

public interface GlobalExceptionsHandler {
    ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex,
                                                        HttpHeaders headers,
                                                        HttpStatus status,
                                                        WebRequest request);
}
