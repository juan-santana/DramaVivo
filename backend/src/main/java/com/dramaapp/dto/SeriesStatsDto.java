package com.dramaapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SeriesStatsDto {
    private String seriesId;
    private String title;
    private long viewCount;
    private long totalEvents;
    private long playEvents;
    private long completionEvents;
}
