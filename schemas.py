from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple,Union

import re

class Bookings(BaseModel):
    user_id: int
    lot_id: int
    vehicle_id: Optional[Union[int, float]]=None
    start_time_dt: Any
    end_time_dt: Any
    total_cost: Optional[float]=None
    confirmation_code: Optional[str]=None
    status: Optional[str]=None
    created_at_dt: Optional[Any]=None
    updated_at_dt: Optional[Any]=None


class ReadBookings(BaseModel):
    user_id: int
    lot_id: int
    vehicle_id: Optional[Union[int, float]]=None
    start_time_dt: Any
    end_time_dt: Any
    total_cost: Optional[float]=None
    confirmation_code: Optional[str]=None
    status: Optional[str]=None
    created_at_dt: Optional[Any]=None
    updated_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class Notifications(BaseModel):
    user_id: int
    type: Optional[str]=None
    message: Optional[str]=None
    is_read: Optional[Union[int, float]]=None
    sent_at_dt: Optional[Any]=None
    created_at_dt: Optional[Any]=None


class ReadNotifications(BaseModel):
    user_id: int
    type: Optional[str]=None
    message: Optional[str]=None
    is_read: Optional[Union[int, float]]=None
    sent_at_dt: Optional[Any]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class ParkingLots(BaseModel):
    owner_id: int
    name: str
    address: str
    latitude: Optional[float]=None
    longitude: Optional[float]=None
    hourly_rate: Optional[float]=None
    daily_rate: Optional[float]=None
    description: Optional[str]=None
    is_active: Optional[Union[int, float]]=None
    created_at_dt: Optional[Any]=None
    updated_at_dt: Optional[Any]=None


class ReadParkingLots(BaseModel):
    owner_id: int
    name: str
    address: str
    latitude: Optional[float]=None
    longitude: Optional[float]=None
    hourly_rate: Optional[float]=None
    daily_rate: Optional[float]=None
    description: Optional[str]=None
    is_active: Optional[Union[int, float]]=None
    created_at_dt: Optional[Any]=None
    updated_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class Payments(BaseModel):
    booking_id: int
    amount: float
    payment_method: Optional[str]=None
    payment_status: Optional[str]=None
    transaction_id: Optional[str]=None
    processed_at_dt: Optional[Any]=None
    created_at_dt: Optional[Any]=None


class ReadPayments(BaseModel):
    booking_id: int
    amount: float
    payment_method: Optional[str]=None
    payment_status: Optional[str]=None
    transaction_id: Optional[str]=None
    processed_at_dt: Optional[Any]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class Reviews(BaseModel):
    user_id: int
    lot_id: int
    rating: int
    comment: Optional[str]=None
    created_at_dt: Optional[Any]=None


class ReadReviews(BaseModel):
    user_id: int
    lot_id: int
    rating: int
    comment: Optional[str]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class UserProfiles(BaseModel):
    user_id: int
    role: Optional[str]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    phone_number: Optional[str]=None
    created_at_dt: Optional[Any]=None
    updated_at_dt: Optional[Any]=None


class ReadUserProfiles(BaseModel):
    user_id: int
    role: Optional[str]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    phone_number: Optional[str]=None
    created_at_dt: Optional[Any]=None
    updated_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class Users(BaseModel):
    email: str
    password: str
    created_at_dt: Optional[Any]=None


class ReadUsers(BaseModel):
    email: str
    password: str
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True


class Vehicles(BaseModel):
    user_id: int
    license_plate: str
    make: Optional[str]=None
    model: Optional[str]=None
    color: Optional[str]=None
    created_at_dt: Optional[Any]=None


class ReadVehicles(BaseModel):
    user_id: int
    license_plate: str
    make: Optional[str]=None
    model: Optional[str]=None
    color: Optional[str]=None
    created_at_dt: Optional[Any]=None
    class Config:
        from_attributes = True




class PostPayments(BaseModel):
    booking_id: int = Field(...)
    amount: Any = Field(...)
    payment_method: Optional[str]=None
    payment_status: Optional[str]=None
    transaction_id: Optional[str]=None
    processed_at_dt: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutPaymentsId(BaseModel):
    id: str = Field(..., max_length=100)
    booking_id: int = Field(...)
    amount: Any = Field(...)
    payment_method: Optional[str]=None
    payment_status: Optional[str]=None
    transaction_id: Optional[str]=None
    processed_at_dt: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostParkingLots(BaseModel):
    owner_id: int = Field(...)
    name: str = Field(..., max_length=100)
    address: str = Field(..., max_length=100)
    latitude: Optional[Any]=None
    longitude: Optional[Any]=None
    hourly_rate: Optional[Any]=None
    daily_rate: Optional[Any]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    created_at_dt: Optional[str]=None
    updated_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutParkingLotsId(BaseModel):
    id: str = Field(..., max_length=100)
    owner_id: Union[int, float] = Field(...)
    name: str = Field(..., max_length=100)
    address: str = Field(..., max_length=100)
    latitude: Optional[Any]=None
    longitude: Optional[Any]=None
    hourly_rate: Optional[Any]=None
    daily_rate: Optional[Any]=None
    description: Optional[str]=None
    is_active: Optional[Union[int, float]]=None
    created_at_dt: Optional[str]=None
    updated_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostReviews(BaseModel):
    user_id: Union[int, float] = Field(...)
    lot_id: Union[int, float] = Field(...)
    rating: Union[int, float] = Field(...)
    comment: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutReviewsId(BaseModel):
    id: str = Field(..., max_length=100)
    user_id: Union[int, float] = Field(...)
    lot_id: Union[int, float] = Field(...)
    rating: Union[int, float] = Field(...)
    comment: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostUserProfiles(BaseModel):
    user_id: Union[int, float] = Field(...)
    role: Optional[str]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    phone_number: Optional[str]=None
    created_at_dt: Optional[str]=None
    updated_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutUserProfilesId(BaseModel):
    id: str = Field(..., max_length=100)
    user_id: Union[int, float] = Field(...)
    role: Optional[str]=None
    first_name: Optional[str]=None
    last_name: Optional[str]=None
    phone_number: Optional[str]=None
    created_at_dt: Optional[str]=None
    updated_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostBookings(BaseModel):
    user_id: Union[int, float] = Field(...)
    lot_id: Union[int, float] = Field(...)
    vehicle_id: Optional[Union[int, float]]=None
    start_time_dt: str = Field(..., max_length=100)
    end_time_dt: str = Field(..., max_length=100)
    total_cost: Optional[Any]=None
    confirmation_code: Optional[str]=None
    status: Optional[str]=None
    created_at_dt: Optional[str]=None
    updated_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutBookingsId(BaseModel):
    id: str = Field(..., max_length=100)
    user_id: Union[int, float] = Field(...)
    lot_id: Union[int, float] = Field(...)
    vehicle_id: Optional[Union[int, float]]=None
    start_time_dt: str = Field(..., max_length=100)
    end_time_dt: str = Field(..., max_length=100)
    total_cost: Optional[Any]=None
    confirmation_code: Optional[str]=None
    status: Optional[str]=None
    created_at_dt: Optional[str]=None
    updated_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostNotifications(BaseModel):
    user_id: Union[int, float] = Field(...)
    type: Optional[str]=None
    message: Optional[str]=None
    is_read: Optional[Union[int, float]]=None
    sent_at_dt: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostVehicles(BaseModel):
    user_id: Union[int, float] = Field(...)
    license_plate: str = Field(..., max_length=20)
    make: Optional[str]=None
    model: Optional[str]=None
    color: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutNotificationsId(BaseModel):
    id: str = Field(..., max_length=100)
    user_id: Union[int, float] = Field(...)
    type: Optional[str]=None
    message: Optional[str]=None
    is_read: Optional[Union[int, float]]=None
    sent_at_dt: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostPlatformAuthPackageMaysonAuthUserLogin(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)

    class Config:
        from_attributes = True



class PostUsers(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=255)
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutUsersId(BaseModel):
    id: str = Field(..., max_length=100)
    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=255)
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PutVehiclesId(BaseModel):
    id: str = Field(..., max_length=100)
    user_id: Union[int, float] = Field(...)
    license_plate: str = Field(..., max_length=20)
    make: Optional[str]=None
    model: Optional[str]=None
    color: Optional[str]=None
    created_at_dt: Optional[str]=None

    class Config:
        from_attributes = True



class PostPlatformAuthPackageMaysonAuthUserRegister(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)

    class Config:
        from_attributes = True



# Query Parameter Validation Schemas

class GetPaymentsIdQueryParams(BaseModel):
    """Query parameter validation for get_payments_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeletePaymentsIdQueryParams(BaseModel):
    """Query parameter validation for delete_payments_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetParkingLotsIdQueryParams(BaseModel):
    """Query parameter validation for get_parking_lots_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteParkingLotsIdQueryParams(BaseModel):
    """Query parameter validation for delete_parking_lots_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetReviewsIdQueryParams(BaseModel):
    """Query parameter validation for get_reviews_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetUserProfilesIdQueryParams(BaseModel):
    """Query parameter validation for get_user_profiles_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteUserProfilesIdQueryParams(BaseModel):
    """Query parameter validation for delete_user_profiles_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteReviewsIdQueryParams(BaseModel):
    """Query parameter validation for delete_reviews_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetBookingsIdQueryParams(BaseModel):
    """Query parameter validation for get_bookings_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteBookingsIdQueryParams(BaseModel):
    """Query parameter validation for delete_bookings_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetNotificationsIdQueryParams(BaseModel):
    """Query parameter validation for get_notifications_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetVehiclesIdQueryParams(BaseModel):
    """Query parameter validation for get_vehicles_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class GetUsersIdQueryParams(BaseModel):
    """Query parameter validation for get_users_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteNotificationsIdQueryParams(BaseModel):
    """Query parameter validation for delete_notifications_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteUsersIdQueryParams(BaseModel):
    """Query parameter validation for delete_users_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True


class DeleteVehiclesIdQueryParams(BaseModel):
    """Query parameter validation for delete_vehicles_id"""
    id: int = Field(..., ge=1, description="Id")

    class Config:
        populate_by_name = True
