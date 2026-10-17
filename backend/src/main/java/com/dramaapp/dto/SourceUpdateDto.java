package com.dramaapp.dto;

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
public class SourceUpdateDto {
    private String name;

    @URL(message = "Base URL must be valid")
    private String baseUrl;

    private String adapterType;

    private Boolean enabled;

    private Map<String, Object> crawlPolicy;
}
