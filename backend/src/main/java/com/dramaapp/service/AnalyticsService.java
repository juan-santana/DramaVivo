package com.dramaapp.service;

import com.dramaapp.dto.AnalyticsEventDto;
import com.dramaapp.dto.DashboardStatsDto;
import com.dramaapp.dto.ImportJobDto;
import com.dramaapp.dto.SeriesStatsDto;
import com.dramaapp.exception.ResourceNotFoundException;
import com.dramaapp.model.AnalyticsEvent;
import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsRecordStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import com.dramaapp.repository.AnalyticsEventRepository;
import com.dramaapp.repository.EpisodeRepository;
import com.dramaapp.repository.ImportJobRepository;
import com.dramaapp.repository.RightsRecordRepository;
import com.dramaapp.repository.SeriesRepository;
import com.dramaapp.repository.VideoAssetRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class AnalyticsService {

    private final AnalyticsEventRepository analyticsEventRepository;
    private final SeriesRepository seriesRepository;
    private final EpisodeRepository episodeRepository;
    private final VideoAssetRepository videoAssetRepository;
    private final RightsRecordRepository rightsRecordRepository;
    private final ImportJobRepository importJobRepository;
    private final ImportService importService;

    public void recordEvent(AnalyticsEventDto dto) {
        AnalyticsEvent event = AnalyticsEvent.builder()
                .anonymousSessionId(dto.getAnonymousSessionId())
                .eventType(dto.getEventType().toUpperCase())
                .seriesId(dto.getSeriesId())
                .episodeId(dto.getEpisodeId())
                .metadata(dto.getMetadata())
                .timestamp(Instant.now())
                .build();
        analyticsEventRepository.save(event);
    }

    public DashboardStatsDto getDashboardStats() {
        long totalSeries = seriesRepository.count();
        long publishedSeries = seriesRepository.countByPublicationStatusAndRightsStatus(
                PublicationStatus.PUBLISHED, RightsStatus.APPROVED);
        long pendingRights = rightsRecordRepository.countByStatus(RightsRecordStatus.PENDING);
        long totalEpisodes = episodeRepository.count();
        long totalAssets = videoAssetRepository.count();

        Instant last24h = Instant.now().minus(24, ChronoUnit.HOURS);
        long eventsLast24h = analyticsEventRepository.countByTimestampAfter(last24h);

        // Sum viewCount
        long totalViews = seriesRepository.findAll().stream()
                .mapToLong(Series::getViewCount)
                .sum();

        List<ImportJobDto> recentJobs = importJobRepository.findAllByOrderByStartedAtDesc(
                PageRequest.of(0, 5, Sort.by(Sort.Direction.DESC, "startedAt"))
        ).getContent().stream().map(importService::toDto).toList();

        return DashboardStatsDto.builder()
                .totalSeries(totalSeries)
                .publishedSeries(publishedSeries)
                .pendingRightsReviews(pendingRights)
                .totalEpisodes(totalEpisodes)
                .totalVideoAssets(totalAssets)
                .totalViews(totalViews)
                .eventsLast24h(eventsLast24h)
                .recentImportJobs(recentJobs)
                .build();
    }

    public SeriesStatsDto getSeriesStats(String seriesId) {
        Series series = seriesRepository.findById(seriesId)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", seriesId));

        long totalEvents = analyticsEventRepository.countBySeriesId(seriesId);
        long playEvents = analyticsEventRepository.countBySeriesIdAndEventType(seriesId, "PLAY_START");
        long completeEvents = analyticsEventRepository.countBySeriesIdAndEventType(seriesId, "PLAY_COMPLETE");

        return SeriesStatsDto.builder()
                .seriesId(series.getId())
                .title(series.getTitle())
                .viewCount(series.getViewCount())
                .totalEvents(totalEvents)
                .playEvents(playEvents)
                .completionEvents(completeEvents)
                .build();
    }
}
