package com.dramaapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SourceDto {
    private String id;
    private String name;
    private String baseUrl;
    private String adapterType;
    private boolean enabled;
    private Map<String, Object> crawlPolicy;
    private Instant lastSuccessfulRun;
    private String lastError;
    private Instant createdAt;
    private Instant updatedAt;
}
