package com.dramaapp.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.CompoundIndexes;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.index.TextIndexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "series")
@CompoundIndexes({
    @CompoundIndex(name = "source_sourceUrl_idx", def = "{'sourceId': 1, 'sourceUrl': 1}"),
    @CompoundIndex(name = "pub_rights_idx", def = "{'publicationStatus': 1, 'rightsStatus': 1}"),
    @CompoundIndex(name = "pub_rights_genre_idx", def = "{'publicationStatus': 1, 'rightsStatus': 1, 'genres': 1}")
})
public class Series {

    @Id
    private String id;

    @Indexed(unique = true)
    private String slug;

    @TextIndexed(weight = 3.0f)
    private String title;

    private String originalTitle;

    @TextIndexed(weight = 1.0f)
    private String synopsis;

    @Builder.Default
    private List<String> genres = new ArrayList<>();

    @Indexed
    private String language;

    private String poster;

    private String sourceId;

    private String sourceUrl;

    @Indexed
    private PublicationStatus publicationStatus;

    @Indexed
    private RightsStatus rightsStatus;

    private String seoTitle;

    private String seoDescription;

    private long viewCount;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
