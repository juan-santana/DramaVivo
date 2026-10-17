package com.dramaapp.service;

import com.dramaapp.dto.CreateUploadSessionRequestDto;
import com.dramaapp.dto.UploadSessionDto;
import com.dramaapp.model.VideoAsset;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.UUID;

@Slf4j
@Component
public class LocalVideoProvider implements VideoProvider {

    public static final String PROVIDER_NAME = "LOCAL";

    @Value("${dramaapp.video.base-playback-url:http://localhost:8080/api/media}")
    private String basePlaybackUrl;

    @Override
    public String getProviderName() {
        return PROVIDER_NAME;
    }

    @Override
    public String generatePlaybackUrl(VideoAsset asset) {
        if (asset == null) {
            return null;
        }
        String fileKey = asset.getFileKey() != null ? asset.getFileKey() : asset.getProviderAssetId();
        return basePlaybackUrl + "/stream/" + fileKey + ".mp4";
    }

    @Override
    public UploadSessionDto createUploadSession(CreateUploadSessionRequestDto request, String assetId) {
        String uploadId = UUID.randomUUID().toString();
        String uploadUrl = basePlaybackUrl + "/upload/" + assetId + "/" + uploadId;

        return UploadSessionDto.builder()
                .uploadId(uploadId)
                .uploadUrl(uploadUrl)
                .assetId(assetId)
                .provider(PROVIDER_NAME)
                .expiresAt(Instant.now().plus(2, ChronoUnit.HOURS))
                .build();
    }
}
