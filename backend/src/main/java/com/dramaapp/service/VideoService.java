package com.dramaapp.service;

import com.dramaapp.dto.CreateUploadSessionRequestDto;
import com.dramaapp.dto.UploadSessionDto;
import com.dramaapp.dto.VideoAssetDto;
import com.dramaapp.exception.ResourceNotFoundException;
import com.dramaapp.model.VideoAsset;
import com.dramaapp.model.VideoProcessingStatus;
import com.dramaapp.repository.VideoAssetRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@Service
public class VideoService {

    private final VideoAssetRepository videoAssetRepository;
    private final Map<String, VideoProvider> providers;
    private final VideoProvider defaultProvider;

    public VideoService(VideoAssetRepository videoAssetRepository, List<VideoProvider> providerList) {
        this.videoAssetRepository = videoAssetRepository;
        this.providers = providerList.stream()
                .collect(Collectors.toMap(p -> p.getProviderName().toUpperCase(), p -> p));
        this.defaultProvider = providers.getOrDefault(LocalVideoProvider.PROVIDER_NAME,
                providerList.isEmpty() ? null : providerList.get(0));
    }

    public VideoAsset registerAsset(String provider, String providerAssetId, Integer durationSeconds, String thumbnailUrl) {
        String effectiveProvider = provider != null ? provider.toUpperCase() : LocalVideoProvider.PROVIDER_NAME;
        return videoAssetRepository.findByProviderAndProviderAssetId(effectiveProvider, providerAssetId)
                .orElseGet(() -> {
                    VideoAsset asset = VideoAsset.builder()
                            .provider(effectiveProvider)
                            .providerAssetId(providerAssetId)
                            .processingStatus(VideoProcessingStatus.READY)
                            .durationSeconds(durationSeconds)
                            .thumbnailUrl(thumbnailUrl)
                            .createdAt(Instant.now())
                            .updatedAt(Instant.now())
                            .build();
                    return videoAssetRepository.save(asset);
                });
    }

    public VideoAsset getAsset(String id) {
        return videoAssetRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("VideoAsset", "id", id));
    }

    public VideoAsset updateStatus(String id, VideoProcessingStatus status) {
        VideoAsset asset = getAsset(id);
        asset.setProcessingStatus(status);
        asset.setUpdatedAt(Instant.now());
        return videoAssetRepository.save(asset);
    }

    public UploadSessionDto createUploadSession(CreateUploadSessionRequestDto request) {
        String assetId = UUID.randomUUID().toString();
        String providerAssetId = "asset-" + UUID.randomUUID().toString().substring(0, 8);

        VideoAsset asset = VideoAsset.builder()
                .id(assetId)
                .provider(LocalVideoProvider.PROVIDER_NAME)
                .providerAssetId(providerAssetId)
                .fileKey(providerAssetId)
                .processingStatus(VideoProcessingStatus.PENDING)
                .durationSeconds(request.getDurationSeconds())
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .build();
        videoAssetRepository.save(asset);

        VideoProvider provider = defaultProvider;
        return provider.createUploadSession(request, assetId);
    }

    public String generatePlaybackUrl(String assetId) {
        VideoAsset asset = getAsset(assetId);
        VideoProvider provider = providers.getOrDefault(asset.getProvider().toUpperCase(), defaultProvider);
        if (provider == null) {
            throw new IllegalStateException("No video provider configured for: " + asset.getProvider());
        }
        return provider.generatePlaybackUrl(asset);
    }

    public Page<VideoAssetDto> listAssets(VideoProcessingStatus status, Pageable pageable) {
        Page<VideoAsset> page = status != null
                ? videoAssetRepository.findByProcessingStatus(status, pageable)
                : videoAssetRepository.findAll(pageable);
        return page.map(this::toDto);
    }

    public VideoAssetDto toDto(VideoAsset asset) {
        if (asset == null) return null;
        String playbackUrl = null;
        try {
            VideoProvider provider = providers.getOrDefault(
                    asset.getProvider() != null ? asset.getProvider().toUpperCase() : LocalVideoProvider.PROVIDER_NAME,
                    defaultProvider);
            if (provider != null) {
                playbackUrl = provider.generatePlaybackUrl(asset);
            }
        } catch (Exception ex) {
            log.warn("Could not generate playback url for asset {}: {}", asset.getId(), ex.getMessage());
        }

        return VideoAssetDto.builder()
                .id(asset.getId())
                .provider(asset.getProvider())
                .providerAssetId(asset.getProviderAssetId())
                .playbackUrl(playbackUrl)
                .storagePath(asset.getStoragePath())
                .fileKey(asset.getFileKey())
                .thumbnailUrl(asset.getThumbnailUrl())
                .processingStatus(asset.getProcessingStatus())
                .durationSeconds(asset.getDurationSeconds())
                .createdAt(asset.getCreatedAt())
                .updatedAt(asset.getUpdatedAt())
                .build();
    }
}
