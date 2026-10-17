package com.dramaapp.dto;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
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
public class SeriesDto {
    private String id;
    private String slug;
    private String title;
    private String originalTitle;
    private String synopsis;
    private List<String> genres;
    private String language;
    private String poster;
    private String sourceId;
    private String sourceUrl;
    private PublicationStatus publicationStatus;
    private RightsStatus rightsStatus;
    private String seoTitle;
    private String seoDescription;
    private long viewCount;
    private long episodeCount;
    private Instant createdAt;
    private Instant updatedAt;
}
