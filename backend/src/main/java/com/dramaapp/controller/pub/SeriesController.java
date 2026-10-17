package com.dramaapp.controller.pub;

import com.dramaapp.dto.EpisodeDto;
import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SeriesDto;
import com.dramaapp.service.EpisodeService;
import com.dramaapp.service.SeriesService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
@Tag(name = "Public Series", description = "Public catalog browsing and search APIs")
public class SeriesController {

    private final SeriesService seriesService;
    private final EpisodeService episodeService;

    @Operation(summary = "List published series with pagination and optional filtering")
    @GetMapping("/series")
    public ResponseEntity<PagedResponseDto<SeriesDto>> listPublished(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String genre,
            @RequestParam(required = false) String language,
            @RequestParam(defaultValue = "createdAt") String sortBy,
            @RequestParam(defaultValue = "desc") String sortDir
    ) {
        return ResponseEntity.ok(seriesService.listPublished(page, size, genre, language, sortBy, sortDir));
    }

    @Operation(summary = "Get series details by SEO slug")
    @GetMapping("/series/{slug}")
    public ResponseEntity<SeriesDto> getBySlug(@PathVariable String slug) {
        return ResponseEntity.ok(seriesService.getBySlug(slug));
    }

    @Operation(summary = "Get episodes list for a series by slug")
    @GetMapping("/series/{slug}/episodes")
    public ResponseEntity<PagedResponseDto<EpisodeDto>> getEpisodes(
            @PathVariable String slug,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "100") int size
    ) {
        return ResponseEntity.ok(episodeService.getEpisodesForSeriesSlug(slug, page, size));
    }

    @Operation(summary = "List all available genres for published dramas")
    @GetMapping("/genres")
    public ResponseEntity<List<String>> getGenres() {
        return ResponseEntity.ok(seriesService.getGenres());
    }

    @Operation(summary = "Full-text and faceted search across published dramas")
    @GetMapping("/search")
    public ResponseEntity<PagedResponseDto<SeriesDto>> search(
            @RequestParam(required = false, name = "q") String query,
            @RequestParam(required = false) String genre,
            @RequestParam(required = false) String language,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(defaultValue = "viewCount") String sortBy,
            @RequestParam(defaultValue = "desc") String sortDir
    ) {
        return ResponseEntity.ok(seriesService.search(query, genre, language, page, size, sortBy, sortDir));
    }
}
