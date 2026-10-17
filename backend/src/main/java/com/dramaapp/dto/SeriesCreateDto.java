package com.dramaapp.dto;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SeriesCreateDto {

    @NotBlank(message = "Title is required")
    private String title;

    private String originalTitle;

    private String synopsis;

    private List<String> genres;

    private String language;

    private String poster;

    private String sourceId;

    private String sourceUrl;

    @Builder.Default
    private PublicationStatus publicationStatus = PublicationStatus.DRAFT;

    @Builder.Default
    private RightsStatus rightsStatus = RightsStatus.DISCOVERED;

    private String seoTitle;

    private String seoDescription;
}
