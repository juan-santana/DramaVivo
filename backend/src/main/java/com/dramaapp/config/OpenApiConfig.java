package com.dramaapp.config;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    private static final String SECURITY_SCHEME_NAME = "bearerAuth";

    @Bean
    public OpenAPI dramaAppOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("DramaApp Backend API")
                        .description("RESTful Backend for DramaApp - Short Drama Streaming Platform with Rights Management, Video Ingestion, and Crawler Adapters.")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("DramaApp Engineering Team")
                                .email("engineering@dramaapp.tv"))
                        .license(new License()
                                .name("Proprietary")
                                .url("https://dramaapp.tv/terms")))
                .addSecurityItem(new SecurityRequirement().addList(SECURITY_SCHEME_NAME))
                .components(new Components()
                        .addSecuritySchemes(SECURITY_SCHEME_NAME,
                                new SecurityScheme()
                                        .name(SECURITY_SCHEME_NAME)
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")
                                        .description("Enter JWT Bearer token obtained from /api/admin/auth/login")));
    }
}
