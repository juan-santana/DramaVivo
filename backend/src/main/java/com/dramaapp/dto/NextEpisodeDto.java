package com.dramaapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NextEpisodeDto {
    private String episodeId;
    private Integer seasonNumber;
    private Integer episodeNumber;
    private String title;
}
