package com.dramaapp.dto;

import com.dramaapp.model.AuthorizationType;
import com.dramaapp.model.RightsRecordStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RightsRecordDto {
    private String id;
    private String seriesId;
    private String episodeId;
    private String rightsHolder;
    private AuthorizationType authorizationType;
    private List<String> allowedTerritories;
    private boolean streamingAllowed;
    private boolean monetizationAllowed;
    private boolean adaptationAllowed;
    private Instant startsAt;
    private Instant expiresAt;
    private String evidenceReference;
    private Instant reviewedAt;
    private String reviewedBy;
    private String reviewNotes;
    private RightsRecordStatus status;
    private Instant createdAt;
    private Instant updatedAt;
}
