"""Import job tracking model."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class ImportJobResult(BaseModel):
    """Execution status and metric summary for an import/scrape job."""

    model_config = ConfigDict(extra="ignore")

    source_id: str = Field(description="Identifier of the scraped source")
    started_at: datetime = Field(description="Timestamp when the scraping job started")
    completed_at: datetime | None = Field(default=None, description="Timestamp when the job completed")
    status: Literal["RUNNING", "COMPLETED", "FAILED", "PARTIAL"] = Field(
        default="RUNNING",
        description="Overall execution status of the import job",
    )
    records_discovered: int = Field(default=0, ge=0, description="Total series and episodes discovered")
    records_imported: int = Field(default=0, ge=0, description="Total records successfully exported/imported")
    records_skipped: int = Field(default=0, ge=0, description="Total duplicate or invalid records skipped")
    error_summary: str | None = Field(default=None, description="Error message or stack summary if failed")
