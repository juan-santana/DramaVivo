package com.dramaapp.controller.admin;

import com.dramaapp.dto.DashboardStatsDto;
import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SeriesStatsDto;
import com.dramaapp.model.AuditLog;
import com.dramaapp.service.AnalyticsService;
import com.dramaapp.service.AuditService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/admin/analytics")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Analytics", description = "Platform KPIs, viewing metrics, and security audit logs")
public class AdminAnalyticsController {

    private final AnalyticsService analyticsService;
    private final AuditService auditService;

    @Operation(summary = "Get high-level dashboard metrics (counts, views, active crawler jobs)")
    @GetMapping("/dashboard")
    public ResponseEntity<DashboardStatsDto> getDashboardStats() {
        return ResponseEntity.ok(analyticsService.getDashboardStats());
    }

    @Operation(summary = "Get detailed analytics and engagement stats for a single series")
    @GetMapping("/series/{seriesId}")
    public ResponseEntity<SeriesStatsDto> getSeriesStats(@PathVariable String seriesId) {
        return ResponseEntity.ok(analyticsService.getSeriesStats(seriesId));
    }

    @Operation(summary = "Get paginated security and administrative audit logs")
    @GetMapping("/audit-logs")
    public ResponseEntity<PagedResponseDto<AuditLog>> getAuditLogs(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        Pageable pageable = PageRequest.of(page, size);
        return ResponseEntity.ok(PagedResponseDto.from(auditService.getAuditLogs(pageable)));
    }
}
