"""Sample domain entity — represents a biosensor / lab sample collected from
a (synthetic) patient and tracked through its lifecycle."""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


class SampleType(str, enum.Enum):
    URINALYSIS = "urinalysis"
    HBA1C = "hba1c"
    BLOOD_CHEMISTRY = "blood_chemistry"
    METABOLIC_PANEL = "metabolic_panel"
    HIV_SCREENING = "hiv_screening"


class SampleStatus(str, enum.Enum):
    REGISTERED = "registered"
    COLLECTED = "collected"
    IN_TRANSIT = "in_transit"
    RECEIVED = "received"
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    REJECTED = "rejected"


@dataclass
class Sample:
    patient_id: UUID
    sample_type: SampleType
    barcode: str
    status: SampleStatus = SampleStatus.REGISTERED
    collected_by: UUID | None = None
    device_id: str | None = None
    raw_signal_ref: str | None = None  # object storage key for raw biosensor signal
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
