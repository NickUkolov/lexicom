from fastapi import Depends, APIRouter, HTTPException, status, Request

from app.db import RedisService
from app.dependencies import get_redis
from app.models import Phone, Address, PhoneAddress

router = APIRouter(
    tags=["Address"],
)


@router.get("/check_data", response_model=Address)
async def read_address(request: Request,
                       phone: Phone = Depends(),
                       db: RedisService = Depends(get_redis)):
    address = await db.get_address(phone.phone)
    if not address:
        raise HTTPException(detail="No address found", status_code=status.HTTP_404_NOT_FOUND)
    return address


@router.post("/write_data", response_model=PhoneAddress)
async def create_address(data: PhoneAddress,
                         request: Request,
                         db: RedisService = Depends(get_redis)):
    if await db.get_address(data.phone):
        raise HTTPException(detail="Address exists", status_code=status.HTTP_400_BAD_REQUEST)
    result = await db.set_address(data.phone, data.address)
    if not result:
        raise HTTPException(detail="Failed to add the address", status_code=status.HTTP_400_BAD_REQUEST)
    return result


@router.put("/write_data", response_model=PhoneAddress)
async def update_address(data: PhoneAddress,
                         request: Request,
                         db: RedisService = Depends(get_redis)):
    if not await db.get_address(data.phone):
        raise HTTPException(detail="No address found", status_code=status.HTTP_404_NOT_FOUND)
    result = await db.set_address(data.phone, data.address)
    if not result:
        raise HTTPException(detail="Failed to update the address", status_code=status.HTTP_400_BAD_REQUEST)
    return result
