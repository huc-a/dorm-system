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
