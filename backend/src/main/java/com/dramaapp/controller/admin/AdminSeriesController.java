package com.dramaapp.controller.admin;

import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SeriesCreateDto;
import com.dramaapp.dto.SeriesDto;
import com.dramaapp.dto.SeriesUpdateDto;
import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.service.SeriesService;
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
@RequestMapping("/api/admin/series")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Series", description = "Administration of drama series metadata, draft status, and publishing")
public class AdminSeriesController {

    private final SeriesService seriesService;

    @Operation(summary = "List all series (drafts, published, archived) with optional filtering")
    @GetMapping
    public ResponseEntity<PagedResponseDto<SeriesDto>> listAdmin(
            @RequestParam(required = false) PublicationStatus publicationStatus,
            @RequestParam(required = false) RightsStatus rightsStatus,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        return ResponseEntity.ok(seriesService.listAdmin(publicationStatus, rightsStatus, page, size));
    }

    @Operation(summary = "Get full series details by ID")
    @GetMapping("/{id}")
    public ResponseEntity<SeriesDto> getById(@PathVariable String id) {
        return ResponseEntity.ok(seriesService.getById(id));
    }

    @Operation(summary = "Create a new series manually")
    @PostMapping
    public ResponseEntity<SeriesDto> create(
            @Valid @RequestBody SeriesCreateDto createDto,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.status(HttpStatus.CREATED).body(seriesService.create(createDto, username));
    }

    @Operation(summary = "Update series metadata or status")
    @PutMapping("/{id}")
    public ResponseEntity<SeriesDto> update(
            @PathVariable String id,
            @Valid @RequestBody SeriesUpdateDto updateDto,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.ok(seriesService.update(id, updateDto, username));
    }

    @Operation(summary = "Delete series and its associated episodes")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id, Principal principal) {
        String username = principal != null ? principal.getName() : "ADMIN";
        seriesService.delete(id, username);
        return ResponseEntity.noContent().build();
    }
}
