// MongoDB initialization script for DramaApp
// This runs automatically when the mongo container is first created.

db = db.getSiblingDB('dramaapp');

// Create collections with validation
db.createCollection('sources');
db.createCollection('series');
db.createCollection('episodes');
db.createCollection('rightsRecords');
db.createCollection('videoAssets');
db.createCollection('importJobs');
db.createCollection('analyticsEvents');
db.createCollection('users');

// --- Indexes ---

// Sources
db.sources.createIndex({ name: 1 }, { unique: true });
db.sources.createIndex({ enabled: 1 });

// Series
db.series.createIndex({ slug: 1 }, { unique: true });
db.series.createIndex({ title: 'text', originalTitle: 'text', synopsis: 'text' });
db.series.createIndex({ genres: 1 });
db.series.createIndex({ sourceId: 1 });
db.series.createIndex({ publicationStatus: 1 });
db.series.createIndex({ rightsStatus: 1 });
db.series.createIndex({ createdAt: -1 });
db.series.createIndex({ sourceId: 1, sourceUrl: 1 }, { unique: true, sparse: true });

// Episodes
db.episodes.createIndex({ seriesId: 1, seasonNumber: 1, episodeNumber: 1 }, { unique: true });
db.episodes.createIndex({ seriesId: 1 });
db.episodes.createIndex({ publicationStatus: 1 });
db.episodes.createIndex({ videoAssetId: 1 });

// Rights Records
db.rightsRecords.createIndex({ seriesId: 1 });
db.rightsRecords.createIndex({ episodeId: 1 });
db.rightsRecords.createIndex({ status: 1 });
db.rightsRecords.createIndex({ expiresAt: 1 });
db.rightsRecords.createIndex({ seriesId: 1, status: 1 });

// Video Assets
db.videoAssets.createIndex({ provider: 1, providerAssetId: 1 }, { unique: true });
db.videoAssets.createIndex({ processingStatus: 1 });

// Import Jobs
db.importJobs.createIndex({ sourceId: 1 });
db.importJobs.createIndex({ status: 1 });
db.importJobs.createIndex({ startedAt: -1 });

// Analytics Events (TTL: 90 days)
db.analyticsEvents.createIndex({ timestamp: 1 }, { expireAfterSeconds: 7776000 });
db.analyticsEvents.createIndex({ eventType: 1 });
db.analyticsEvents.createIndex({ seriesId: 1 });
db.analyticsEvents.createIndex({ anonymousSessionId: 1 });

// Users
db.users.createIndex({ username: 1 }, { unique: true });

print('DramaApp MongoDB initialized successfully with collections and indexes.');
