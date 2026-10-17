package com.dramaapp.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "episodes")
@CompoundIndex(name = "series_season_episode_unique", def = "{'seriesId': 1, 'seasonNumber': 1, 'episodeNumber': 1}", unique = true)
public class Episode {

    @Id
    private String id;

    @Indexed
    private String seriesId;

    private Integer seasonNumber;

    private Integer episodeNumber;

    private String title;

    private String synopsis;

    private Integer durationSeconds;

    @Indexed
    private String videoAssetId;

    @Builder.Default
    private List<SubtitleTrack> subtitleTracks = new ArrayList<>();

    private String thumbnail;

    @Indexed
    private PublicationStatus publicationStatus;

    @Indexed
    private RightsStatus rightsStatus;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
