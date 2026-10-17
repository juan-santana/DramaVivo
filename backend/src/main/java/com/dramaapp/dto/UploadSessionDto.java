package com.dramaapp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UploadSessionDto {
    private String uploadId;
    private String uploadUrl;
    private String assetId;
    private String provider;
    private Instant expiresAt;
}
