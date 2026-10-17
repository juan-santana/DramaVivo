package com.dramaapp.dto;

import com.dramaapp.model.SubtitleTrack;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PlaybackResponseDto {
    private String episodeId;
    private String seriesId;
    private String seriesTitle;
    private String episodeTitle;
    private Integer seasonNumber;
    private Integer episodeNumber;
    private String playbackUrl;
    private String thumbnailUrl;
    private Integer durationSeconds;
    private List<SubtitleTrack> subtitleTracks;
    private NextEpisodeDto nextEpisode;
}
