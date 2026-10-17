package com.dramaapp.repository;

import com.dramaapp.model.ImportJob;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ImportJobRepository extends MongoRepository<ImportJob, String> {

    List<ImportJob> findBySourceIdOrderByStartedAtDesc(String sourceId);

    Page<ImportJob> findAllByOrderByStartedAtDesc(Pageable pageable);

    Page<ImportJob> findBySourceIdOrderByStartedAtDesc(String sourceId, Pageable pageable);
}
