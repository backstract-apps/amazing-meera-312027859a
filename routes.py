from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, Query, Form, File
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional
import service, models, schemas
from database import SessionLocal
from middleware.application_middleware import platform_auth_platform_auth_middleware_group_dependency, default_dependency


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/parking_lots/')
async def get_parking_lots(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_parking_lots(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/platform_auth_package/mayson/sso/auth/callback/')
async def get_platform_auth_package_mayson_sso_auth_callback(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_platform_auth_package_mayson_sso_auth_callback(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/payments/')
async def get_payments(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_payments(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/payments/id/')
async def get_payments_id(request: Request, query: schemas.GetPaymentsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_payments_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/payments/')
async def post_payments(request: Request, raw_data: schemas.PostPayments, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_payments(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/payments/id/')
async def put_payments_id(request: Request, raw_data: schemas.PutPaymentsId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_payments_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/payments/id/')
async def delete_payments_id(request: Request, query: schemas.DeletePaymentsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_payments_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/parking_lots/id/')
async def get_parking_lots_id(request: Request, query: schemas.GetParkingLotsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_parking_lots_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/parking_lots/')
async def post_parking_lots(request: Request, raw_data: schemas.PostParkingLots, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_parking_lots(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/parking_lots/id/')
async def put_parking_lots_id(request: Request, raw_data: schemas.PutParkingLotsId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_parking_lots_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/parking_lots/id/')
async def delete_parking_lots_id(request: Request, query: schemas.DeleteParkingLotsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_parking_lots_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/notifications/')
async def get_notifications(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_notifications(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/reviews/')
async def get_reviews(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_reviews(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/reviews/id/')
async def get_reviews_id(request: Request, query: schemas.GetReviewsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_reviews_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/user_profiles/')
async def get_user_profiles(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_user_profiles(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/user_profiles/id/')
async def get_user_profiles_id(request: Request, query: schemas.GetUserProfilesIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_user_profiles_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/reviews/')
async def post_reviews(request: Request, raw_data: schemas.PostReviews, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_reviews(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/reviews/id/')
async def put_reviews_id(request: Request, raw_data: schemas.PutReviewsId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_reviews_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/user_profiles/')
async def post_user_profiles(request: Request, raw_data: schemas.PostUserProfiles, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_user_profiles(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/user_profiles/id/')
async def put_user_profiles_id(request: Request, raw_data: schemas.PutUserProfilesId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_user_profiles_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/user_profiles/id/')
async def delete_user_profiles_id(request: Request, query: schemas.DeleteUserProfilesIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_user_profiles_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/platform_auth_package/mayson/sso/auth/login/google')
async def get_platform_auth_package_mayson_sso_auth_login_google(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_platform_auth_package_mayson_sso_auth_login_google(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/reviews/id/')
async def delete_reviews_id(request: Request, query: schemas.DeleteReviewsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_reviews_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/bookings/')
async def get_bookings(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_bookings(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/bookings/id/')
async def get_bookings_id(request: Request, query: schemas.GetBookingsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_bookings_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/bookings/')
async def post_bookings(request: Request, raw_data: schemas.PostBookings, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_bookings(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/bookings/id/')
async def put_bookings_id(request: Request, raw_data: schemas.PutBookingsId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_bookings_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/bookings/id/')
async def delete_bookings_id(request: Request, query: schemas.DeleteBookingsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_bookings_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/notifications/id/')
async def get_notifications_id(request: Request, query: schemas.GetNotificationsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_notifications_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/vehicles/')
async def get_vehicles(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_vehicles(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/notifications/')
async def post_notifications(request: Request, raw_data: schemas.PostNotifications, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_notifications(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/')
async def get_users(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_users(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/vehicles/id/')
async def get_vehicles_id(request: Request, query: schemas.GetVehiclesIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_vehicles_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/users/id/')
async def get_users_id(request: Request, query: schemas.GetUsersIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_users_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/vehicles/')
async def post_vehicles(request: Request, raw_data: schemas.PostVehicles, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_vehicles(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/notifications/id/')
async def put_notifications_id(request: Request, raw_data: schemas.PutNotificationsId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_notifications_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/notifications/id/')
async def delete_notifications_id(request: Request, query: schemas.DeleteNotificationsIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_notifications_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/platform_auth_package/mayson/auth/user/login')
async def post_platform_auth_package_mayson_auth_user_login(request: Request, raw_data: schemas.PostPlatformAuthPackageMaysonAuthUserLogin, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_platform_auth_package_mayson_auth_user_login(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/users/')
async def post_users(request: Request, raw_data: schemas.PostUsers, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_users(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/users/id/')
async def put_users_id(request: Request, raw_data: schemas.PutUsersId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_users_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/users/id/')
async def delete_users_id(request: Request, query: schemas.DeleteUsersIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_users_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/vehicles/id/')
async def put_vehicles_id(request: Request, raw_data: schemas.PutVehiclesId, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.put_vehicles_id(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/vehicles/id/')
async def delete_vehicles_id(request: Request, query: schemas.DeleteVehiclesIdQueryParams = Depends(), db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.delete_vehicles_id(request, db, query.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/platform_auth_package/mayson/sso/auth/me')
async def get_platform_auth_package_mayson_sso_auth_me(request: Request, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.get_platform_auth_package_mayson_sso_auth_me(request, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/platform_auth_package/mayson/auth/user/register')
async def post_platform_auth_package_mayson_auth_user_register(request: Request, raw_data: schemas.PostPlatformAuthPackageMaysonAuthUserRegister, db: Session = Depends(get_db), protected_deps_1: dict = Depends(platform_auth_platform_auth_middleware_group_dependency), protected_deps_2: dict = Depends(default_dependency),  ):
    try:
        return await service.post_platform_auth_package_mayson_auth_user_register(request, db, raw_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

