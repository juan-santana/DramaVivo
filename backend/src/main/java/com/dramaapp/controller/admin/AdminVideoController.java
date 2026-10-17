package com.dramaapp.controller.admin;

import com.dramaapp.dto.CreateUploadSessionRequestDto;
import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.UploadSessionDto;
import com.dramaapp.dto.VideoAssetDto;
import com.dramaapp.model.VideoProcessingStatus;
import com.dramaapp.service.VideoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/admin/videos")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Video Assets", description = "Video asset management and upload session generation")
public class AdminVideoController {

    private final VideoService videoService;

    @Operation(summary = "List registered video assets with optional status filter")
    @GetMapping
    public ResponseEntity<PagedResponseDto<VideoAssetDto>> listAssets(
            @RequestParam(required = false) VideoProcessingStatus status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        Pageable pageable = PageRequest.of(page, size);
        return ResponseEntity.ok(PagedResponseDto.from(videoService.listAssets(status, pageable)));
    }

    @Operation(summary = "Get video asset details by ID")
    @GetMapping("/{id}")
    public ResponseEntity<VideoAssetDto> getById(@PathVariable String id) {
        return ResponseEntity.ok(videoService.toDto(videoService.getAsset(id)));
    }

    @Operation(summary = "Generate a direct upload session URL for video file ingest")
    @PostMapping("/upload-session")
    public ResponseEntity<UploadSessionDto> createUploadSession(
            @Valid @RequestBody CreateUploadSessionRequestDto request
    ) {
        return ResponseEntity.status(HttpStatus.CREATED).body(videoService.createUploadSession(request));
    }

    @Operation(summary = "Update video processing status (e.g. READY, FAILED)")
    @PatchMapping("/{id}/status")
    public ResponseEntity<VideoAssetDto> updateStatus(
            @PathVariable String id,
            @RequestBody Map<String, String> body
    ) {
        VideoProcessingStatus status = VideoProcessingStatus.valueOf(body.get("status").toUpperCase());
        return ResponseEntity.ok(videoService.toDto(videoService.updateStatus(id, status)));
    }
}
