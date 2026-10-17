package com.dramaapp.service;

import com.dramaapp.dto.CreateUploadSessionRequestDto;
import com.dramaapp.dto.UploadSessionDto;
import com.dramaapp.model.VideoAsset;

public interface VideoProvider {
    String getProviderName();
    String generatePlaybackUrl(VideoAsset asset);
    UploadSessionDto createUploadSession(CreateUploadSessionRequestDto request, String assetId);
}
