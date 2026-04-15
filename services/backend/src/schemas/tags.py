from typing import Optional, List

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Tags


TagInSchema = pydantic_model_creator(
    Tags, name="TagIn", exclude_readonly=True)
TagOutSchema = pydantic_model_creator(
    Tags, name="Tag", exclude =[
      "modified_at", "created_at"
    ]
)


class UpdateTag(BaseModel):
    name: Optional[str]
