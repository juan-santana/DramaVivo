package com.dramaapp.controller.admin;

import com.dramaapp.dto.PagedResponseDto;
import com.dramaapp.dto.RightsApprovalDto;
import com.dramaapp.dto.RightsRecordDto;
import com.dramaapp.service.RightsService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;
import java.util.Map;

@RestController
@RequestMapping("/api/admin/rights")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Admin Rights", description = "Rights management, license verification, and copyright review")
public class AdminRightsController {

    private final RightsService rightsService;

    @Operation(summary = "List pending rights records requiring human legal review")
    @GetMapping("/pending")
    public ResponseEntity<PagedResponseDto<RightsRecordDto>> getPendingReviews(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        return ResponseEntity.ok(rightsService.getPendingReviews(page, size));
    }

    @Operation(summary = "Approve or update licensing terms for a rights record")
    @PostMapping("/{id}/approve")
    public ResponseEntity<RightsRecordDto> approve(
            @PathVariable String id,
            @Valid @RequestBody RightsApprovalDto approvalDto,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        return ResponseEntity.ok(rightsService.approve(id, approvalDto, username));
    }

    @Operation(summary = "Reject licensing for a rights record with explanation reason")
    @PostMapping("/{id}/reject")
    public ResponseEntity<RightsRecordDto> reject(
            @PathVariable String id,
            @RequestBody(required = false) Map<String, String> body,
            Principal principal
    ) {
        String username = principal != null ? principal.getName() : "ADMIN";
        String reason = body != null && body.containsKey("reason") ? body.get("reason") : "Rejected by admin";
        return ResponseEntity.ok(rightsService.reject(id, reason, username));
    }
}
