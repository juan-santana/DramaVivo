package com.dramaapp.controller.pub;

import com.dramaapp.dto.AnalyticsEventDto;
import com.dramaapp.service.AnalyticsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/analytics")
@RequiredArgsConstructor
@Tag(name = "Public Analytics", description = "Client telemetry and viewing analytics endpoints")
public class AnalyticsController {

    private final AnalyticsService analyticsService;

    @Operation(summary = "Record client playback or navigation telemetry event")
    @PostMapping("/events")
    public ResponseEntity<Map<String, String>> recordEvent(@Valid @RequestBody AnalyticsEventDto eventDto) {
        analyticsService.recordEvent(eventDto);
        return ResponseEntity.ok(Map.of("status", "recorded"));
    }
}
