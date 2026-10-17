import json
import re

mock_data_path = r"E:\DramaApp\frontend\src\services\mockData.ts"
with open(mock_data_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. New Dailymotion series
dm_series = [
    {
        "id": "dm-1",
        "title": "Vagabundo de día, francotirador de noche",
        "originalTitle": "Vagabundo de día, francotirador de noche - Serie Completa Doblada",
        "slug": "vagabundo-de-dia-francotirador-de-noche",
        "synopsis": "Vagabundo de día, francotirador de noche (Serie Completa - Doblado al Español). El legendario francotirador que se oculta bajo la apariencia de un indigente para proteger a su amada y vengarse de la élite criminal. Incluye los 63 episodios compilados en formato película continua de 1h 45m.",
        "posterUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
        "bannerUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
        "thumbnailUrl": "https://s2.dmcdn.net/v/cwRE21gmaydLgcsEq",
        "verticalPosterUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
        "releaseYear": 2026,
        "genres": ["Series Completas (1h+)", "Acción romántica", "Venganza", "Doblado ESP", "Suspenso"],
        "language": "Español (Doblado)",
        "subtitles": ["Español"],
        "totalEpisodes": 1,
        "availableEpisodes": 1,
        "durationPerEpisode": 6359,
        "status": "completed",
        "featured": True,
        "trending": True,
        "rating": 4.9,
        "viewsCount": 842100,
        "likesCount": 41200,
        "rightsStatus": "approved",
        "sourceName": "Dailymotion Oficial",
        "createdAt": "2026-03-01T12:00:00Z"
    },
    {
        "id": "dm-2",
        "title": "El conserje mágico",
        "originalTitle": "El conserje mágico - Serie Completa Doblada",
        "slug": "el-conserje-magico",
        "synopsis": "El conserje mágico (Serie Completa en Español Latino). Un hombre bajo la humilde apariencia de empleado de limpieza oculta la verdadera llave maestra de un imperio corporativo y poderes que pondrán de rodillas a quienes intentaron humillarlo.",
        "posterUrl": "https://s1.dmcdn.net/v/dtZpQ1glYKFNhJgi-/x720",
        "bannerUrl": "https://s1.dmcdn.net/v/dtZpQ1glYKFNhJgi-/x720",
        "thumbnailUrl": "https://s1.dmcdn.net/v/dtZpQ1glYKFNhJgi-/x720",
        "verticalPosterUrl": "https://s1.dmcdn.net/v/dtZpQ1glYKFNhJgi-/x720",
        "releaseYear": 2026,
        "genres": ["Series Completas (1h+)", "Venganza", "Multimillonarios", "Fantasía", "Doblado ESP"],
        "language": "Español (Doblado)",
        "subtitles": ["Español"],
        "totalEpisodes": 1,
        "availableEpisodes": 1,
        "durationPerEpisode": 6519,
        "status": "completed",
        "featured": True,
        "trending": True,
        "rating": 4.8,
        "viewsCount": 512300,
        "likesCount": 28400,
        "rightsStatus": "approved",
        "sourceName": "Dailymotion Oficial",
        "createdAt": "2026-03-01T12:00:00Z"
    },
    {
        "id": "dm-3",
        "title": "Incomparable: El heredero oculto",
        "originalTitle": "Incomparable - Serie Completa",
        "slug": "incomparable-el-heredero-oculto",
        "synopsis": "Incomparable (Serie Completa en Español). Tras años de desprecio por parte de la familia de su prometida, se descubre que él es el único heredero del consorcio más poderoso de la nación.",
        "posterUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
        "bannerUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
        "thumbnailUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
        "verticalPosterUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
        "releaseYear": 2026,
        "genres": ["Series Completas (1h+)", "Multimillonarios", "Venganza", "Doblado ESP", "Romance"],
        "language": "Español (Doblado)",
        "subtitles": ["Español"],
        "totalEpisodes": 1,
        "availableEpisodes": 1,
        "durationPerEpisode": 3905,
        "status": "completed",
        "featured": False,
        "trending": True,
        "rating": 4.7,
        "viewsCount": 395000,
        "likesCount": 19200,
        "rightsStatus": "approved",
        "sourceName": "Dailymotion Oficial",
        "createdAt": "2026-03-01T12:00:00Z"
    }
]

dm_episodes = {
    "dm-1": [
        {
            "id": "ep-dm1-1",
            "seriesId": "dm-1",
            "seriesTitle": "Vagabundo de día, francotirador de noche",
            "episodeNumber": 1,
            "title": "Película Completa (1h 45m - Doblado ESP)",
            "synopsis": "Todos los 63 episodios compilados en una sola reproducción continua en alta definición con audio doblado al español latino.",
            "duration": 6359,
            "thumbnailUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
            "videoUrl": "https://www.dailymotion.com/embed/video/xasoubm",
            "subtitles": [
                {
                    "lang": "es",
                    "label": "Español",
                    "src": "",
                    "isDefault": True
                }
            ],
            "isFree": True,
            "viewsCount": 842100,
            "likesCount": 41200,
            "createdAt": "2026-03-01T12:00:00Z"
        }
    ],
    "dm-2": [
        {
            "id": "ep-dm2-1",
            "seriesId": "dm-2",
            "seriesTitle": "El conserje mágico",
            "episodeNumber": 1,
            "title": "Película Completa (1h 48m - Doblado ESP)",
            "synopsis": "Serie completa doblada al español latino con revelación de secretos y ascenso corporativo.",
            "duration": 6519,
            "thumbnailUrl": "https://s1.dmcdn.net/v/dtZpQ1glYKFNhJgi-/x720",
            "videoUrl": "https://www.dailymotion.com/embed/video/xb8khla",
            "subtitles": [
                {
                    "lang": "es",
                    "label": "Español",
                    "src": "",
                    "isDefault": True
                }
            ],
            "isFree": True,
            "viewsCount": 512300,
            "likesCount": 28400,
            "createdAt": "2026-03-01T12:00:00Z"
        }
    ],
    "dm-3": [
        {
            "id": "ep-dm3-1",
            "seriesId": "dm-3",
            "seriesTitle": "Incomparable: El heredero oculto",
            "episodeNumber": 1,
            "title": "Película Completa (1h 05m - Doblado ESP)",
            "synopsis": "Drama completo continuo de 65 minutos con audio en español.",
            "duration": 3905,
            "thumbnailUrl": "https://s1.dmcdn.net/v/cwRE21gmaydwQRg8-/x720",
            "videoUrl": "https://www.dailymotion.com/embed/video/xbjokdu",
            "subtitles": [
                {
                    "lang": "es",
                    "label": "Español",
                    "src": "",
                    "isDefault": True
                }
            ],
            "isFree": True,
            "viewsCount": 395000,
            "likesCount": 19200,
            "createdAt": "2026-03-01T12:00:00Z"
        }
    ]
}

# Add Dailymotion series before the closing bracket of MOCK_SERIES
series_marker = "export const MOCK_EPISODES: Record<string, Episode[]> = {"
marker_idx = content.find(series_marker)

# Find the `]` right before `series_marker`
bracket_idx = content.rfind("]", 0, marker_idx)

# Format dm_series as JSON string without outer brackets
dm_series_json = ",\n" + ",\n".join(json.dumps(s, ensure_ascii=False, indent=2) for s in dm_series)

# Check if already added
if "dm-1" not in content:
    content = content[:bracket_idx] + dm_series_json + "\n" + content[bracket_idx:]
    print("Added Dailymotion series to MOCK_SERIES!")
else:
    print("Dailymotion series already present in MOCK_SERIES.")

# Now add episodes before the closing `}` of MOCK_EPISODES
sources_marker = "export const MOCK_SOURCES: Source[] = ["
sources_idx = content.find(sources_marker)
curly_idx = content.rfind("}", 0, sources_idx)

dm_episodes_json = ""
for sid, eps in dm_episodes.items():
    if f'"{sid}":' not in content:
        eps_str = json.dumps(eps, ensure_ascii=False, indent=4)
        dm_episodes_json += f',\n  "{sid}": {eps_str}'

if dm_episodes_json:
    content = content[:curly_idx] + dm_episodes_json + "\n" + content[curly_idx:]
    print("Added Dailymotion episodes to MOCK_EPISODES!")
else:
    print("Dailymotion episodes already present.")

# Save modified content
with open(mock_data_path, "w", encoding="utf-8") as f:
    f.write(content)

print("mockData.ts successfully updated!")
