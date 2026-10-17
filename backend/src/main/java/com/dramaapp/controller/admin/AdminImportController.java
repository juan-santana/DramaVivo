package com.dramaapp.controller.admin;

import com.dramaapp.dto.ImportDiscoveryDto;
import com.dramaapp.dto.ImportJobDto;
import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SeriesDto;
import com.dramaapp.model.Series;
import com.dramaapp.service.ImportService;
import com.dramaapp.service.SeriesService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/admin/imports")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Imports", description = "Monitor crawler execution jobs and accept discovered drama metadata")
public class AdminImportController {

    private final ImportService importService;
    private final SeriesService seriesService;

    @Operation(summary = "List crawler execution jobs with status")
    @GetMapping
    public ResponseEntity<PagedResponseDto<ImportJobDto>> listJobs(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        return ResponseEntity.ok(importService.listJobs(page, size));
    }

    @Operation(summary = "Get specific import job details by ID")
    @GetMapping("/{id}")
    public ResponseEntity<ImportJobDto> getJob(@PathVariable String id) {
        return ResponseEntity.ok(importService.getJob(id));
    }

    @Operation(summary = "Webhook / endpoint for external scrapers to post newly discovered series")
    @PostMapping("/discover")
    public ResponseEntity<SeriesDto> receiveDiscovered(@Valid @RequestBody ImportDiscoveryDto discoveryDto) {
        Series series = importService.receiveDiscoveredSeries(discoveryDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(seriesService.toDto(series));
    }
}
