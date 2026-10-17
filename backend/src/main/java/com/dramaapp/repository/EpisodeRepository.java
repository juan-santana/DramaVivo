package com.dramaapp.repository;

import com.dramaapp.model.Episode;
import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface EpisodeRepository extends MongoRepository<Episode, String> {

    List<Episode> findBySeriesIdOrderBySeasonNumberAscEpisodeNumberAsc(String seriesId);

    Page<Episode> findBySeriesIdOrderBySeasonNumberAscEpisodeNumberAsc(String seriesId, Pageable pageable);

    Page<Episode> findBySeriesIdAndPublicationStatusAndRightsStatusOrderBySeasonNumberAscEpisodeNumberAsc(
            String seriesId,
            PublicationStatus publicationStatus,
            RightsStatus rightsStatus,
            Pageable pageable
    );

    Optional<Episode> findBySeriesIdAndSeasonNumberAndEpisodeNumber(
            String seriesId,
            Integer seasonNumber,
            Integer episodeNumber
    );

    Optional<Episode> findFirstBySeriesIdAndSeasonNumberAndEpisodeNumberGreaterThanOrderByEpisodeNumberAsc(
            String seriesId,
            Integer seasonNumber,
            Integer episodeNumber
    );

    long countBySeriesId(String seriesId);

    void deleteBySeriesId(String seriesId);
}
