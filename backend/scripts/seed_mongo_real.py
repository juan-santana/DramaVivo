import json
from datetime import datetime, timezone
from pymongo import MongoClient

print("Conectando a MongoDB en localhost:27017...")
client = MongoClient('mongodb://localhost:27017/')
db = client['dramaapp']

with open('E:/DramaApp/scraper/output/dramashorts_real_catalog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

series_list = data['series']
episodes_dict = data['episodes']

print(f"Limpiando colecciones anteriores e insertando {len(series_list)} series...")
db.series.delete_many({})
db.episodes.delete_many({})
db.sources.delete_many({})

# Insert Source
db.sources.insert_one({
    '_id': 'src-1',
    'name': 'DramaShorts Oficial',
    'baseUrl': 'https://dramashorts.io/es',
    'adapterType': 'dramashorts',
    'enabled': True,
    'crawlPolicy': {'intervalHours': 6, 'respectRobotsTxt': True},
    'lastSuccessfulRun': datetime.now(timezone.utc),
    'lastError': None
})

now = datetime.now(timezone.utc)
series_docs = []
episode_docs = []

for s in series_list:
    sid = s['id']
    series_docs.append({
        '_id': sid,
        'slug': s['slug'],
        'title': s['title'],
        'originalTitle': s.get('originalTitle') or s['title'],
        'synopsis': s['synopsis'],
        'genres': s['genres'],
        'language': 'es',
        'poster': s['posterUrl'],
        'sourceId': 'src-1',
        'sourceUrl': f"https://dramashorts.io/es/shorts/{s['slug']}",
        'publicationStatus': 'PUBLISHED',
        'rightsStatus': 'APPROVED',
        'seoTitle': f"{s['title']} | Ver Episodios Gratis Online",
        'seoDescription': s['synopsis'][:150],
        'viewCount': s['viewsCount'],
        'createdAt': now,
        'updatedAt': now,
        '_class': 'com.dramaapp.model.Series'
    })

    # Episodes for this series
    eps = episodes_dict.get(sid, [])
    for ep in eps:
        episode_docs.append({
            '_id': ep['id'],
            'seriesId': sid,
            'seasonNumber': 1,
            'episodeNumber': ep['episodeNumber'],
            'title': ep['title'],
            'synopsis': ep['synopsis'],
            'durationSeconds': ep['duration'],
            'videoAssetId': ep['videoUrl'],
            'subtitleTracks': [
                {'language': 'es', 'label': 'Español', 'fileUrl': '', 'isDefault': True}
            ],
            'thumbnail': ep['thumbnailUrl'],
            'publicationStatus': 'PUBLISHED',
            'rightsStatus': 'APPROVED',
            'createdAt': now,
            'updatedAt': now,
            '_class': 'com.dramaapp.model.Episode'
        })

db.series.insert_many(series_docs)
db.episodes.insert_many(episode_docs)

print(f"✅ ¡MongoDB actualizado con éxito! {len(series_docs)} series y {len(episode_docs)} episodios insertados en la base de datos.")
