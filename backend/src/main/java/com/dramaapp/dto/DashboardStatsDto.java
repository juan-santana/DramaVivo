package com.dramaapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DashboardStatsDto {
    private long totalSeries;
    private long publishedSeries;
    private long pendingRightsReviews;
    private long totalEpisodes;
    private long totalVideoAssets;
    private long totalViews;
    private long eventsLast24h;
    private List<ImportJobDto> recentImportJobs;
}
