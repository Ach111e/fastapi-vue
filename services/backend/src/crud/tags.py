from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Tags
from src.schemas.tags import TagOutSchema
from src.schemas.token import Status


async def get_tags():
    return await TagOutSchema.from_queryset(Tags.all())


async def get_tag(tag_id) -> TagOutSchema:
    return await TagOutSchema.from_queryset_single(Tags.get(id=tag_id))


async def create_tag(tag) -> TagOutSchema:
    tag_dict = tag.dict(exclude_unset=True)
    tag_obj = await Tags.create(**tag_dict)
    return await TagOutSchema.from_tortoise_orm(tag_obj)


async def update_tag(tag_id, tag) -> TagOutSchema:
    try:
        await TagOutSchema.from_queryset_single(Tags.get(id=tag_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")

    await Tags.filter(id=tag_id).update(**tag.dict(exclude_unset=True))
    return await TagOutSchema.from_queryset_single(Tags.get(id=tag_id))


async def delete_tag(tag_id) -> Status:
    try:
        await TagOutSchema.from_queryset_single(Tags.get(id=tag_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")

    deleted_count = await Tags.filter(id=tag_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")
    return Status(message=f"Deleted tag {tag_id}")
