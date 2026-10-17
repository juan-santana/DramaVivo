package com.dramaapp.controller.pub;

import com.dramaapp.dto.EpisodeDto;
import com.dramaapp.dto.PlaybackResponseDto;
import com.dramaapp.service.EpisodeService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/episodes")
@RequiredArgsConstructor
@Tag(name = "Public Episodes", description = "Public episode metadata and video streaming playback APIs")
public class EpisodeController {

    private final EpisodeService episodeService;

    @Operation(summary = "Get episode metadata by ID")
    @GetMapping("/{id}")
    public ResponseEntity<EpisodeDto> getById(@PathVariable String id) {
        return ResponseEntity.ok(episodeService.getById(id));
    }

    @Operation(summary = "Get video playback URL and player metadata (verifies streaming rights)")
    @GetMapping("/{id}/playback")
    public ResponseEntity<PlaybackResponseDto> getPlayback(@PathVariable String id) {
        return ResponseEntity.ok(episodeService.getPlayback(id));
    }
}
