package com.dramaapp.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AnalyticsEventDto {

    @NotBlank(message = "Anonymous session ID is required")
    private String anonymousSessionId;

    @NotBlank(message = "Event type is required (e.g. PAGE_VIEW, PLAY_START, PLAY_PROGRESS, PLAY_COMPLETE)")
    private String eventType;

    private String seriesId;

    private String episodeId;

    private Map<String, Object> metadata;
}
