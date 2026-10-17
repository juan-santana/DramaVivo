package com.dramaapp.service;

import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SourceCreateDto;
import com.dramaapp.dto.SourceDto;
import com.dramaapp.dto.SourceUpdateDto;
import com.dramaapp.exception.ResourceNotFoundException;
import com.dramaapp.model.ImportJob;
import com.dramaapp.model.Source;
import com.dramaapp.repository.SourceRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Lazy;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Slf4j
@Service
public class SourceService {

    private final SourceRepository sourceRepository;
    private final ImportService importService;
    private final AuditService auditService;

    public SourceService(
            SourceRepository sourceRepository,
            @Lazy ImportService importService,
            AuditService auditService) {
        this.sourceRepository = sourceRepository;
        this.importService = importService;
        this.auditService = auditService;
    }

    public PagedResponseDto<SourceDto> listSources(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<Source> sourcePage = sourceRepository.findAll(pageable);
        return PagedResponseDto.from(sourcePage.map(this::toDto));
    }

    public SourceDto getById(String id) {
        Source source = sourceRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Source", "id", id));
        return toDto(source);
    }

    public SourceDto create(SourceCreateDto dto, String adminUsername) {
        Source source = Source.builder()
                .name(dto.getName())
                .baseUrl(dto.getBaseUrl())
                .adapterType(dto.getAdapterType())
                .enabled(dto.isEnabled())
                .crawlPolicy(dto.getCrawlPolicy())
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .build();

        Source saved = sourceRepository.save(source);
        auditService.logAction(adminUsername, "CREATE", "SOURCE", saved.getId(), "Created source: " + saved.getName());
        return toDto(saved);
    }

    public SourceDto update(String id, SourceUpdateDto dto, String adminUsername) {
        Source source = sourceRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Source", "id", id));

        if (dto.getName() != null && !dto.getName().isBlank()) {
            source.setName(dto.getName());
        }
        if (dto.getBaseUrl() != null && !dto.getBaseUrl().isBlank()) {
            source.setBaseUrl(dto.getBaseUrl());
        }
        if (dto.getAdapterType() != null) {
            source.setAdapterType(dto.getAdapterType());
        }
        if (dto.getEnabled() != null) {
            source.setEnabled(dto.getEnabled());
        }
        if (dto.getCrawlPolicy() != null) {
            source.setCrawlPolicy(dto.getCrawlPolicy());
        }
        source.setUpdatedAt(Instant.now());

        Source saved = sourceRepository.save(source);
        auditService.logAction(adminUsername, "UPDATE", "SOURCE", saved.getId(), "Updated source: " + saved.getName());
        return toDto(saved);
    }

    public void delete(String id, String adminUsername) {
        Source source = sourceRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Source", "id", id));
        sourceRepository.delete(source);
        auditService.logAction(adminUsername, "DELETE", "SOURCE", id, "Deleted source: " + source.getName());
    }

    public ImportJob triggerImport(String sourceId, String adminUsername) {
        Source source = sourceRepository.findById(sourceId)
                .orElseThrow(() -> new ResourceNotFoundException("Source", "id", sourceId));

        if (!source.isEnabled()) {
            throw new IllegalStateException("Source '" + source.getName() + "' is disabled.");
        }

        ImportJob job = importService.createJob(sourceId);
        auditService.logAction(adminUsername, "TRIGGER_IMPORT", "SOURCE", sourceId, "Triggered import job: " + job.getId());
        return job;
    }

    public SourceDto toDto(Source source) {
        if (source == null) return null;
        return SourceDto.builder()
                .id(source.getId())
                .name(source.getName())
                .baseUrl(source.getBaseUrl())
                .adapterType(source.getAdapterType())
                .enabled(source.isEnabled())
                .crawlPolicy(source.getCrawlPolicy())
                .lastSuccessfulRun(source.getLastSuccessfulRun())
                .lastError(source.getLastError())
                .createdAt(source.getCreatedAt())
                .updatedAt(source.getUpdatedAt())
                .build();
    }
}
