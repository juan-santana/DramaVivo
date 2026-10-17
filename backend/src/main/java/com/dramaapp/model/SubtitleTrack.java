package com.dramaapp.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SubtitleTrack {
    private String language;
    private String label;
    private String url;
    private boolean isDefault;
}
