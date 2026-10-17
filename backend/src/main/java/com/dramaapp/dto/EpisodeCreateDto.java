package com.dramaapp.dto;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.SubtitleTrack;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EpisodeCreateDto {

    @NotBlank(message = "Series ID is required")
    private String seriesId;

    @Builder.Default
    @Min(value = 1, message = "Season number must be at least 1")
    private Integer seasonNumber = 1;

    @NotNull(message = "Episode number is required")
    @Min(value = 1, message = "Episode number must be at least 1")
    private Integer episodeNumber;

    @NotBlank(message = "Episode title is required")
    private String title;

    private String synopsis;

    private Integer durationSeconds;

    private String videoAssetId;

    private List<SubtitleTrack> subtitleTracks;

    private String thumbnail;

    @Builder.Default
    private PublicationStatus publicationStatus = PublicationStatus.DRAFT;

    @Builder.Default
    private RightsStatus rightsStatus = RightsStatus.DISCOVERED;
}
