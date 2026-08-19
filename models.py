from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import class_mapper
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, Float, Text, ForeignKey, JSON, Numeric, Date, \
    TIMESTAMP, UUID, LargeBinary, text as text_sql, Interval
from sqlalchemy.types import Enum
from sqlalchemy.ext.declarative import declarative_base


@as_declarative()
class Base:
    id: int
    __name__: str

    # Auto-generate table name if not provided
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # Generic to_dict() method
    def to_dict(self):
        """
        Converts the SQLAlchemy model instance to a dictionary, ensuring UUID fields are converted to strings.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            value = getattr(self, column.key)
                # Handle UUID fields
            if isinstance(value, uuid.UUID):
                value = str(value)
            # Handle datetime fields
            elif isinstance(value, datetime):
                value = value.isoformat()  # Convert to ISO 8601 string
            # Handle Decimal fields
            elif isinstance(value, Decimal):
                value = float(value)

            result[column.key] = value
        return result




class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    lot_id = Column(Integer)
    vehicle_id = Column(Integer, nullable=True)
    start_time_dt = Column(DateTime, server_default=text_sql("now()"))
    end_time_dt = Column(DateTime, server_default=text_sql("now()"))
    total_cost = Column(Float, nullable=True)
    confirmation_code = Column(String, nullable=True)
    status = Column(String, nullable=True)
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))
    updated_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    type = Column(String, nullable=True)
    message = Column(String, nullable=True)
    is_read = Column(Integer, nullable=True)
    sent_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


class ParkingLots(Base):
    __tablename__ = "parking_lots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer)
    name = Column(String)
    address = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    hourly_rate = Column(Float, nullable=True)
    daily_rate = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Integer, nullable=True)
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))
    updated_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer)
    amount = Column(Float)
    payment_method = Column(String, nullable=True)
    payment_status = Column(String, nullable=True)
    transaction_id = Column(String, nullable=True)
    processed_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    lot_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(String, nullable=True)
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


class UserProfiles(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    role = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))
    updated_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password = Column(String)
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


class Vehicles(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    license_plate = Column(String)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    color = Column(String, nullable=True)
    created_at_dt = Column(DateTime, nullable=True, server_default=text_sql("now()"))


