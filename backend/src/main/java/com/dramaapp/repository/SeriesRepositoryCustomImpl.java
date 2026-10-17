package com.dramaapp.repository;

import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.TextCriteria;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@RequiredArgsConstructor
public class SeriesRepositoryCustomImpl implements SeriesRepositoryCustom {

    private final MongoTemplate mongoTemplate;

    @Override
    public Page<Series> searchPublished(String query, String genre, String language, Pageable pageable) {
        Query q = new Query();
        q.addCriteria(Criteria.where("publicationStatus").is(PublicationStatus.PUBLISHED));
        q.addCriteria(Criteria.where("rightsStatus").is(RightsStatus.APPROVED));

        if (query != null && !query.trim().isEmpty()) {
            q.addCriteria(new Criteria().orOperator(
                Criteria.where("title").regex(query.trim(), "i"),
                Criteria.where("originalTitle").regex(query.trim(), "i"),
                Criteria.where("synopsis").regex(query.trim(), "i")
            ));
        }

        if (genre != null && !genre.trim().isEmpty()) {
            q.addCriteria(Criteria.where("genres").is(genre.trim()));
        }

        if (language != null && !language.trim().isEmpty()) {
            q.addCriteria(Criteria.where("language").regex(language.trim(), "i"));
        }

        long total = mongoTemplate.count(q, Series.class);
        q.with(pageable);
        List<Series> list = mongoTemplate.find(q, Series.class);

        return new PageImpl<>(list, pageable, total);
    }

    @Override
    public List<String> findDistinctGenresByPublicationStatusAndRightsStatus(PublicationStatus pubStatus, RightsStatus rightsStatus) {
        Query q = new Query();
        q.addCriteria(Criteria.where("publicationStatus").is(pubStatus));
        q.addCriteria(Criteria.where("rightsStatus").is(rightsStatus));
        return mongoTemplate.findDistinct(q, "genres", Series.class, String.class);
    }

    @Override
    public void incrementViewCount(String seriesId) {
        Query q = new Query(Criteria.where("id").is(seriesId));
        Update update = new Update().inc("viewCount", 1);
        mongoTemplate.updateFirst(q, update, Series.class);
    }
}
