from enum import Enum
from pydantic import BaseModel

class Scenario(str, Enum):
    ROOM = "ROOM"
    FLOOR = "FLOOR"

class PointSampleIn(BaseModel):
    point_id: int | None = None
    beacon: str
    rssi: int
    tx_time_ns: str | None = None
    rx_time_ns: str
    class Config:
        from_attributes=True

class PointSampleOut(PointSampleIn):
    id: int

class AcquisitionPointIn(BaseModel):
    name: str
    x: int
    y: int
    preamble_time: int | None = None
    acquisition_time: int
    campaign_name: str
    class Config:
        from_attributes=True

class AcquisitionPointOut(AcquisitionPointIn):
    id: int
    samples: list[PointSampleOut]

class AcquisitionCampaignIn(BaseModel):
    name: str
    description: str | None = None
    scenario: Scenario
    class Config:
        from_attributes=True

class AcquisitionCampaignOut(AcquisitionCampaignIn):
    points: list[AcquisitionPointOut]
