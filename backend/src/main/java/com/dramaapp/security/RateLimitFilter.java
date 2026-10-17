package com.dramaapp.security;

import com.dramaapp.dto.ErrorResponseDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.lang.NonNull;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

@Slf4j
@Component
public class RateLimitFilter extends OncePerRequestFilter {

    private final int publicLimit;
    private final int adminLimit;
    private final ObjectMapper objectMapper;
    private final Map<String, RequestCounter> requestCounts = new ConcurrentHashMap<>();

    public RateLimitFilter(
            @Value("${dramaapp.rate-limit.public-requests-per-minute:100}") int publicLimit,
            @Value("${dramaapp.rate-limit.admin-requests-per-minute:200}") int adminLimit,
            ObjectMapper objectMapper) {
        this.publicLimit = publicLimit;
        this.adminLimit = adminLimit;
        this.objectMapper = objectMapper;
    }

    private static class RequestCounter {
        private volatile long windowStart;
        private final AtomicInteger count;

        public RequestCounter(long windowStart) {
            this.windowStart = windowStart;
            this.count = new AtomicInteger(1);
        }

        public synchronized int incrementAndGet(long now) {
            if (now - windowStart > 60000) {
                windowStart = now;
                count.set(1);
                return 1;
            }
            return count.incrementAndGet();
        }
    }

    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain
    ) throws ServletException, IOException {
        String path = request.getRequestURI();

        // Skip rate limiting for static / docs / actuator
        if (path.startsWith("/swagger-ui") || path.startsWith("/v3/api-docs") || path.startsWith("/actuator")) {
            filterChain.doFilter(request, response);
            return;
        }

        String clientIp = getClientIp(request);
        boolean isAdmin = path.startsWith("/api/admin");
        int maxAllowed = isAdmin ? adminLimit : publicLimit;

        long now = System.currentTimeMillis();
        RequestCounter counter = requestCounts.computeIfAbsent(clientIp + ":" + (isAdmin ? "admin" : "pub"),
                k -> new RequestCounter(now));

        int currentRequests = counter.incrementAndGet(now);

        if (currentRequests > maxAllowed) {
            log.warn("Rate limit exceeded for IP: {} on path: {} ({} > {})", clientIp, path, currentRequests, maxAllowed);
            response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            response.setContentType(MediaType.APPLICATION_JSON_VALUE);

            ErrorResponseDto error = ErrorResponseDto.builder()
                    .timestamp(Instant.now())
                    .status(HttpStatus.TOO_MANY_REQUESTS.value())
                    .error("Too Many Requests")
                    .message("Rate limit exceeded. Allowed: " + maxAllowed + " requests per minute.")
                    .path(path)
                    .build();

            response.getWriter().write(objectMapper.writeValueAsString(error));
            return;
        }

        filterChain.doFilter(request, response);
    }

    private String getClientIp(HttpServletRequest request) {
        String xfHeader = request.getHeader("X-Forwarded-For");
        if (xfHeader == null || xfHeader.isEmpty()) {
            return request.getRemoteAddr();
        }
        return xfHeader.split(",")[0].trim();
    }
}
