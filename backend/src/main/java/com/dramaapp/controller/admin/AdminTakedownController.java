package com.dramaapp.controller.admin;

import com.dramaapp.dto.TakedownRequestDto;
import com.dramaapp.service.RightsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;
import java.util.Map;

@RestController
@RequestMapping("/api/admin/takedowns")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Takedowns", description = "DMCA, copyright compliance, and immediate content takedown operations")
public class AdminTakedownController {

    private final RightsService rightsService;

    @Operation(summary = "Execute a copyright takedown or block on a series and revoke rights")
    @PostMapping("/series/{seriesId}")
    public ResponseEntity<Map<String, String>> executeTakedown(
            @PathVariable String seriesId,
            @Valid @RequestBody TakedownRequestDto takedownRequest,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        rightsService.createTakedown(seriesId, takedownRequest, username);
        return ResponseEntity.ok(Map.of(
                "seriesId", seriesId,
                "status", "TAKEDOWN_EXECUTED",
                "reason", takedownRequest.getReason()
        ));
    }
}
