package com.dramaapp.repository;

import com.dramaapp.model.AnalyticsEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;

@Repository
public interface AnalyticsEventRepository extends MongoRepository<AnalyticsEvent, String> {

    long countByTimestampAfter(Instant timestamp);

    long countByEventTypeAndTimestampAfter(String eventType, Instant timestamp);

    long countBySeriesId(String seriesId);

    long countBySeriesIdAndEventType(String seriesId, String eventType);

    long countBySeriesIdAndTimestampAfter(String seriesId, Instant timestamp);

    long countByEpisodeIdAndEventType(String episodeId, String eventType);
}
