from sqlalchemy.orm import Session, aliased
from database import SessionLocal
from sqlalchemy import and_, or_
from typing import *
from loguru import logger
from fastapi import Request, UploadFile, HTTPException, status
from fastapi.responses import RedirectResponse, StreamingResponse
import models, schemas
import boto3
import jwt
from datetime import datetime, timezone, date, time
import requests
import math
import os
import json
import random
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    RunConfig,
    ModelSettings,
    InputGuardrail,
    OutputGuardrail,
)
import agent_session_store as store


load_dotenv()


def convert_to_datetime(date_string):
    if isinstance(date_string, datetime):
        return date_string
    if date_string is None:
        return datetime.now()
    if not date_string.strip():
        return datetime.now()
    if "T" in date_string:
        try:
            return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        except ValueError:
            date_part = date_string.split("T")[0]
            try:
                return datetime.strptime(date_part, "%Y-%m-%d")
            except ValueError:
                return datetime.now()
    else:
        # Try to determine format based on first segment
        parts = date_string.split("-")
        if len(parts[0]) == 4:
            # Likely YYYY-MM-DD format
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                return datetime.now()

        # Try DD-MM-YYYY format
        try:
            return datetime.strptime(date_string, "%d-%m-%Y")
        except ValueError:
            return datetime.now()

        # Fallback: try YYYY-MM-DD if not already tried
        if len(parts[0]) != 4:
            try:
                return datetime.strptime(date_string, "%Y-%m-%d")
            except ValueError:
                return datetime.now()

        return datetime.now()


class SessionStoreAdapter:

    def load_session(self, session_id: str) -> dict:
        return store.load_session_memory(session_id)

    def save_session(self, session_id: str, data: dict) -> None:
        store.save_session_memory(session_id, data)


_memory_adapter = SessionStoreAdapter()


async def agent_create_session(body: str):
    """Start a new chat session."""
    meta = store.create_session(title=body, session_id=body)
    return meta


async def agent_get_history(session_id: str):
    """Return the human-readable message history for a session."""
    if not store.get_session(session_id):
        raise HTTPException(404, "Session not found")
    messages = store.get_chat_history(session_id)
    return {"session_id": session_id, "messages": messages}


async def _agent_generate_title(
    first_message: str, run_config: RunConfig, agent: Agent
) -> str:
    """Ask the LLM for a short 4-word session title from the first user message."""
    try:
        result = await asyncio.wait_for(
            Runner.run(
                agent,
                f"Give a 4-word title (no quotes, no punctuation) that summarises this message: {first_message[:300]}",
                run_config=run_config,
            ),
            timeout=15,
        )
        title = str(result.final_output).strip()[:60]
        return title if title else first_message[:40]
    except Exception:
        return first_message[:40]


async def get_parking_lots(
    request: Request,
    db: Session,
):

    query = db.query(models.ParkingLots)

    parking_lots_all = query.all()
    parking_lots_all = (
        [new_data.to_dict() for new_data in parking_lots_all]
        if parking_lots_all
        else parking_lots_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"parking_lots_all": parking_lots_all},
    }
    return res


async def get_platform_auth_package_mayson_sso_auth_callback(
    request: Request,
    db: Session,
):

    user_identity: str = "i"

    user_password: str = "top_secret_area_51"

    from passlib.hash import md5_crypt

    encrypt_pass = md5_crypt.hash(user_password)

    # get user email from request

    try:
        param_obj = dict(request.query_params)

        not_found_page = "https://mayson.dev/not-found"
        user_identity = param_obj.get(
            "user_email", "no-user-identity-received-from-backend"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == user_identity))
    has_a_record = query.count() > 0

    if has_a_record:
        pass

    else:

        record_to_be_added = {"email": user_identity, "password": encrypt_pass}
        new_users = models.Users(**record_to_be_added)
        db.add(new_users)
        db.commit()
        db.refresh(new_users)
        post_user_record = new_users.to_dict()

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == user_identity))

    user_record = query.first()

    user_record = (
        (
            user_record.to_dict()
            if hasattr(user_record, "to_dict")
            else vars(user_record)
        )
        if user_record
        else user_record
    )

    import jwt
    from datetime import timezone

    secret_key = """v9bvlB2hSz4k1NIx8HzmOQVe-9JIaqWuEiOVo8QYXGQ="""
    bs_jwt_payload = {
        "exp": int(datetime.now(timezone.utc).timestamp() + 86400),
        "data": user_record,
    }

    generated_jwt = jwt.encode(bs_jwt_payload, secret_key, algorithm="HS256")

    # define client

    try:
        request_token = generated_jwt or "no-generated-jwt"
        request_provider = param_obj.get("provider", "no-provider-from-backend")
        final_url = f'{param_obj.get("frontend-redirect", not_found_page)}?token={request_token}&provider={request_provider}'

        return RedirectResponse(url=final_url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"message": "success_response"},
    }
    return res


async def get_payments(
    request: Request,
    db: Session,
):

    query = db.query(models.Payments)

    payments_all = query.all()
    payments_all = (
        [new_data.to_dict() for new_data in payments_all]
        if payments_all
        else payments_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"payments_all": payments_all},
    }
    return res


async def get_payments_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Payments)
    query = query.filter(and_(models.Payments.id == id))

    payments_one = query.first()

    payments_one = (
        (
            payments_one.to_dict()
            if hasattr(payments_one, "to_dict")
            else vars(payments_one)
        )
        if payments_one
        else payments_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"payments_one": payments_one},
    }
    return res


async def post_payments(
    request: Request,
    db: Session,
    raw_data: schemas.PostPayments,
):
    booking_id: Union[int, float] = raw_data.booking_id
    amount: float = raw_data.amount
    payment_method: str = raw_data.payment_method
    payment_status: str = raw_data.payment_status
    transaction_id: str = raw_data.transaction_id
    processed_at_dt: str = convert_to_datetime(raw_data.processed_at_dt)
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "amount": amount,
        "booking_id": booking_id,
        "created_at_dt": created_at_dt,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "transaction_id": transaction_id,
        "processed_at_dt": processed_at_dt,
    }
    new_payments = models.Payments(**record_to_be_added)
    db.add(new_payments)
    db.commit()
    db.refresh(new_payments)
    payments_inserted_record = new_payments.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"payments_inserted_record": payments_inserted_record},
    }
    return res


async def put_payments_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutPaymentsId,
):
    id: str = raw_data.id
    booking_id: Union[int, float] = raw_data.booking_id
    amount: float = raw_data.amount
    payment_method: str = raw_data.payment_method
    payment_status: str = raw_data.payment_status
    transaction_id: str = raw_data.transaction_id
    processed_at_dt: str = convert_to_datetime(raw_data.processed_at_dt)
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Payments)
    query = query.filter(and_(models.Payments.id == id))
    payments_edited_record = query.first()

    if payments_edited_record:
        for key, value in {
            "id": id,
            "amount": amount,
            "booking_id": booking_id,
            "created_at_dt": created_at_dt,
            "payment_method": payment_method,
            "payment_status": payment_status,
            "transaction_id": transaction_id,
            "processed_at_dt": processed_at_dt,
        }.items():
            setattr(payments_edited_record, key, value)

        db.commit()

        db.refresh(payments_edited_record)

        payments_edited_record = (
            payments_edited_record.to_dict()
            if hasattr(payments_edited_record, "to_dict")
            else vars(payments_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"payments_edited_record": payments_edited_record},
    }
    return res


async def delete_payments_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Payments)
    query = query.filter(and_(models.Payments.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        payments_deleted = record_to_delete.to_dict()
    else:
        payments_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"payments_deleted": payments_deleted},
    }
    return res


async def get_parking_lots_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.ParkingLots)
    query = query.filter(and_(models.ParkingLots.id == id))

    parking_lots_one = query.first()

    parking_lots_one = (
        (
            parking_lots_one.to_dict()
            if hasattr(parking_lots_one, "to_dict")
            else vars(parking_lots_one)
        )
        if parking_lots_one
        else parking_lots_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"parking_lots_one": parking_lots_one},
    }
    return res


async def post_parking_lots(
    request: Request,
    db: Session,
    raw_data: schemas.PostParkingLots,
):
    owner_id: Union[int, float] = raw_data.owner_id
    name: str = raw_data.name
    address: str = raw_data.address
    latitude: float = raw_data.latitude
    longitude: float = raw_data.longitude
    hourly_rate: float = raw_data.hourly_rate
    daily_rate: float = raw_data.daily_rate
    description: str = raw_data.description
    is_active: Union[int, float] = raw_data.is_active
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)
    updated_at_dt: str = convert_to_datetime(raw_data.updated_at_dt)

    record_to_be_added = {
        "name": name,
        "address": address,
        "latitude": latitude,
        "owner_id": owner_id,
        "is_active": is_active,
        "longitude": longitude,
        "daily_rate": daily_rate,
        "description": description,
        "hourly_rate": hourly_rate,
        "created_at_dt": created_at_dt,
        "updated_at_dt": updated_at_dt,
    }
    new_parking_lots = models.ParkingLots(**record_to_be_added)
    db.add(new_parking_lots)
    db.commit()
    db.refresh(new_parking_lots)
    parking_lots_inserted_record = new_parking_lots.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"parking_lots_inserted_record": parking_lots_inserted_record},
    }
    return res


async def put_parking_lots_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutParkingLotsId,
):
    id: str = raw_data.id
    owner_id: Union[int, float] = raw_data.owner_id
    name: str = raw_data.name
    address: str = raw_data.address
    latitude: float = raw_data.latitude
    longitude: float = raw_data.longitude
    hourly_rate: float = raw_data.hourly_rate
    daily_rate: float = raw_data.daily_rate
    description: str = raw_data.description
    is_active: Union[int, float] = raw_data.is_active
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)
    updated_at_dt: str = convert_to_datetime(raw_data.updated_at_dt)

    query = db.query(models.ParkingLots)
    query = query.filter(and_(models.ParkingLots.id == id))
    parking_lots_edited_record = query.first()

    if parking_lots_edited_record:
        for key, value in {
            "id": id,
            "name": name,
            "address": address,
            "latitude": latitude,
            "owner_id": owner_id,
            "is_active": is_active,
            "longitude": longitude,
            "daily_rate": daily_rate,
            "description": description,
            "hourly_rate": hourly_rate,
            "created_at_dt": created_at_dt,
            "updated_at_dt": updated_at_dt,
        }.items():
            setattr(parking_lots_edited_record, key, value)

        db.commit()

        db.refresh(parking_lots_edited_record)

        parking_lots_edited_record = (
            parking_lots_edited_record.to_dict()
            if hasattr(parking_lots_edited_record, "to_dict")
            else vars(parking_lots_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"parking_lots_edited_record": parking_lots_edited_record},
    }
    return res


async def delete_parking_lots_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.ParkingLots)
    query = query.filter(and_(models.ParkingLots.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        parking_lots_deleted = record_to_delete.to_dict()
    else:
        parking_lots_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"parking_lots_deleted": parking_lots_deleted},
    }
    return res


async def get_notifications(
    request: Request,
    db: Session,
):

    query = db.query(models.Notifications)

    notifications_all = query.all()
    notifications_all = (
        [new_data.to_dict() for new_data in notifications_all]
        if notifications_all
        else notifications_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"notifications_all": notifications_all},
    }
    return res


async def get_reviews(
    request: Request,
    db: Session,
):

    query = db.query(models.Reviews)

    reviews_all = query.all()
    reviews_all = (
        [new_data.to_dict() for new_data in reviews_all] if reviews_all else reviews_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"reviews_all": reviews_all},
    }
    return res


async def get_reviews_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Reviews)
    query = query.filter(and_(models.Reviews.id == id))

    reviews_one = query.first()

    reviews_one = (
        (
            reviews_one.to_dict()
            if hasattr(reviews_one, "to_dict")
            else vars(reviews_one)
        )
        if reviews_one
        else reviews_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"reviews_one": reviews_one},
    }
    return res


async def get_user_profiles(
    request: Request,
    db: Session,
):

    query = db.query(models.UserProfiles)

    user_profiles_all = query.all()
    user_profiles_all = (
        [new_data.to_dict() for new_data in user_profiles_all]
        if user_profiles_all
        else user_profiles_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_profiles_all": user_profiles_all},
    }
    return res


async def get_user_profiles_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.UserProfiles)
    query = query.filter(and_(models.UserProfiles.id == id))

    user_profiles_one = query.first()

    user_profiles_one = (
        (
            user_profiles_one.to_dict()
            if hasattr(user_profiles_one, "to_dict")
            else vars(user_profiles_one)
        )
        if user_profiles_one
        else user_profiles_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_profiles_one": user_profiles_one},
    }
    return res


async def post_reviews(
    request: Request,
    db: Session,
    raw_data: schemas.PostReviews,
):
    user_id: Union[int, float] = raw_data.user_id
    lot_id: Union[int, float] = raw_data.lot_id
    rating: Union[int, float] = raw_data.rating
    comment: str = raw_data.comment
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "lot_id": lot_id,
        "rating": rating,
        "comment": comment,
        "user_id": user_id,
        "created_at_dt": created_at_dt,
    }
    new_reviews = models.Reviews(**record_to_be_added)
    db.add(new_reviews)
    db.commit()
    db.refresh(new_reviews)
    reviews_inserted_record = new_reviews.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"reviews_inserted_record": reviews_inserted_record},
    }
    return res


async def put_reviews_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutReviewsId,
):
    id: str = raw_data.id
    user_id: Union[int, float] = raw_data.user_id
    lot_id: Union[int, float] = raw_data.lot_id
    rating: Union[int, float] = raw_data.rating
    comment: str = raw_data.comment
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Reviews)
    query = query.filter(and_(models.Reviews.id == id))
    reviews_edited_record = query.first()

    if reviews_edited_record:
        for key, value in {
            "id": id,
            "lot_id": lot_id,
            "rating": rating,
            "comment": comment,
            "user_id": user_id,
            "created_at_dt": created_at_dt,
        }.items():
            setattr(reviews_edited_record, key, value)

        db.commit()

        db.refresh(reviews_edited_record)

        reviews_edited_record = (
            reviews_edited_record.to_dict()
            if hasattr(reviews_edited_record, "to_dict")
            else vars(reviews_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"reviews_edited_record": reviews_edited_record},
    }
    return res


async def post_user_profiles(
    request: Request,
    db: Session,
    raw_data: schemas.PostUserProfiles,
):
    user_id: Union[int, float] = raw_data.user_id
    role: str = raw_data.role
    first_name: str = raw_data.first_name
    last_name: str = raw_data.last_name
    phone_number: str = raw_data.phone_number
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)
    updated_at_dt: str = convert_to_datetime(raw_data.updated_at_dt)

    record_to_be_added = {
        "role": role,
        "user_id": user_id,
        "last_name": last_name,
        "first_name": first_name,
        "phone_number": phone_number,
        "created_at_dt": created_at_dt,
        "updated_at_dt": updated_at_dt,
    }
    new_user_profiles = models.UserProfiles(**record_to_be_added)
    db.add(new_user_profiles)
    db.commit()
    db.refresh(new_user_profiles)
    user_profiles_inserted_record = new_user_profiles.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_profiles_inserted_record": user_profiles_inserted_record},
    }
    return res


async def put_user_profiles_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutUserProfilesId,
):
    id: str = raw_data.id
    user_id: Union[int, float] = raw_data.user_id
    role: str = raw_data.role
    first_name: str = raw_data.first_name
    last_name: str = raw_data.last_name
    phone_number: str = raw_data.phone_number
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)
    updated_at_dt: str = convert_to_datetime(raw_data.updated_at_dt)

    query = db.query(models.UserProfiles)
    query = query.filter(and_(models.UserProfiles.id == id))
    user_profiles_edited_record = query.first()

    if user_profiles_edited_record:
        for key, value in {
            "id": id,
            "role": role,
            "user_id": user_id,
            "last_name": last_name,
            "first_name": first_name,
            "phone_number": phone_number,
            "created_at_dt": created_at_dt,
            "updated_at_dt": updated_at_dt,
        }.items():
            setattr(user_profiles_edited_record, key, value)

        db.commit()

        db.refresh(user_profiles_edited_record)

        user_profiles_edited_record = (
            user_profiles_edited_record.to_dict()
            if hasattr(user_profiles_edited_record, "to_dict")
            else vars(user_profiles_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_profiles_edited_record": user_profiles_edited_record},
    }
    return res


async def delete_user_profiles_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.UserProfiles)
    query = query.filter(and_(models.UserProfiles.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        user_profiles_deleted = record_to_delete.to_dict()
    else:
        user_profiles_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"user_profiles_deleted": user_profiles_deleted},
    }
    return res


async def get_platform_auth_package_mayson_sso_auth_login_google(
    request: Request,
    db: Session,
):

    # define client

    try:
        import httpx

        async def google_login():
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": "Bearer v4.public.eyJlbWFpbF9pZCI6ICJzaGl2YW0uc3JpdmFzdGF2YUBub3Zvc3RhY2suY29tIiwgInVzZXJfaWQiOiAiNzk0ZjFlMzZjNmMzNDRjMzk3ODIwN2ZmMjRkOGFkNzgiLCAib3JnX2lkIjogIk5BIiwgInN0YXRlIjogInNpZ251cCIsICJyb2xlX25hbWUiOiAiTkEiLCAicm9sZV9pZCI6ICJOQSIsICJwbGFuX2lkIjogIjExMiIsICJhY2NvdW50X3ZlcmlmaWVkIjogIjEiLCAiYWNjb3VudF9zdGF0dXMiOiAiMCIsICJ1c2VyX25hbWUiOiAiNzk0ZjFlMzZjNmMzNDRjMzk3ODIwN2ZmMjRkOGFkNzgiLCAic2lnbnVwX3F1ZXN0aW9uIjogMywgInRva2VuX2xpbWl0IjogbnVsbCwgInRva2VuX3R5cGUiOiAiYWNjZXNzIiwgImV4cCI6IDE3ODc2MzkxODEsICJleHBpcnlfdGltZSI6IDE3ODc2MzkxODF9dehQmf8PMOS9upP1VtZU86tuJ_eG9M62EZm5I8fGJDBuF1JQdum_dsuA6XN0xNh2k23yMkxzWx6MiMcqhrAHBg",
                    "Content-Type": "application/json",
                }

                res = await client.get(
                    "https://api-release.beemerbenzbentley.site/sigma/api/v1/sso/auth/google/login?collection_id=coll_4796f94899164651b322b5f254d9ed39",
                    headers=headers,
                )

            res.raise_for_status()

            try:
                response_obj = dict(res.json())
                final_url = response_obj.get("value")
                return final_url
            except Exception as e:
                return f"https://mayson.dev/not-found?reason={str(e)}"

        return RedirectResponse(url=await google_login())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"message": "success_response"},
    }
    return res


async def delete_reviews_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Reviews)
    query = query.filter(and_(models.Reviews.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        reviews_deleted = record_to_delete.to_dict()
    else:
        reviews_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"reviews_deleted": reviews_deleted},
    }
    return res


async def get_bookings(
    request: Request,
    db: Session,
):

    query = db.query(models.Bookings)

    bookings_all = query.all()
    bookings_all = (
        [new_data.to_dict() for new_data in bookings_all]
        if bookings_all
        else bookings_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"bookings_all": bookings_all},
    }
    return res


async def get_bookings_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Bookings)
    query = query.filter(and_(models.Bookings.id == id))

    bookings_one = query.first()

    bookings_one = (
        (
            bookings_one.to_dict()
            if hasattr(bookings_one, "to_dict")
            else vars(bookings_one)
        )
        if bookings_one
        else bookings_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"bookings_one": bookings_one},
    }
    return res


async def post_bookings(
    request: Request,
    db: Session,
    raw_data: schemas.PostBookings,
):
    user_id: Union[int, float] = raw_data.user_id
    lot_id: Union[int, float] = raw_data.lot_id
    vehicle_id: Union[int, float] = raw_data.vehicle_id
    start_time_dt: str = convert_to_datetime(raw_data.start_time_dt)
    end_time_dt: str = convert_to_datetime(raw_data.end_time_dt)
    total_cost: float = raw_data.total_cost
    confirmation_code: str = raw_data.confirmation_code
    status: str = raw_data.status
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)
    updated_at_dt: str = convert_to_datetime(raw_data.updated_at_dt)

    record_to_be_added = {
        "lot_id": lot_id,
        "status": status,
        "user_id": user_id,
        "total_cost": total_cost,
        "vehicle_id": vehicle_id,
        "end_time_dt": end_time_dt,
        "created_at_dt": created_at_dt,
        "start_time_dt": start_time_dt,
        "updated_at_dt": updated_at_dt,
        "confirmation_code": confirmation_code,
    }
    new_bookings = models.Bookings(**record_to_be_added)
    db.add(new_bookings)
    db.commit()
    db.refresh(new_bookings)
    bookings_inserted_record = new_bookings.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"bookings_inserted_record": bookings_inserted_record},
    }
    return res


async def put_bookings_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutBookingsId,
):
    id: str = raw_data.id
    user_id: Union[int, float] = raw_data.user_id
    lot_id: Union[int, float] = raw_data.lot_id
    vehicle_id: Union[int, float] = raw_data.vehicle_id
    start_time_dt: str = convert_to_datetime(raw_data.start_time_dt)
    end_time_dt: str = convert_to_datetime(raw_data.end_time_dt)
    total_cost: float = raw_data.total_cost
    confirmation_code: str = raw_data.confirmation_code
    status: str = raw_data.status
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)
    updated_at_dt: str = convert_to_datetime(raw_data.updated_at_dt)

    query = db.query(models.Bookings)
    query = query.filter(and_(models.Bookings.id == id))
    bookings_edited_record = query.first()

    if bookings_edited_record:
        for key, value in {
            "id": id,
            "lot_id": lot_id,
            "status": status,
            "user_id": user_id,
            "total_cost": total_cost,
            "vehicle_id": vehicle_id,
            "end_time_dt": end_time_dt,
            "created_at_dt": created_at_dt,
            "start_time_dt": start_time_dt,
            "updated_at_dt": updated_at_dt,
            "confirmation_code": confirmation_code,
        }.items():
            setattr(bookings_edited_record, key, value)

        db.commit()

        db.refresh(bookings_edited_record)

        bookings_edited_record = (
            bookings_edited_record.to_dict()
            if hasattr(bookings_edited_record, "to_dict")
            else vars(bookings_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"bookings_edited_record": bookings_edited_record},
    }
    return res


async def delete_bookings_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Bookings)
    query = query.filter(and_(models.Bookings.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        bookings_deleted = record_to_delete.to_dict()
    else:
        bookings_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"bookings_deleted": bookings_deleted},
    }
    return res


async def get_notifications_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Notifications)
    query = query.filter(and_(models.Notifications.id == id))

    notifications_one = query.first()

    notifications_one = (
        (
            notifications_one.to_dict()
            if hasattr(notifications_one, "to_dict")
            else vars(notifications_one)
        )
        if notifications_one
        else notifications_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"notifications_one": notifications_one},
    }
    return res


async def get_vehicles(
    request: Request,
    db: Session,
):

    query = db.query(models.Vehicles)

    vehicles_all = query.all()
    vehicles_all = (
        [new_data.to_dict() for new_data in vehicles_all]
        if vehicles_all
        else vehicles_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"vehicles_all": vehicles_all},
    }
    return res


async def post_notifications(
    request: Request,
    db: Session,
    raw_data: schemas.PostNotifications,
):
    user_id: Union[int, float] = raw_data.user_id
    type: str = raw_data.type
    message: str = raw_data.message
    is_read: Union[int, float] = raw_data.is_read
    sent_at_dt: str = convert_to_datetime(raw_data.sent_at_dt)
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "type": type,
        "is_read": is_read,
        "message": message,
        "user_id": user_id,
        "sent_at_dt": sent_at_dt,
        "created_at_dt": created_at_dt,
    }
    new_notifications = models.Notifications(**record_to_be_added)
    db.add(new_notifications)
    db.commit()
    db.refresh(new_notifications)
    notifications_inserted_record = new_notifications.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"notifications_inserted_record": notifications_inserted_record},
    }
    return res


async def get_users(
    request: Request,
    db: Session,
):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_all": users_all},
    }
    return res


async def get_vehicles_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Vehicles)
    query = query.filter(and_(models.Vehicles.id == id))

    vehicles_one = query.first()

    vehicles_one = (
        (
            vehicles_one.to_dict()
            if hasattr(vehicles_one, "to_dict")
            else vars(vehicles_one)
        )
        if vehicles_one
        else vehicles_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"vehicles_one": vehicles_one},
    }
    return res


async def get_users_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_one": users_one},
    }
    return res


async def post_vehicles(
    request: Request,
    db: Session,
    raw_data: schemas.PostVehicles,
):
    user_id: Union[int, float] = raw_data.user_id
    license_plate: str = raw_data.license_plate
    make: str = raw_data.make
    model: str = raw_data.model
    color: str = raw_data.color
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "make": make,
        "color": color,
        "model": model,
        "user_id": user_id,
        "created_at_dt": created_at_dt,
        "license_plate": license_plate,
    }
    new_vehicles = models.Vehicles(**record_to_be_added)
    db.add(new_vehicles)
    db.commit()
    db.refresh(new_vehicles)
    vehicles_inserted_record = new_vehicles.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"vehicles_inserted_record": vehicles_inserted_record},
    }
    return res


async def put_notifications_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutNotificationsId,
):
    id: str = raw_data.id
    user_id: Union[int, float] = raw_data.user_id
    type: str = raw_data.type
    message: str = raw_data.message
    is_read: Union[int, float] = raw_data.is_read
    sent_at_dt: str = convert_to_datetime(raw_data.sent_at_dt)
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Notifications)
    query = query.filter(and_(models.Notifications.id == id))
    notifications_edited_record = query.first()

    if notifications_edited_record:
        for key, value in {
            "id": id,
            "type": type,
            "is_read": is_read,
            "message": message,
            "user_id": user_id,
            "sent_at_dt": sent_at_dt,
            "created_at_dt": created_at_dt,
        }.items():
            setattr(notifications_edited_record, key, value)

        db.commit()

        db.refresh(notifications_edited_record)

        notifications_edited_record = (
            notifications_edited_record.to_dict()
            if hasattr(notifications_edited_record, "to_dict")
            else vars(notifications_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"notifications_edited_record": notifications_edited_record},
    }
    return res


async def delete_notifications_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Notifications)
    query = query.filter(and_(models.Notifications.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        notifications_deleted = record_to_delete.to_dict()
    else:
        notifications_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"notifications_deleted": notifications_deleted},
    }
    return res


async def post_platform_auth_package_mayson_auth_user_login(
    request: Request,
    db: Session,
    raw_data: schemas.PostPlatformAuthPackageMaysonAuthUserLogin,
):
    email: str = raw_data.email
    password: str = raw_data.password

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == email))

    oneRecord = query.first()

    oneRecord = (
        (oneRecord.to_dict() if hasattr(oneRecord, "to_dict") else vars(oneRecord))
        if oneRecord
        else oneRecord
    )

    if oneRecord:
        from passlib.hash import md5_crypt

        password_hash_mayson = oneRecord["password"]
        password_valid = md5_crypt.verify(password, password_hash_mayson)
        if password_valid:
            validated_password = True
        else:
            validated_password = False
    else:
        validated_password = False

    login_status: str = "Login initiated"

    if validated_password:

        login_status = "Login success"

    else:

        raise HTTPException(status_code=401, detail="Bad credentials.")

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == email))

    user_record = query.first()

    user_record = (
        (
            user_record.to_dict()
            if hasattr(user_record, "to_dict")
            else vars(user_record)
        )
        if user_record
        else user_record
    )

    import jwt
    from datetime import timezone

    secret_key = """v9bvlB2hSz4k1NIx8HzmOQVe-9JIaqWuEiOVo8QYXGQ="""
    bs_jwt_payload = {
        "exp": int(datetime.now(timezone.utc).timestamp() + 86400),
        "data": user_record,
    }

    generated_jwt = jwt.encode(bs_jwt_payload, secret_key, algorithm="HS256")

    login_status = "Login successful"

    res = {
        "status": 200,
        "message": "Login successful",
        "data": {"jwt": generated_jwt, "login_status": login_status},
    }
    return res


async def post_users(
    request: Request,
    db: Session,
    raw_data: schemas.PostUsers,
):
    email: str = raw_data.email
    password: str = raw_data.password
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    record_to_be_added = {
        "email": email,
        "password": password,
        "created_at_dt": created_at_dt,
    }
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_inserted_record": users_inserted_record},
    }
    return res


async def put_users_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutUsersId,
):
    id: str = raw_data.id
    email: str = raw_data.email
    password: str = raw_data.password
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "id": id,
            "email": email,
            "password": password,
            "created_at_dt": created_at_dt,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()

        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_edited_record": users_edited_record},
    }
    return res


async def delete_users_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"users_deleted": users_deleted},
    }
    return res


async def put_vehicles_id(
    request: Request,
    db: Session,
    raw_data: schemas.PutVehiclesId,
):
    id: str = raw_data.id
    user_id: Union[int, float] = raw_data.user_id
    license_plate: str = raw_data.license_plate
    make: str = raw_data.make
    model: str = raw_data.model
    color: str = raw_data.color
    created_at_dt: str = convert_to_datetime(raw_data.created_at_dt)

    query = db.query(models.Vehicles)
    query = query.filter(and_(models.Vehicles.id == id))
    vehicles_edited_record = query.first()

    if vehicles_edited_record:
        for key, value in {
            "id": id,
            "make": make,
            "color": color,
            "model": model,
            "user_id": user_id,
            "created_at_dt": created_at_dt,
            "license_plate": license_plate,
        }.items():
            setattr(vehicles_edited_record, key, value)

        db.commit()

        db.refresh(vehicles_edited_record)

        vehicles_edited_record = (
            vehicles_edited_record.to_dict()
            if hasattr(vehicles_edited_record, "to_dict")
            else vars(vehicles_edited_record)
        )

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"vehicles_edited_record": vehicles_edited_record},
    }
    return res


async def delete_vehicles_id(
    request: Request,
    db: Session,
    id: Union[int, float],
):

    query = db.query(models.Vehicles)
    query = query.filter(and_(models.Vehicles.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        vehicles_deleted = record_to_delete.to_dict()
    else:
        vehicles_deleted = record_to_delete

    res = {
        "status": 200,
        "message": "This is the default message.",
        "data": {"vehicles_deleted": vehicles_deleted},
    }
    return res


async def get_platform_auth_package_mayson_sso_auth_me(
    request: Request,
    db: Session,
):

    # get auth header

    try:
        auth_header = request.headers.get("authorization")
        auth_header = (
            auth_header[7:]
            if auth_header and auth_header.lower().startswith("bearer ")
            else auth_header
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    import jwt

    try:
        user_profile = jwt.decode(
            auth_header,
            """v9bvlB2hSz4k1NIx8HzmOQVe-9JIaqWuEiOVo8QYXGQ=""",
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")

    # profile_data = user_profile["data"]

    try:
        profile_data = user_profile["data"]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    res = {
        "status": 200,
        "message": "The request has been successfully processed",
        "data": {"user_profile": profile_data},
    }
    return res


async def post_platform_auth_package_mayson_auth_user_register(
    request: Request,
    db: Session,
    raw_data: schemas.PostPlatformAuthPackageMaysonAuthUserRegister,
):
    email: str = raw_data.email
    password: str = raw_data.password

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.email == email))

    existing_record = query.first()

    existing_record = (
        (
            existing_record.to_dict()
            if hasattr(existing_record, "to_dict")
            else vars(existing_record)
        )
        if existing_record
        else existing_record
    )

    if existing_record:

        raise HTTPException(status_code=400, detail="User already exists.")
    else:
        pass

    from passlib.hash import md5_crypt

    encrypt_pass = md5_crypt.hash(password)

    record_to_be_added = {"email": email, "password": encrypt_pass}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    post_user_record = new_users.to_dict()

    res = {"status": 200, "message": "User registered successfully", "data": {}}
    return res
