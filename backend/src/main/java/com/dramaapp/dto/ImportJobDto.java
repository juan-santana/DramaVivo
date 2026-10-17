package com.dramaapp.dto;

import com.dramaapp.model.ImportJobStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ImportJobDto {
    private String id;
    private String sourceId;
    private Instant startedAt;
    private Instant completedAt;
    private ImportJobStatus status;
    private int recordsDiscovered;
    private int recordsImported;
    private int recordsSkipped;
    private String errorSummary;
}
