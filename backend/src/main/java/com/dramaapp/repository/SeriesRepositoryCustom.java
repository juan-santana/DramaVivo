package com.dramaapp.repository;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface SeriesRepositoryCustom {
    Page<Series> searchPublished(String query, String genre, String language, Pageable pageable);
    List<String> findDistinctGenresByPublicationStatusAndRightsStatus(PublicationStatus pubStatus, RightsStatus rightsStatus);
    void incrementViewCount(String seriesId);
}
