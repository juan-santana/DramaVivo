# 🎥 Guía: Integrar un Proveedor de Streaming

Esta guía explica cómo conectar DramaApp con un proveedor de almacenamiento y streaming de video externo (AWS S3, Cloudflare R2, Bunny.net, etc.).

---

## Arquitectura del Sistema de Video

DramaApp usa una **abstracción de proveedor de video** (`VideoProvider`) que separa la lógica de negocio del almacenamiento real:

```
Admin sube video → VideoService → VideoProvider (interfaz)
                                       ↓
                              ┌─────────────────┐
                              │ LocalVideoProvider│  ← Desarrollo
                              │ S3VideoProvider   │  ← Producción
                              │ R2VideoProvider   │  ← Alternativa
                              │ BunnyProvider     │  ← CDN económico
                              └─────────────────┘
```

---

## Paso 1: Implementar la Interfaz VideoProvider

Crea una nueva clase en `backend/src/main/java/com/dramaapp/service/`:

```java
package com.dramaapp.service;

import org.springframework.stereotype.Service;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;

@Service
@ConditionalOnProperty(name = "video.provider", havingValue = "s3")
public class S3VideoProvider implements VideoProvider {

    // Inyectar credenciales desde application.yml
    @Value("${aws.s3.bucket}")
    private String bucket;

    @Value("${aws.s3.region}")
    private String region;

    @Value("${cdn.base-url}")
    private String cdnBaseUrl;

    @Override
    public String generatePlaybackUrl(String assetId) {
        // Generar URL firmada temporal (presigned URL)
        // Expira en 4 horas para evitar redistribución
        return generatePresignedUrl(bucket, assetId, Duration.ofHours(4));
    }

    @Override
    public UploadSessionDto createUploadSession(String fileName, String contentType) {
        // Generar presigned POST/PUT para subida directa
        String key = "videos/" + UUID.randomUUID() + "/" + fileName;
        String uploadUrl = generatePresignedUploadUrl(bucket, key);

        return new UploadSessionDto(
            UUID.randomUUID().toString(),
            uploadUrl,
            key,
            Instant.now().plus(Duration.ofHours(1))
        );
    }

    @Override
    public String generateThumbnailUrl(String assetId) {
        return cdnBaseUrl + "/thumbnails/" + assetId + ".jpg";
    }
}
```

---

## Paso 2: Agregar Dependencias

Para AWS S3, añade al `pom.xml`:

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
    <version>2.25.0</version>
</dependency>
```

Para Cloudflare R2 (compatible con S3):
```xml
<!-- Misma SDK de AWS S3, pero con endpoint personalizado -->
```

Para Bunny.net:
```xml
<!-- HTTP client estándar, la API es REST -->
```

---

## Paso 3: Configurar Variables de Entorno

Añade al `.env`:

```env
VIDEO_PROVIDER=s3

# AWS S3 / Cloudflare R2
AWS_ACCESS_KEY_ID=tu-access-key
AWS_SECRET_ACCESS_KEY=tu-secret-key
AWS_S3_BUCKET=dramaapp-videos
AWS_S3_REGION=us-east-1
# Para R2: AWS_S3_ENDPOINT=https://xxxx.r2.cloudflarestorage.com

# CDN (opcional pero recomendado)
CDN_BASE_URL=https://cdn.tudramaapp.com
```

Y en `application.yml`:

```yaml
video:
  provider: ${VIDEO_PROVIDER:local}

aws:
  s3:
    bucket: ${AWS_S3_BUCKET:}
    region: ${AWS_S3_REGION:us-east-1}
    endpoint: ${AWS_S3_ENDPOINT:}

cdn:
  base-url: ${CDN_BASE_URL:http://localhost:8080/api/media}
```

---

## Paso 4: Flujo de Subida de Videos

```
1. Admin crea sesión → POST /api/admin/videos/upload-session
   → Backend genera presigned URL → devuelve uploadUrl + uploadId

2. Frontend sube directo al storage → PUT {uploadUrl}
   → El video llega a S3/R2/Bunny sin pasar por el backend

3. Frontend confirma → PATCH /api/admin/videos/{id}/status
   → Backend actualiza estado a PROCESSING

4. (Opcional) Webhook de transcodificación → actualiza a READY

5. Público reproduce → GET /api/episodes/{id}/playback
   → Backend genera URL temporal firmada → devuelve al reproductor
```

---

## Proveedores Recomendados (Económicos)

| Proveedor | Storage | Transfer | Ventajas |
|---|---|---|---|
| **Cloudflare R2** | $0.015/GB | Gratis (egress) | Sin costes de transferencia |
| **Bunny.net** | $0.005/GB | $0.01/GB | Muy económico, CDN incluido |
| **AWS S3** | $0.023/GB | $0.09/GB | Estándar, muchas herramientas |
| **Backblaze B2** | $0.005/GB | Gratis con CF | Muy barato + Cloudflare gratis |

### Recomendación para DramaApp:
**Cloudflare R2 + Cloudflare Stream** — Sin costes de transferencia, CDN global incluido, transcodificación automática.

---

## Paso 5: Transcodificación (Opcional)

Para servir video adaptativo (HLS/DASH):

1. **Cloudflare Stream**: Transcodifica automáticamente al subir.
2. **AWS MediaConvert**: Servicio bajo demanda.
3. **FFmpeg en servidor**: Más manual, pero sin coste de servicio.

Ejemplo de configuración para formato vertical:
```bash
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920" \
  -c:v h264 -crf 23 -preset medium \
  -c:a aac -b:a 128k \
  output_vertical.mp4
```

---

## Notas de Seguridad

- **Nunca** guardes URLs de reproducción permanentes en la base de datos
- Genera URLs firmadas temporales (máx. 4 horas)
- Valida el tipo de contenido antes de aceptar subidas
- Limita el tamaño de archivo (configurable)
- Usa HTTPS siempre para URLs de reproducción
- Configura CORS en el bucket para permitir solo tu dominio
