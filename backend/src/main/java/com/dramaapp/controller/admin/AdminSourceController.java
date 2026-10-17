package com.dramaapp.controller.admin;

import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SourceCreateDto;
import com.dramaapp.dto.SourceDto;
import com.dramaapp.dto.SourceUpdateDto;
import com.dramaapp.model.ImportJob;
import com.dramaapp.service.SourceService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
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
@RequestMapping("/api/admin/sources")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Sources", description = "Manage scraper content sources and trigger crawl operations")
public class AdminSourceController {

    private final SourceService sourceService;

    @Operation(summary = "List all registered drama sources with pagination")
    @GetMapping
    public ResponseEntity<PagedResponseDto<SourceDto>> listSources(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        return ResponseEntity.ok(sourceService.listSources(page, size));
    }

    @Operation(summary = "Get source details by ID")
    @GetMapping("/{id}")
    public ResponseEntity<SourceDto> getById(@PathVariable String id) {
        return ResponseEntity.ok(sourceService.getById(id));
    }

    @Operation(summary = "Create a new crawler source")
    @PostMapping
    public ResponseEntity<SourceDto> create(
            @Valid @RequestBody SourceCreateDto createDto,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.status(HttpStatus.CREATED).body(sourceService.create(createDto, username));
    }

    @Operation(summary = "Update an existing crawler source")
    @PutMapping("/{id}")
    public ResponseEntity<SourceDto> update(
            @PathVariable String id,
            @Valid @RequestBody SourceUpdateDto updateDto,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.ok(sourceService.update(id, updateDto, username));
    }

    @Operation(summary = "Delete a crawler source")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable String id, Principal principal) {
        String username = principal != null ? principal.getName() : "ADMIN";
        sourceService.delete(id, username);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Trigger import / crawl job for a specific source")
    @PostMapping("/{id}/trigger-import")
    public ResponseEntity<ImportJob> triggerImport(@PathVariable String id, Principal principal) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.ok(sourceService.triggerImport(id, username));
    }
}
