package com.dramaapp.dto;

import com.dramaapp.model.AuthorizationType;
import jakarta.validation.constraints.NotNull;
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
public class RightsApprovalDto {

    @NotNull(message = "Approval decision is required")
    private Boolean approved;

    private String reviewNotes;

    private AuthorizationType authorizationType;

    private List<String> allowedTerritories;

    private Instant startsAt;

    private Instant expiresAt;

    @Builder.Default
    private Boolean streamingAllowed = true;

    @Builder.Default
    private Boolean monetizationAllowed = true;

    @Builder.Default
    private Boolean adaptationAllowed = false;
}
