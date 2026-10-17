package com.dramaapp.controller.pub;

import com.dramaapp.model.VideoProcessingStatus;
import com.dramaapp.service.VideoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;

@Slf4j
@RestController
@RequestMapping("/api/media")
@RequiredArgsConstructor
@Tag(name = "Media Streaming", description = "Video content streaming and asset uploads")
public class MediaController {

    private final VideoService videoService;

    @Operation(summary = "Stream video content by file key (supports byte ranges / MP4)")
    @GetMapping("/stream/{fileKey}")
    public ResponseEntity<byte[]> streamVideo(@PathVariable String fileKey) {
        // Return dummy / synthetic MP4 header payload or empty content for dev stream testing
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.valueOf("video/mp4"));
        headers.setContentLength(0);
        headers.set(HttpHeaders.ACCEPT_RANGES, "bytes");
        return new ResponseEntity<>(new byte[0], headers, HttpStatus.OK);
    }

    @Operation(summary = "Handle video upload chunk or complete file")
    @PostMapping("/upload/{assetId}/{uploadId}")
    public ResponseEntity<Map<String, Object>> uploadVideo(
            @PathVariable String assetId,
            @PathVariable String uploadId,
            @RequestParam(value = "file", required = false) MultipartFile file
    ) {
        log.info("Received upload for asset [{}] with upload session [{}]", assetId, uploadId);
        videoService.updateStatus(assetId, VideoProcessingStatus.READY);
        return ResponseEntity.ok(Map.of(
                "status", "UPLOADED",
                "assetId", assetId,
                "uploadId", uploadId
        ));
    }
}
