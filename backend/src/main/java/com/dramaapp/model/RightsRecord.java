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
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "rights_records")
@CompoundIndexes({
    @CompoundIndex(name = "series_rights_status_idx", def = "{'seriesId': 1, 'status': 1}"),
    @CompoundIndex(name = "status_expires_idx", def = "{'status': 1, 'expiresAt': 1}")
})
public class RightsRecord {

    @Id
    private String id;

    @Indexed
    private String seriesId;

    @Indexed
    private String episodeId;

    private String rightsHolder;

    private AuthorizationType authorizationType;

    @Builder.Default
    private List<String> allowedTerritories = new ArrayList<>();

    private boolean streamingAllowed;

    private boolean monetizationAllowed;

    private boolean adaptationAllowed;

    private Instant startsAt;

    @Indexed
    private Instant expiresAt;

    private String evidenceReference;

    private Instant reviewedAt;

    private String reviewedBy;

    private String reviewNotes;

    @Indexed
    private RightsRecordStatus status;

    @CreatedDate
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}
