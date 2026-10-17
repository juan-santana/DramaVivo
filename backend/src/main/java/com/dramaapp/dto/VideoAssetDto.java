package com.dramaapp.dto;

import com.dramaapp.model.VideoProcessingStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class VideoAssetDto {
    private String id;
    private String provider;
    private String providerAssetId;
    private String playbackUrl;
    private String storagePath;
    private String fileKey;
    private String thumbnailUrl;
    private VideoProcessingStatus processingStatus;
    private Integer durationSeconds;
    private Instant createdAt;
    private Instant updatedAt;
}
