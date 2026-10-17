package com.dramaapp.service;

import com.dramaapp.dto.ImportDiscoveryDto;
import com.dramaapp.dto.ImportJobDto;
import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.exception.ResourceNotFoundException;
import com.dramaapp.model.ImportJob;
import com.dramaapp.model.ImportJobStatus;
import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsRecord;
import com.dramaapp.model.RightsRecordStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import com.dramaapp.model.Source;
import com.dramaapp.repository.ImportJobRepository;
import com.dramaapp.repository.RightsRecordRepository;
import com.dramaapp.repository.SeriesRepository;
import com.dramaapp.repository.SourceRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.text.Normalizer;
import java.time.Instant;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.regex.Pattern;

@Slf4j
@Service
@RequiredArgsConstructor
public class ImportService {

    private static final Pattern NONLATIN = Pattern.compile("[^\\w-]");
    private static final Pattern WHITESPACE = Pattern.compile("[\\s]");

    private final ImportJobRepository importJobRepository;
    private final SourceRepository sourceRepository;
    private final SeriesRepository seriesRepository;
    private final RightsRecordRepository rightsRecordRepository;

    public ImportJob createJob(String sourceId) {
        ImportJob job = ImportJob.builder()
                .sourceId(sourceId)
                .startedAt(Instant.now())
                .status(ImportJobStatus.RUNNING)
                .recordsDiscovered(0)
                .recordsImported(0)
                .recordsSkipped(0)
                .build();
        return importJobRepository.save(job);
    }

    public ImportJob updateJob(ImportJob job) {
        return importJobRepository.save(job);
    }

    public PagedResponseDto<ImportJobDto> listJobs(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<ImportJob> jobPage = importJobRepository.findAllByOrderByStartedAtDesc(pageable);
        return PagedResponseDto.from(jobPage.map(this::toDto));
    }

    public ImportJobDto getJob(String id) {
        ImportJob job = importJobRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("ImportJob", "id", id));
        return toDto(job);
    }

    public Series receiveDiscoveredSeries(ImportDiscoveryDto dto) {
        Source source = sourceRepository.findById(dto.getSourceId())
                .orElseThrow(() -> new ResourceNotFoundException("Source", "id", dto.getSourceId()));

        Optional<Series> existingSeries = seriesRepository.findBySourceIdAndSourceUrl(dto.getSourceId(), dto.getSourceUrl());

        Series series;
        if (existingSeries.isPresent()) {
            series = existingSeries.get();
            // Update metadata if needed
            if (dto.getTitle() != null && !dto.getTitle().isBlank()) {
                series.setTitle(dto.getTitle());
            }
            if (dto.getSynopsis() != null) {
                series.setSynopsis(dto.getSynopsis());
            }
            if (dto.getPoster() != null) {
                series.setPoster(dto.getPoster());
            }
            if (dto.getGenres() != null && !dto.getGenres().isEmpty()) {
                series.setGenres(dto.getGenres());
            }
            series.setUpdatedAt(Instant.now());
            series = seriesRepository.save(series);
            log.info("Updated discovered series: {} [{}]", series.getTitle(), series.getId());
        } else {
            String baseSlug = toSlug(dto.getTitle());
            String slug = generateUniqueSlug(baseSlug);

            series = Series.builder()
                    .title(dto.getTitle())
                    .originalTitle(dto.getOriginalTitle())
                    .slug(slug)
                    .synopsis(dto.getSynopsis())
                    .genres(dto.getGenres() != null ? dto.getGenres() : List.of())
                    .language(dto.getLanguage())
                    .poster(dto.getPoster())
                    .sourceId(source.getId())
                    .sourceUrl(dto.getSourceUrl())
                    .publicationStatus(PublicationStatus.DRAFT)
                    .rightsStatus(RightsStatus.DISCOVERED)
                    .seoTitle(dto.getTitle())
                    .seoDescription(dto.getSynopsis())
                    .viewCount(0)
                    .createdAt(Instant.now())
                    .updatedAt(Instant.now())
                    .build();

            series = seriesRepository.save(series);

            // Automatically create a pending RightsRecord for rights team verification
            RightsRecord pendingRights = RightsRecord.builder()
                    .seriesId(series.getId())
                    .rightsHolder(source.getName())
                    .status(RightsRecordStatus.PENDING)
                    .evidenceReference("Scraped from " + dto.getSourceUrl())
                    .streamingAllowed(false)
                    .monetizationAllowed(false)
                    .adaptationAllowed(false)
                    .createdAt(Instant.now())
                    .updatedAt(Instant.now())
                    .build();
            rightsRecordRepository.save(pendingRights);

            log.info("Imported new discovered series: {} [{}]", series.getTitle(), series.getId());
        }

        source.setLastSuccessfulRun(Instant.now());
        sourceRepository.save(source);

        return series;
    }

    public ImportJobDto toDto(ImportJob job) {
        if (job == null) return null;
        return ImportJobDto.builder()
                .id(job.getId())
                .sourceId(job.getSourceId())
                .startedAt(job.getStartedAt())
                .completedAt(job.getCompletedAt())
                .status(job.getStatus())
                .recordsDiscovered(job.getRecordsDiscovered())
                .recordsImported(job.getRecordsImported())
                .recordsSkipped(job.getRecordsSkipped())
                .errorSummary(job.getErrorSummary())
                .build();
    }

    private String toSlug(String input) {
        if (input == null || input.isBlank()) {
            return "series-" + Instant.now().toEpochMilli();
        }
        String nowhitespace = WHITESPACE.matcher(input.trim().toLowerCase(Locale.ROOT)).replaceAll("-");
        String normalized = Normalizer.normalize(nowhitespace, Normalizer.Form.NFD);
        String slug = NONLATIN.matcher(normalized).replaceAll("");
        return slug.replaceAll("-{2,}", "-").replaceAll("^-|-$", "");
    }

    private String generateUniqueSlug(String baseSlug) {
        String slug = baseSlug.isEmpty() ? "series" : baseSlug;
        if (!seriesRepository.existsBySlug(slug)) {
            return slug;
        }
        int counter = 2;
        while (seriesRepository.existsBySlug(slug + "-" + counter)) {
            counter++;
        }
        return slug + "-" + counter;
    }
}
