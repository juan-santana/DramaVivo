package com.dramaapp.service;

import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SeriesCreateDto;
import com.dramaapp.dto.SeriesDto;
import com.dramaapp.dto.SeriesUpdateDto;
import com.dramaapp.exception.ResourceNotFoundException;
import com.dramaapp.exception.RightsViolationException;
import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsRecord;
import com.dramaapp.model.RightsRecordStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import com.dramaapp.repository.EpisodeRepository;
import com.dramaapp.repository.RightsRecordRepository;
import com.dramaapp.repository.SeriesRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.text.Normalizer;
import java.time.Instant;
import java.util.List;
import java.util.Locale;
import java.util.regex.Pattern;

@Slf4j
@Service
@RequiredArgsConstructor
public class SeriesService {

    private static final Pattern NONLATIN = Pattern.compile("[^\\w-]");
    private static final Pattern WHITESPACE = Pattern.compile("[\\s]");

    private final SeriesRepository seriesRepository;
    private final EpisodeRepository episodeRepository;
    private final RightsRecordRepository rightsRecordRepository;
    private final AuditService auditService;

    public PagedResponseDto<SeriesDto> listPublished(int page, int size, String genre, String language, String sortBy, String sortDir) {
        Sort.Direction direction = "asc".equalsIgnoreCase(sortDir) ? Sort.Direction.ASC : Sort.Direction.DESC;
        String sortProperty = (sortBy != null && !sortBy.isBlank()) ? sortBy : "createdAt";
        Pageable pageable = PageRequest.of(page, size, Sort.by(direction, sortProperty));

        Page<Series> seriesPage;
        if (genre != null && !genre.isBlank() && language != null && !language.isBlank()) {
            seriesPage = seriesRepository.findByPublicationStatusAndRightsStatusAndGenresContainingAndLanguage(
                    PublicationStatus.PUBLISHED, RightsStatus.APPROVED, genre.trim(), language.trim(), pageable);
        } else if (genre != null && !genre.isBlank()) {
            seriesPage = seriesRepository.findByPublicationStatusAndRightsStatusAndGenresContaining(
                    PublicationStatus.PUBLISHED, RightsStatus.APPROVED, genre.trim(), pageable);
        } else if (language != null && !language.isBlank()) {
            seriesPage = seriesRepository.findByPublicationStatusAndRightsStatusAndLanguage(
                    PublicationStatus.PUBLISHED, RightsStatus.APPROVED, language.trim(), pageable);
        } else {
            seriesPage = seriesRepository.findByPublicationStatusAndRightsStatus(
                    PublicationStatus.PUBLISHED, RightsStatus.APPROVED, pageable);
        }

        return PagedResponseDto.from(seriesPage.map(this::toDto));
    }

    public SeriesDto getBySlug(String slug) {
        Series series = seriesRepository.findBySlug(slug)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "slug", slug));

        if (series.getPublicationStatus() != PublicationStatus.PUBLISHED || series.getRightsStatus() != RightsStatus.APPROVED) {
            throw new RightsViolationException("Series is not available for streaming");
        }

        seriesRepository.incrementViewCount(series.getId());
        series.setViewCount(series.getViewCount() + 1);

        return toDto(series);
    }

    public SeriesDto getById(String id) {
        Series series = seriesRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", id));
        return toDto(series);
    }

    public PagedResponseDto<SeriesDto> search(String query, String genre, String language, int page, int size, String sortBy, String sortDir) {
        Sort.Direction direction = "asc".equalsIgnoreCase(sortDir) ? Sort.Direction.ASC : Sort.Direction.DESC;
        String sortProperty = (sortBy != null && !sortBy.isBlank()) ? sortBy : "createdAt";
        Pageable pageable = PageRequest.of(page, size, Sort.by(direction, sortProperty));

        Page<Series> seriesPage = seriesRepository.searchPublished(query, genre, language, pageable);
        return PagedResponseDto.from(seriesPage.map(this::toDto));
    }

    public SeriesDto create(SeriesCreateDto dto, String adminUsername) {
        String baseSlug = toSlug(dto.getTitle());
        String slug = generateUniqueSlug(baseSlug);

        Series series = Series.builder()
                .title(dto.getTitle())
                .originalTitle(dto.getOriginalTitle())
                .slug(slug)
                .synopsis(dto.getSynopsis())
                .genres(dto.getGenres() != null ? dto.getGenres() : List.of())
                .language(dto.getLanguage())
                .poster(dto.getPoster())
                .sourceId(dto.getSourceId())
                .sourceUrl(dto.getSourceUrl())
                .publicationStatus(dto.getPublicationStatus() != null ? dto.getPublicationStatus() : PublicationStatus.DRAFT)
                .rightsStatus(dto.getRightsStatus() != null ? dto.getRightsStatus() : RightsStatus.DISCOVERED)
                .seoTitle(dto.getSeoTitle() != null ? dto.getSeoTitle() : dto.getTitle())
                .seoDescription(dto.getSeoDescription())
                .viewCount(0)
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .build();

        Series saved = seriesRepository.save(series);

        // Create initial pending RightsRecord if created in DRAFT or RIGHTS_PENDING
        RightsRecord rightsRecord = RightsRecord.builder()
                .seriesId(saved.getId())
                .rightsHolder("To Be Verified")
                .status(RightsRecordStatus.PENDING)
                .streamingAllowed(false)
                .monetizationAllowed(false)
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .build();
        rightsRecordRepository.save(rightsRecord);

        auditService.logAction(adminUsername, "CREATE", "SERIES", saved.getId(), "Created series: " + saved.getTitle());
        return toDto(saved);
    }

    public SeriesDto update(String id, SeriesUpdateDto dto, String adminUsername) {
        Series series = seriesRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", id));

        if (dto.getTitle() != null && !dto.getTitle().isBlank()) {
            series.setTitle(dto.getTitle());
        }
        if (dto.getOriginalTitle() != null) {
            series.setOriginalTitle(dto.getOriginalTitle());
        }
        if (dto.getSynopsis() != null) {
            series.setSynopsis(dto.getSynopsis());
        }
        if (dto.getGenres() != null) {
            series.setGenres(dto.getGenres());
        }
        if (dto.getLanguage() != null) {
            series.setLanguage(dto.getLanguage());
        }
        if (dto.getPoster() != null) {
            series.setPoster(dto.getPoster());
        }
        if (dto.getPublicationStatus() != null) {
            series.setPublicationStatus(dto.getPublicationStatus());
        }
        if (dto.getRightsStatus() != null) {
            series.setRightsStatus(dto.getRightsStatus());
        }
        if (dto.getSeoTitle() != null) {
            series.setSeoTitle(dto.getSeoTitle());
        }
        if (dto.getSeoDescription() != null) {
            series.setSeoDescription(dto.getSeoDescription());
        }
        series.setUpdatedAt(Instant.now());

        Series saved = seriesRepository.save(series);
        auditService.logAction(adminUsername, "UPDATE", "SERIES", saved.getId(), "Updated series: " + saved.getTitle());
        return toDto(saved);
    }

    public void delete(String id, String adminUsername) {
        Series series = seriesRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", id));

        episodeRepository.deleteBySeriesId(id);
        seriesRepository.delete(series);

        auditService.logAction(adminUsername, "DELETE", "SERIES", id, "Deleted series and episodes: " + series.getTitle());
    }

    public List<String> getGenres() {
        return seriesRepository.findDistinctGenresByPublicationStatusAndRightsStatus(
                PublicationStatus.PUBLISHED, RightsStatus.APPROVED);
    }

    public PagedResponseDto<SeriesDto> listAdmin(PublicationStatus pubStatus, RightsStatus rightsStatus, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        Page<Series> seriesPage;

        if (pubStatus != null && rightsStatus != null) {
            seriesPage = seriesRepository.findByPublicationStatusAndRightsStatus(pubStatus, rightsStatus, pageable);
        } else if (pubStatus != null) {
            seriesPage = seriesRepository.findByPublicationStatus(pubStatus, pageable);
        } else if (rightsStatus != null) {
            seriesPage = seriesRepository.findByRightsStatus(rightsStatus, pageable);
        } else {
            seriesPage = seriesRepository.findAll(pageable);
        }

        return PagedResponseDto.from(seriesPage.map(this::toDto));
    }

    public SeriesDto toDto(Series series) {
        if (series == null) return null;
        long episodeCount = episodeRepository.countBySeriesId(series.getId());
        return SeriesDto.builder()
                .id(series.getId())
                .slug(series.getSlug())
                .title(series.getTitle())
                .originalTitle(series.getOriginalTitle())
                .synopsis(series.getSynopsis())
                .genres(series.getGenres())
                .language(series.getLanguage())
                .poster(series.getPoster())
                .sourceId(series.getSourceId())
                .sourceUrl(series.getSourceUrl())
                .publicationStatus(series.getPublicationStatus())
                .rightsStatus(series.getRightsStatus())
                .seoTitle(series.getSeoTitle())
                .seoDescription(series.getSeoDescription())
                .viewCount(series.getViewCount())
                .episodeCount(episodeCount)
                .createdAt(series.getCreatedAt())
                .updatedAt(series.getUpdatedAt())
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
