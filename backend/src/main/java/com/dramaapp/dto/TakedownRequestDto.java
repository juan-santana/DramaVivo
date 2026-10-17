package com.dramaapp.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TakedownRequestDto {

    @NotBlank(message = "Takedown reason is required")
    private String reason;

    private String legalReference;

    @Builder.Default
    private boolean immediate = true;
}
