package com.dramaapp.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "import_jobs")
public class ImportJob {

    @Id
    private String id;

    @Indexed
    private String sourceId;

    private Instant startedAt;

    private Instant completedAt;

    @Indexed
    private ImportJobStatus status;

    private int recordsDiscovered;

    private int recordsImported;

    private int recordsSkipped;

    private String errorSummary;
}
