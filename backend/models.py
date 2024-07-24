from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)

class AcquisitionCampaign(Base):
    __tablename__ = "acquisition_campaigns"

    name: Mapped[str] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)
    scenario: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.username"))

    points: Mapped[list["AcquisitionPoint"]] = relationship(back_populates="campaign",
                                                            cascade="all, delete-orphan")

class AcquisitionPoint(Base):
    __tablename__ = "acquisition_points"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    x: Mapped[int] = mapped_column(nullable=False)
    y: Mapped[int] = mapped_column(nullable=False)
    preamble_time: Mapped[int] = mapped_column(nullable=True)
    acquisition_time: Mapped[int] = mapped_column(nullable=False)
    campaign_name: Mapped[str] = mapped_column(ForeignKey("acquisition_campaigns.name",
                                                          ondelete='CASCADE'))

    campaign: Mapped["AcquisitionCampaign"] = relationship(back_populates="points")
    samples: Mapped[list["PointSample"]] = relationship(back_populates="point")

class PointSample(Base):
    __tablename__ = "point_samples"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    beacon: Mapped[int] = mapped_column(nullable=False)
    rssi: Mapped[int] = mapped_column(nullable=False)
    tx_time_ns: Mapped[str] = mapped_column(nullable=True)
    rx_time_ns: Mapped[str] = mapped_column(nullable=False)
    point_id: Mapped[int] = mapped_column(ForeignKey("acquisition_points.id",
                                                     ondelete="CASCADE"))

    point: Mapped["AcquisitionPoint"] = relationship(back_populates="samples")