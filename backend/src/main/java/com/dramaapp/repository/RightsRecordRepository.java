package com.dramaapp.repository;

import com.dramaapp.model.RightsRecord;
import com.dramaapp.model.RightsRecordStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

@Repository
public interface RightsRecordRepository extends MongoRepository<RightsRecord, String> {

    Page<RightsRecord> findByStatus(RightsRecordStatus status, Pageable pageable);

    List<RightsRecord> findBySeriesId(String seriesId);

    Optional<RightsRecord> findFirstBySeriesIdAndStatus(String seriesId, RightsRecordStatus status);

    Optional<RightsRecord> findFirstBySeriesIdAndEpisodeIdAndStatus(String seriesId, String episodeId, RightsRecordStatus status);

    Optional<RightsRecord> findBySeriesIdAndEpisodeIdIsNull(String seriesId);

    List<RightsRecord> findByStatusAndExpiresAtBefore(RightsRecordStatus status, Instant expiryThreshold);

    long countByStatus(RightsRecordStatus status);
}
