import type { Series } from '../types'

export interface SitemapUrl {
  loc: string
  lastmod?: string
  changefreq?: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'never'
  priority?: number
}

export function generateSitemapXml(baseUrl: string, seriesList: Series[]): string {
  const staticUrls: SitemapUrl[] = [
    { loc: `${baseUrl}/`, changefreq: 'daily', priority: 1.0, lastmod: new Date().toISOString().split('T')[0] },
    { loc: `${baseUrl}/catalogo`, changefreq: 'daily', priority: 0.9, lastmod: new Date().toISOString().split('T')[0] },
    { loc: `${baseUrl}/buscar`, changefreq: 'weekly', priority: 0.7 },
    { loc: `${baseUrl}/privacidad`, changefreq: 'monthly', priority: 0.3 },
    { loc: `${baseUrl}/terminos`, changefreq: 'monthly', priority: 0.3 },
    { loc: `${baseUrl}/cookies`, changefreq: 'monthly', priority: 0.3 },
  ]

  const dynamicUrls: SitemapUrl[] = seriesList.map(s => ({
    loc: `${baseUrl}/serie/${s.slug || s.id}`,
    lastmod: s.updatedAt?.split('T')[0] || s.createdAt?.split('T')[0] || new Date().toISOString().split('T')[0],
    changefreq: s.status === 'completed' ? 'monthly' : 'daily',
    priority: s.featured ? 0.9 : 0.8,
  }))

  const allUrls = [...staticUrls, ...dynamicUrls]

  const xmlUrls = allUrls
    .map(
      u => `  <url>
    <loc>${u.loc}</loc>
    ${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}
    ${u.changefreq ? `<changefreq>${u.changefreq}</changefreq>` : ''}
    ${u.priority !== undefined ? `<priority>${u.priority.toFixed(1)}</priority>` : ''}
  </url>`
    )
    .join('\n')

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${xmlUrls}
</urlset>`
}
