package com.dramaapp.config;

import com.dramaapp.service.AuthService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
@RequiredArgsConstructor
public class StartupConfig {

    private final AuthService authService;

    @Bean
    public CommandLineRunner initDatabase() {
        return args -> {
            log.info("Initializing DramaApp system defaults...");
            authService.initDefaultAdmin();
            log.info("DramaApp backend initialized successfully.");
        };
    }
}
