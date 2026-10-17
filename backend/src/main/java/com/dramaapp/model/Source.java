package com.dramaapp.model;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.URL;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "sources")
public class Source {

    @Id
    private String id;

    @NotBlank(message = "Source name is required")
    private String name;

    @NotBlank(message = "Base URL is required")
    @URL(message = "Base URL must be a valid URL")
    private String baseUrl;

    private String adapterType;

    private boolean enabled;

    private Map<String, Object> crawlPolicy;

    private Instant lastSuccessfulRun;

    private String lastError;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
