package com.dramaapp.dto;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.SubtitleTrack;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EpisodeDto {
    private String id;
    private String seriesId;
    private Integer seasonNumber;
    private Integer episodeNumber;
    private String title;
    private String synopsis;
    private Integer durationSeconds;
    private String videoAssetId;
    private List<SubtitleTrack> subtitleTracks;
    private String thumbnail;
    private PublicationStatus publicationStatus;
    private RightsStatus rightsStatus;
    private Instant createdAt;
    private Instant updatedAt;
}
