import enum
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class UserStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class AssetType(enum.Enum):
    KEY = "KEY"
    GAS_CARD = "GAS_CARD"

class AssetStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"

class TransactionAction(enum.Enum):
    PICKUP = "PICKUP"
    RETURN = "RETURN"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    id_last4: Mapped[str] = mapped_column(String(4))
    status: Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus), default=UserStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    transactions: Mapped[list["TransactionLog"]] = relationship(back_populates="user")

class Asset(Base):
    __tablename__ = "assets"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[AssetType] = mapped_column(SQLEnum(AssetType))
    identifier: Mapped[str] = mapped_column(String(255))
    status: Mapped[AssetStatus] = mapped_column(SQLEnum(AssetStatus), default=AssetStatus.AVAILABLE)
    current_holder_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    transactions: Mapped[list["TransactionLog"]] = relationship(back_populates="asset")

class OTPPool(Base):
    __tablename__ = "otp_pool"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    password: Mapped[str] = mapped_column(String(255))
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    transactions: Mapped[list["TransactionLog"]] = relationship(back_populates="otp")

class TransactionLog(Base):
    __tablename__ = "transaction_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assets.id"))
    action: Mapped[TransactionAction] = mapped_column(SQLEnum(TransactionAction))
    otp_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("otp_pool.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates="transactions")
    asset: Mapped["Asset"] = relationship(back_populates="transactions")
    otp: Mapped["OTPPool"] = relationship(back_populates="transactions")
