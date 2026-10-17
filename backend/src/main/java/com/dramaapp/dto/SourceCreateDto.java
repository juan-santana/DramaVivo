package com.dramaapp.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.URL;

import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SourceCreateDto {

    @NotBlank(message = "Source name is required")
    private String name;

    @NotBlank(message = "Base URL is required")
    @URL(message = "Base URL must be valid")
    private String baseUrl;

    private String adapterType;

    @Builder.Default
    private boolean enabled = true;

    private Map<String, Object> crawlPolicy;
}
