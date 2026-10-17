package com.dramaapp.service;

import com.dramaapp.dto.EpisodeCreateDto;
import com.dramaapp.dto.EpisodeDto;
import com.dramaapp.dto.EpisodeUpdateDto;
import com.dramaapp.dto.NextEpisodeDto;
import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.PlaybackResponseDto;
import com.dramaapp.exception.ResourceNotFoundException;
import com.dramaapp.model.Episode;
import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import com.dramaapp.repository.EpisodeRepository;
import com.dramaapp.repository.SeriesRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class EpisodeService {

    private final EpisodeRepository episodeRepository;
    private final SeriesRepository seriesRepository;
    private final RightsService rightsService;
    private final VideoService videoService;
    private final AuditService auditService;

    public PagedResponseDto<EpisodeDto> getEpisodesForSeriesSlug(String slug, int page, int size) {
        Series series = seriesRepository.findBySlug(slug)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "slug", slug));

        Pageable pageable = PageRequest.of(page, size);
        Page<Episode> episodePage = episodeRepository.findBySeriesIdAndPublicationStatusAndRightsStatusOrderBySeasonNumberAscEpisodeNumberAsc(
                series.getId(), PublicationStatus.PUBLISHED, RightsStatus.APPROVED, pageable);

        return PagedResponseDto.from(episodePage.map(this::toDto));
    }

    public PagedResponseDto<EpisodeDto> getEpisodesForSeries(String seriesId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<Episode> episodePage = episodeRepository.findBySeriesIdOrderBySeasonNumberAscEpisodeNumberAsc(seriesId, pageable);
        return PagedResponseDto.from(episodePage.map(this::toDto));
    }

    public EpisodeDto getById(String id) {
        Episode episode = episodeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Episode", "id", id));
        rightsService.checkRightsValid(episode.getSeriesId(), episode.getId());
        return toDto(episode);
    }

    public PlaybackResponseDto getPlayback(String episodeId) {
        Episode episode = episodeRepository.findById(episodeId)
                .orElseThrow(() -> new ResourceNotFoundException("Episode", "id", episodeId));

        Series series = seriesRepository.findById(episode.getSeriesId())
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", episode.getSeriesId()));

        // Validate rights
        rightsService.checkRightsValid(episode.getSeriesId(), episode.getId());

        // Generate playback URL
        String playbackUrl = null;
        if (episode.getVideoAssetId() != null) {
            playbackUrl = videoService.generatePlaybackUrl(episode.getVideoAssetId());
        }

        // Find next episode in series
        NextEpisodeDto nextEpisodeDto = null;
        Optional<Episode> nextEpisode = episodeRepository.findFirstBySeriesIdAndSeasonNumberAndEpisodeNumberGreaterThanOrderByEpisodeNumberAsc(
                episode.getSeriesId(), episode.getSeasonNumber(), episode.getEpisodeNumber());
        if (nextEpisode.isPresent()) {
            Episode next = nextEpisode.get();
            nextEpisodeDto = NextEpisodeDto.builder()
                    .episodeId(next.getId())
                    .seasonNumber(next.getSeasonNumber())
                    .episodeNumber(next.getEpisodeNumber())
                    .title(next.getTitle())
                    .build();
        }

        return PlaybackResponseDto.builder()
                .episodeId(episode.getId())
                .seriesId(series.getId())
                .seriesTitle(series.getTitle())
                .episodeTitle(episode.getTitle())
                .seasonNumber(episode.getSeasonNumber())
                .episodeNumber(episode.getEpisodeNumber())
                .playbackUrl(playbackUrl)
                .thumbnailUrl(episode.getThumbnail())
                .durationSeconds(episode.getDurationSeconds())
                .subtitleTracks(episode.getSubtitleTracks())
                .nextEpisode(nextEpisodeDto)
                .build();
    }

    public EpisodeDto create(EpisodeCreateDto dto, String adminUsername) {
        Series series = seriesRepository.findById(dto.getSeriesId())
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", dto.getSeriesId()));

        // Check if episode with same season and number already exists
        episodeRepository.findBySeriesIdAndSeasonNumberAndEpisodeNumber(
                series.getId(), dto.getSeasonNumber(), dto.getEpisodeNumber()
        ).ifPresent(e -> {
            throw new IllegalArgumentException(String.format("Episode %d already exists for season %d", dto.getEpisodeNumber(), dto.getSeasonNumber()));
        });

        Episode episode = Episode.builder()
                .seriesId(series.getId())
                .seasonNumber(dto.getSeasonNumber())
                .episodeNumber(dto.getEpisodeNumber())
                .title(dto.getTitle())
                .synopsis(dto.getSynopsis())
                .durationSeconds(dto.getDurationSeconds())
                .videoAssetId(dto.getVideoAssetId())
                .subtitleTracks(dto.getSubtitleTracks() != null ? dto.getSubtitleTracks() : java.util.List.of())
                .thumbnail(dto.getThumbnail())
                .publicationStatus(dto.getPublicationStatus() != null ? dto.getPublicationStatus() : PublicationStatus.DRAFT)
                .rightsStatus(dto.getRightsStatus() != null ? dto.getRightsStatus() : series.getRightsStatus())
                .createdAt(Instant.now())
                .updatedAt(Instant.now())
                .build();

        Episode saved = episodeRepository.save(episode);
        auditService.logAction(adminUsername, "CREATE", "EPISODE", saved.getId(), "Created episode: " + saved.getTitle() + " for series: " + series.getTitle());
        return toDto(saved);
    }

    public EpisodeDto update(String id, EpisodeUpdateDto dto, String adminUsername) {
        Episode episode = episodeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Episode", "id", id));

        if (dto.getSeasonNumber() != null) {
            episode.setSeasonNumber(dto.getSeasonNumber());
        }
        if (dto.getEpisodeNumber() != null) {
            episode.setEpisodeNumber(dto.getEpisodeNumber());
        }
        if (dto.getTitle() != null && !dto.getTitle().isBlank()) {
            episode.setTitle(dto.getTitle());
        }
        if (dto.getSynopsis() != null) {
            episode.setSynopsis(dto.getSynopsis());
        }
        if (dto.getDurationSeconds() != null) {
            episode.setDurationSeconds(dto.getDurationSeconds());
        }
        if (dto.getVideoAssetId() != null) {
            episode.setVideoAssetId(dto.getVideoAssetId());
        }
        if (dto.getSubtitleTracks() != null) {
            episode.setSubtitleTracks(dto.getSubtitleTracks());
        }
        if (dto.getThumbnail() != null) {
            episode.setThumbnail(dto.getThumbnail());
        }
        if (dto.getPublicationStatus() != null) {
            episode.setPublicationStatus(dto.getPublicationStatus());
        }
        if (dto.getRightsStatus() != null) {
            episode.setRightsStatus(dto.getRightsStatus());
        }
        episode.setUpdatedAt(Instant.now());

        Episode saved = episodeRepository.save(episode);
        auditService.logAction(adminUsername, "UPDATE", "EPISODE", saved.getId(), "Updated episode: " + saved.getTitle());
        return toDto(saved);
    }

    public void delete(String id, String adminUsername) {
        Episode episode = episodeRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Episode", "id", id));
        episodeRepository.delete(episode);
        auditService.logAction(adminUsername, "DELETE", "EPISODE", id, "Deleted episode: " + episode.getTitle());
    }

    public EpisodeDto toDto(Episode episode) {
        if (episode == null) return null;
        return EpisodeDto.builder()
                .id(episode.getId())
                .seriesId(episode.getSeriesId())
                .seasonNumber(episode.getSeasonNumber())
                .episodeNumber(episode.getEpisodeNumber())
                .title(episode.getTitle())
                .synopsis(episode.getSynopsis())
                .durationSeconds(episode.getDurationSeconds())
                .videoAssetId(episode.getVideoAssetId())
                .subtitleTracks(episode.getSubtitleTracks())
                .thumbnail(episode.getThumbnail())
                .publicationStatus(episode.getPublicationStatus())
                .rightsStatus(episode.getRightsStatus())
                .createdAt(episode.getCreatedAt())
                .updatedAt(episode.getUpdatedAt())
                .build();
    }
}
