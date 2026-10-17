package com.dramaapp.dto;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SeriesUpdateDto {
    private String title;
    private String originalTitle;
    private String synopsis;
    private List<String> genres;
    private String language;
    private String poster;
    private PublicationStatus publicationStatus;
    private RightsStatus rightsStatus;
    private String seoTitle;
    private String seoDescription;
}
