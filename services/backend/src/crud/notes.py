from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Notes, Tags
from src.schemas.notes import NoteOutSchema
from src.schemas.token import Status


async def get_notes(tag_id: int = None):
    if tag_id:
        return await NoteOutSchema.from_queryset(Notes.filter(tags__id=tag_id))
    return await NoteOutSchema.from_queryset(Notes.all())


async def get_note(note_id) -> NoteOutSchema:
    return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))


async def create_note(note, current_user) -> NoteOutSchema:
    note_dict = note.dict(exclude_unset=True)
    note_dict["author_id"] = current_user.id
    tags = note_dict.pop("tags", [])
    note_obj = await Notes.create(**note_dict)
    if tags:
        await note_obj.tags.add(*tags)
    return await NoteOutSchema.from_tortoise_orm(note_obj)


async def update_note(note_id, note, current_user) -> NoteOutSchema:
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    if db_note.author.id == current_user.id:
        note_dict = note.dict(exclude_unset=True)
        tags = note_dict.pop("tags", None)
        if note_dict:
            await Notes.filter(id=note_id).update(**note_dict)
        
        if tags is not None:
            note_obj = await Notes.get(id=note_id)
            await note_obj.tags.clear()
            if tags:
                await note_obj.tags.add(*tags)
        
        return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_note(note_id, current_user) -> Status:
    try:
        db_note = await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")

    if db_note.author.id == current_user.id:
        deleted_count = await Notes.filter(id=note_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
        return Status(message=f"Deleted note {note_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
