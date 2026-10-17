# 🚀 Guía de Despliegue Económico

Cómo desplegar DramaApp con el menor coste inicial posible.

---

## Opciones de Despliegue

### Opción 1: Ultra Económica (~$5/mes)

| Componente | Servicio | Coste |
|---|---|---|
| Frontend | **Cloudflare Pages** | Gratis |
| Backend | **Railway** (Hobby plan) | $5/mes |
| MongoDB | **MongoDB Atlas** (M0) | Gratis (512 MB) |
| Video | **Cloudflare R2** | Pago por uso |
| Dominio | Porkbun/Namecheap | ~$10/año |

### Opción 2: Pequeña Escala (~$15-25/mes)

| Componente | Servicio | Coste |
|---|---|---|
| Frontend | **Vercel** (Pro) | $20/mes |
| Backend | **Render** (Starter) | $7/mes |
| MongoDB | **MongoDB Atlas** (M2) | $9/mes |
| Video | **Bunny.net Storage + CDN** | ~$2-5/mes |
| Dominio | Cloudflare Registrar | ~$10/año |

### Opción 3: VPS Todo-en-Uno (~$10-20/mes)

| Componente | Servicio | Coste |
|---|---|---|
| Todo | **Hetzner Cloud** (CX22) | €4.35/mes |
| O todo | **DigitalOcean** (Basic) | $12/mes |
| O todo | **Contabo** (VPS S) | €5.99/mes |
| CDN | **Cloudflare** (Free) | Gratis |

---

## Despliegue en VPS con Docker (Recomendado)

### 1. Preparar el servidor

```bash
# Ubuntu 22.04 LTS
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install docker-compose-plugin
```

### 2. Clonar y configurar

```bash
git clone <tu-repo> /opt/dramaapp
cd /opt/dramaapp
cp .env.example .env
nano .env  # Configurar variables de producción
```

Variables críticas para producción:
```env
JWT_SECRET=<cadena-aleatoria-de-64+-caracteres>
ADMIN_DEFAULT_PASSWORD=<contraseña-segura>
MONGO_USERNAME=dramaapp
MONGO_PASSWORD=<contraseña-mongo-segura>
VITE_API_BASE_URL=https://api.tudramaapp.com/api
```

### 3. Construir y arrancar

```bash
docker compose up -d --build
```

### 4. Configurar Nginx como reverse proxy

```bash
sudo apt install nginx certbot python3-certbot-nginx

# Crear configuración de sitio
sudo nano /etc/nginx/sites-available/dramaapp
```

```nginx
server {
    server_name tudramaapp.com www.tudramaapp.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/dramaapp /etc/nginx/sites-enabled/
sudo certbot --nginx -d tudramaapp.com -d www.tudramaapp.com
sudo systemctl restart nginx
```

### 5. Backups automáticos

```bash
# Crontab para backup diario de MongoDB
0 3 * * * docker exec dramaapp-mongo mongodump --out /data/backup/$(date +\%Y\%m\%d) && \
  tar czf /backups/dramaapp-$(date +\%Y\%m\%d).tar.gz /data/backup/$(date +\%Y\%m\%d)
```

---

## Despliegue en Railway

### 1. Frontend en Cloudflare Pages

```bash
# En el directorio frontend/
npm run build
# Sube dist/ a Cloudflare Pages
# O conecta tu repo GitHub → auto deploy
```

Variables de entorno en Cloudflare Pages:
- `VITE_API_BASE_URL` = `https://tu-backend.railway.app/api`

### 2. Backend en Railway

1. Crea un nuevo proyecto en [railway.app](https://railway.app)
2. Añade un servicio **MongoDB**
3. Añade un servicio desde tu **GitHub repo** (directorio `backend/`)
4. Configura variables de entorno:
   - `SPRING_DATA_MONGODB_URI` = (auto-generada por Railway)
   - `JWT_SECRET` = tu-secreto
   - `CORS_ALLOWED_ORIGINS` = https://tudramaapp.com

### 3. Scraper como Worker

1. Añade otro servicio desde el repo (directorio `scraper/`)
2. Configura:
   - `SCRAPER_API_URL` = URL interna del backend
   - `SCRAPER_SCHEDULE_HOURS` = 6

---

## Monitorización

### Health Checks

- Backend: `GET /actuator/health`
- Frontend: Verificar que `index.html` responda 200

### Logs

```bash
# Ver logs en Docker
docker compose logs -f backend
docker compose logs -f scraper

# Logs del backend Spring Boot
docker compose logs -f backend | grep ERROR
```

### Alertas (gratuitas)

- **UptimeRobot** — Monitoriza URLs cada 5 min (gratis)
- **Better Stack** — Alertas por email/Slack (free tier)

---

## Optimización de Costes

1. **Comprime imágenes** — Usa WebP para posters (<100KB cada uno)
2. **CDN gratuito** — Cloudflare en plan gratuito para todo el sitio
3. **Caché agresivo** — 1 año para assets estáticos
4. **Lazy loading** — Carga imágenes solo cuando son visibles
5. **MongoDB Atlas Free** — Suficiente para empezar (<512MB)
6. **Videos en R2** — Sin costes de egress con Cloudflare
7. **Scraper conservador** — Ejecutar cada 12-24 horas, no cada hora

---

## Checklist de Producción

- [ ] Variables de entorno seguras (JWT_SECRET largo, contraseñas fuertes)
- [ ] HTTPS con certificado SSL (Let's Encrypt gratuito)
- [ ] CORS configurado solo para tu dominio
- [ ] Backups automáticos de MongoDB
- [ ] Monitorización con health checks
- [ ] Rate limiting activo
- [ ] Logs configurados y rotación
- [ ] Política de privacidad y cookies publicada
- [ ] robots.txt correcto
- [ ] Sitemap.xml generándose
- [ ] Error pages (404, 500) funcionando
- [ ] Compresión gzip/brotli activa
- [ ] Headers de seguridad configurados
