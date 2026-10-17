package com.dramaapp.controller.admin;

import com.dramaapp.dto.EpisodeCreateDto;
import com.dramaapp.dto.EpisodeDto;
import com.dramaapp.dto.EpisodeUpdateDto;
import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.service.EpisodeService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;

@RestController
@RequestMapping("/api/admin/episodes")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Episodes", description = "Administration of episodes, video links, and subtitle tracks")
public class AdminEpisodeController {

    private final EpisodeService episodeService;

    @Operation(summary = "List all episodes for a series with pagination")
    @GetMapping("/series/{seriesId}")
    public ResponseEntity<PagedResponseDto<EpisodeDto>> getBySeries(
            @PathVariable String seriesId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "100") int size
    ) {
        return ResponseEntity.ok(episodeService.getEpisodesForSeries(seriesId, page, size));
    }

    @Operation(summary = "Get episode details by ID")
    @GetMapping("/{id}")
    public ResponseEntity<EpisodeDto> getById(@PathVariable String id) {
        return ResponseEntity.ok(episodeService.getById(id));
    }

    @Operation(summary = "Create an episode in a series")
    @PostMapping
    public ResponseEntity<EpisodeDto> create(
            @Valid @RequestBody EpisodeCreateDto createDto,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.status(HttpStatus.CREATED).body(episodeService.create(createDto, username));
    }

    @Operation(summary = "Update episode details, video asset or subtitle tracks")
    @PutMapping("/{id}")
    public ResponseEntity<EpisodeDto> update(
            @PathVariable String id,
            @Valid @RequestBody EpisodeUpdateDto updateDto,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.ok(episodeService.update(id, updateDto, username));
    }

    @Operation(summary = "Delete an episode")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id, Principal principal) {
        String username = principal != null ? principal.getName() : "ADMIN";
        episodeService.delete(id, username);
        return ResponseEntity.noContent().build();
    }
}
