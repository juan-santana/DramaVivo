package com.dramaapp.repository;

import com.dramaapp.model.VideoAsset;
import com.dramaapp.model.VideoProcessingStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface VideoAssetRepository extends MongoRepository<VideoAsset, String> {

    Optional<VideoAsset> findByProviderAndProviderAssetId(String provider, String providerAssetId);

    List<VideoAsset> findByProcessingStatus(VideoProcessingStatus status);

    Page<VideoAsset> findByProcessingStatus(VideoProcessingStatus status, Pageable pageable);
}
