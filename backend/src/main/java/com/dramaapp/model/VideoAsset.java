package com.dramaapp.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "video_assets")
@CompoundIndex(name = "provider_asset_unique", def = "{'provider': 1, 'providerAssetId': 1}", unique = true)
public class VideoAsset {

    @Id
    private String id;

    private String provider;

    private String providerAssetId;

    @Transient
    private String playbackUrl;

    private String storagePath;

    private String fileKey;

    private String thumbnailUrl;

    @Indexed
    private VideoProcessingStatus processingStatus;

    private Integer durationSeconds;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
