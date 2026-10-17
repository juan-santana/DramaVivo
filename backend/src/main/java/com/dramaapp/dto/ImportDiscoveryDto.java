package com.dramaapp.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.URL;

import java.util.List;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ImportDiscoveryDto {

    @NotBlank(message = "Source ID is required")
    private String sourceId;

    @NotBlank(message = "Source URL is required")
    @URL(message = "Source URL must be valid")
    private String sourceUrl;

    @NotBlank(message = "Title is required")
    private String title;

    private String originalTitle;

    private String synopsis;

    private List<String> genres;

    private String language;

    private String poster;

    private Integer externalEpisodesCount;

    private Map<String, Object> metadata;
}
