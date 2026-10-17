package com.dramaapp.service;

import com.dramaapp.model.AuditLog;
import com.dramaapp.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    public void logAction(String adminUsername, String action, String targetType, String targetId, String details) {
        try {
            AuditLog auditLog = AuditLog.builder()
                    .adminUsername(adminUsername != null ? adminUsername : "SYSTEM")
                    .action(action)
                    .targetType(targetType)
                    .targetId(targetId)
                    .details(details)
                    .timestamp(Instant.now())
                    .build();
            auditLogRepository.save(auditLog);
            log.info("AUDIT: User [{}] performed [{}] on {} [{}] - {}", adminUsername, action, targetType, targetId, details);
        } catch (Exception ex) {
            log.error("Failed to persist audit log: {}", ex.getMessage());
        }
    }

    public Page<AuditLog> getAuditLogs(Pageable pageable) {
        return auditLogRepository.findAllByOrderByTimestampDesc(pageable);
    }
}
