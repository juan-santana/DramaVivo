package com.dramaapp.repository;

import com.dramaapp.model.Source;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SourceRepository extends MongoRepository<Source, String> {
    Optional<Source> findByName(String name);
    List<Source> findByEnabled(boolean enabled);
    Page<Source> findByEnabled(boolean enabled, Pageable pageable);
}
