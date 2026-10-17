package com.dramaapp.service;

import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.RightsApprovalDto;
import com.dramaapp.dto.RightsRecordDto;
import com.dramaapp.dto.TakedownRequestDto;
import com.dramaapp.exception.ResourceNotFoundException;
import com.dramaapp.exception.RightsViolationException;
import com.dramaapp.model.PublicationStatus;
import com.dramaapp.model.RightsRecord;
import com.dramaapp.model.RightsRecordStatus;
import com.dramaapp.model.RightsStatus;
import com.dramaapp.model.Series;
import com.dramaapp.repository.EpisodeRepository;
import com.dramaapp.repository.RightsRecordRepository;
import com.dramaapp.repository.SeriesRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class RightsService {

    private final RightsRecordRepository rightsRecordRepository;
    private final SeriesRepository seriesRepository;
    private final EpisodeRepository episodeRepository;
    private final AuditService auditService;

    public PagedResponseDto<RightsRecordDto> getPendingReviews(int page, int size) {
        Pageable pageable = PageRequest.of(page, size);
        Page<RightsRecord> pendingPage = rightsRecordRepository.findByStatus(RightsRecordStatus.PENDING, pageable);
        return PagedResponseDto.from(pendingPage.map(this::toDto));
    }

    public RightsRecordDto approve(String id, RightsApprovalDto approvalDto, String adminUsername) {
        RightsRecord record = rightsRecordRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("RightsRecord", "id", id));

        record.setStatus(approvalDto.getApproved() ? RightsRecordStatus.APPROVED : RightsRecordStatus.REJECTED);
        record.setReviewedAt(Instant.now());
        record.setReviewedBy(adminUsername);
        record.setReviewNotes(approvalDto.getReviewNotes());

        if (approvalDto.getAuthorizationType() != null) {
            record.setAuthorizationType(approvalDto.getAuthorizationType());
        }
        if (approvalDto.getAllowedTerritories() != null) {
            record.setAllowedTerritories(approvalDto.getAllowedTerritories());
        }
        if (approvalDto.getStartsAt() != null) {
            record.setStartsAt(approvalDto.getStartsAt());
        }
        if (approvalDto.getExpiresAt() != null) {
            record.setExpiresAt(approvalDto.getExpiresAt());
        }
        if (approvalDto.getStreamingAllowed() != null) {
            record.setStreamingAllowed(approvalDto.getStreamingAllowed());
        }
        if (approvalDto.getMonetizationAllowed() != null) {
            record.setMonetizationAllowed(approvalDto.getMonetizationAllowed());
        }
        if (approvalDto.getAdaptationAllowed() != null) {
            record.setAdaptationAllowed(approvalDto.getAdaptationAllowed());
        }
        record.setUpdatedAt(Instant.now());

        RightsRecord savedRecord = rightsRecordRepository.save(record);

        // Update Series rights status
        if (record.getSeriesId() != null) {
            seriesRepository.findById(record.getSeriesId()).ifPresent(series -> {
                if (savedRecord.getStatus() == RightsRecordStatus.APPROVED) {
                    series.setRightsStatus(RightsStatus.APPROVED);
                } else {
                    series.setRightsStatus(RightsStatus.BLOCKED);
                }
                series.setUpdatedAt(Instant.now());
                seriesRepository.save(series);
            });
        }

        auditService.logAction(
                adminUsername,
                savedRecord.getStatus() == RightsRecordStatus.APPROVED ? "APPROVE_RIGHTS" : "REJECT_RIGHTS",
                "RIGHTS_RECORD",
                savedRecord.getId(),
                "Decision notes: " + approvalDto.getReviewNotes()
        );

        return toDto(savedRecord);
    }

    public RightsRecordDto reject(String id, String reason, String adminUsername) {
        RightsApprovalDto rejectDto = RightsApprovalDto.builder()
                .approved(false)
                .reviewNotes(reason)
                .build();
        return approve(id, rejectDto, adminUsername);
    }

    public void checkRightsValid(String seriesId, String episodeId) {
        Series series = seriesRepository.findById(seriesId)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", seriesId));

        if (series.getRightsStatus() != RightsStatus.APPROVED && series.getRightsStatus() != RightsStatus.PUBLISHED) {
            throw new RightsViolationException("Content is currently blocked or rights not approved for series: " + series.getTitle());
        }

        // Check if there is an active rights record
        RightsRecord rightsRecord = rightsRecordRepository.findFirstBySeriesIdAndStatus(seriesId, RightsRecordStatus.APPROVED)
                .orElseThrow(() -> new RightsViolationException("No approved rights agreement found for series: " + series.getTitle()));

        Instant now = Instant.now();
        if (rightsRecord.getStartsAt() != null && now.isBefore(rightsRecord.getStartsAt())) {
            throw new RightsViolationException("Streaming rights period has not started yet.");
        }

        if (rightsRecord.getExpiresAt() != null && now.isAfter(rightsRecord.getExpiresAt())) {
            throw new RightsViolationException("Streaming rights agreement has expired.");
        }

        if (!rightsRecord.isStreamingAllowed()) {
            throw new RightsViolationException("Streaming is explicitly not allowed under current rights agreement.");
        }
    }

    @Scheduled(cron = "0 0 * * * *") // Every hour
    public void expireOutdated() {
        log.info("Running scheduled check for expired rights records...");
        Instant now = Instant.now();
        List<RightsRecord> expiredRecords = rightsRecordRepository.findByStatusAndExpiresAtBefore(RightsRecordStatus.APPROVED, now);

        for (RightsRecord record : expiredRecords) {
            record.setStatus(RightsRecordStatus.EXPIRED);
            record.setUpdatedAt(now);
            rightsRecordRepository.save(record);

            if (record.getSeriesId() != null) {
                seriesRepository.findById(record.getSeriesId()).ifPresent(series -> {
                    series.setRightsStatus(RightsStatus.BLOCKED);
                    series.setPublicationStatus(PublicationStatus.ARCHIVED);
                    series.setUpdatedAt(now);
                    seriesRepository.save(series);
                    log.warn("Blocked series '{}' [{}] due to expired rights.", series.getTitle(), series.getId());
                });
            }

            auditService.logAction("SYSTEM", "EXPIRE_RIGHTS", "RIGHTS_RECORD", record.getId(), "Rights expired automatically");
        }

        if (!expiredRecords.isEmpty()) {
            log.info("Expired {} outdated rights records.", expiredRecords.size());
        }
    }

    public void createTakedown(String seriesId, TakedownRequestDto request, String adminUsername) {
        Series series = seriesRepository.findById(seriesId)
                .orElseThrow(() -> new ResourceNotFoundException("Series", "id", seriesId));

        series.setRightsStatus(request.isImmediate() ? RightsStatus.REMOVED : RightsStatus.TAKEDOWN_PENDING);
        series.setPublicationStatus(PublicationStatus.ARCHIVED);
        series.setUpdatedAt(Instant.now());
        seriesRepository.save(series);

        // Revoke active rights records
        List<RightsRecord> records = rightsRecordRepository.findBySeriesId(seriesId);
        for (RightsRecord rec : records) {
            rec.setStatus(RightsRecordStatus.REVOKED);
            rec.setReviewNotes("Takedown issued: " + request.getReason() + " (Ref: " + request.getLegalReference() + ")");
            rec.setUpdatedAt(Instant.now());
            rightsRecordRepository.save(rec);
        }

        auditService.logAction(
                adminUsername,
                "TAKEDOWN",
                "SERIES",
                seriesId,
                "Takedown processed: " + request.getReason() + " | Ref: " + request.getLegalReference()
        );
        log.warn("Takedown executed on series [{}] by {}. Reason: {}", seriesId, adminUsername, request.getReason());
    }

    public RightsRecordDto toDto(RightsRecord record) {
        if (record == null) return null;
        return RightsRecordDto.builder()
                .id(record.getId())
                .seriesId(record.getSeriesId())
                .episodeId(record.getEpisodeId())
                .rightsHolder(record.getRightsHolder())
                .authorizationType(record.getAuthorizationType())
                .allowedTerritories(record.getAllowedTerritories())
                .streamingAllowed(record.isStreamingAllowed())
                .monetizationAllowed(record.isMonetizationAllowed())
                .adaptationAllowed(record.isAdaptationAllowed())
                .startsAt(record.getStartsAt())
                .expiresAt(record.getExpiresAt())
                .evidenceReference(record.getEvidenceReference())
                .reviewedAt(record.getReviewedAt())
                .reviewedBy(record.getReviewedBy())
                .reviewNotes(record.getReviewNotes())
                .status(record.getStatus())
                .createdAt(record.getCreatedAt())
                .updatedAt(record.getUpdatedAt())
                .build();
    }
}
