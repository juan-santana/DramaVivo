package com.dramaapp.repository;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SeriesRepository extends MongoRepository<Series, String>, SeriesRepositoryCustom {

    Optional<Series> findBySlug(String slug);

    Optional<Series> findBySourceIdAndSourceUrl(String sourceId, String sourceUrl);

    boolean existsBySlug(String slug);

    Page<Series> findByPublicationStatusAndRightsStatus(
            PublicationStatus publicationStatus,
            RightsStatus rightsStatus,
            Pageable pageable
    );

    Page<Series> findByPublicationStatusAndRightsStatusAndGenresContaining(
            PublicationStatus publicationStatus,
            RightsStatus rightsStatus,
            String genre,
            Pageable pageable
    );

    Page<Series> findByPublicationStatusAndRightsStatusAndLanguage(
            PublicationStatus publicationStatus,
            RightsStatus rightsStatus,
            String language,
            Pageable pageable
    );

    Page<Series> findByPublicationStatusAndRightsStatusAndGenresContainingAndLanguage(
            PublicationStatus publicationStatus,
            RightsStatus rightsStatus,
            String genre,
            String language,
            Pageable pageable
    );

    Page<Series> findByPublicationStatus(PublicationStatus publicationStatus, Pageable pageable);

    Page<Series> findByRightsStatus(RightsStatus rightsStatus, Pageable pageable);

    long countByPublicationStatusAndRightsStatus(PublicationStatus publicationStatus, RightsStatus rightsStatus);
}
