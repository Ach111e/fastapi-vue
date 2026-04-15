from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.tags as crud
from src.auth.jwthandler import get_current_user
from src.schemas.tags import TagOutSchema, TagInSchema, UpdateTag
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/tags",
    response_model=List[TagOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_tags():
    return await crud.get_tags()


@router.get(
    "/tag/{tag_id}",
    response_model=TagOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_tag(tag_id: int) -> TagOutSchema:
    try:
        return await crud.get_tag(tag_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Tag does not exist",
        )


@router.post(
    "/tags", response_model=TagOutSchema, dependencies=[Depends(get_current_user)]
)
async def create_tag(
    tag: TagInSchema, current_user: UserOutSchema = Depends(get_current_user)
) -> TagOutSchema:
    return await crud.create_tag(tag)


@router.patch(
    "/tag/{tag_id}",
    dependencies=[Depends(get_current_user)],
    response_model=TagOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_tag(
    tag_id: int,
    tag: UpdateTag,
    current_user: UserOutSchema = Depends(get_current_user),
) -> TagOutSchema:
    return await crud.update_tag(tag_id, tag)


@router.delete(
    "/tag/{tag_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_tag(
    tag_id: int, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_tag(tag_id)
