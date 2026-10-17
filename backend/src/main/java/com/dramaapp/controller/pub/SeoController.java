package com.dramaapp.controller.pub;

import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.SeriesDto;
import com.dramaapp.service.SeriesService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
@Tag(name = "SEO & Crawlers", description = "Search engine discovery endpoints")
public class SeoController {

    private final SeriesService seriesService;

    @Operation(summary = "Generate dynamic sitemap.xml for search engines")
    @GetMapping(value = "/sitemap.xml", produces = MediaType.APPLICATION_XML_VALUE)
    public ResponseEntity<String> getSitemap() {
        PagedResponseDto<SeriesDto> published = seriesService.listPublished(0, 500, null, null, "createdAt", "desc");

        StringBuilder xml = new StringBuilder();
        xml.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        xml.append("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n");

        xml.append("  <url>\n");
        xml.append("    <loc>https://dramaapp.tv/</loc>\n");
        xml.append("    <changefreq>daily</changefreq>\n");
        xml.append("    <priority>1.0</priority>\n");
        xml.append("  </url>\n");

        for (SeriesDto s : published.getContent()) {
            xml.append("  <url>\n");
            xml.append("    <loc>https://dramaapp.tv/series/").append(s.getSlug()).append("</loc>\n");
            xml.append("    <lastmod>").append(s.getUpdatedAt() != null ? s.getUpdatedAt() : s.getCreatedAt()).append("</lastmod>\n");
            xml.append("    <changefreq>weekly</changefreq>\n");
            xml.append("    <priority>0.8</priority>\n");
            xml.append("  </url>\n");
        }

        xml.append("</urlset>");
        return ResponseEntity.ok(xml.toString());
    }

    @Operation(summary = "Robots.txt directive for search engine crawlers")
    @GetMapping(value = "/robots.txt", produces = MediaType.TEXT_PLAIN_VALUE)
    public ResponseEntity<String> getRobotsTxt() {
        String robots = """
                User-agent: *
                Allow: /
                Disallow: /api/admin/
                Disallow: /actuator/
                
                Sitemap: https://dramaapp.tv/sitemap.xml
                """;
        return ResponseEntity.ok(robots);
    }
}
