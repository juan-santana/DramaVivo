package com.dramaapp.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.CompoundIndexes;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "analytics_events")
@CompoundIndexes({
    @CompoundIndex(name = "series_event_idx", def = "{'seriesId': 1, 'eventType': 1}"),
    @CompoundIndex(name = "type_time_idx", def = "{'eventType': 1, 'timestamp': -1}")
})
public class AnalyticsEvent {

    @Id
    private String id;

    @Indexed
    private String anonymousSessionId;

    @Indexed
    private String eventType;

    @Indexed
    private String seriesId;

    @Indexed
    private String episodeId;

    @Indexed
    private Instant timestamp;

    private Map<String, Object> metadata;
}
