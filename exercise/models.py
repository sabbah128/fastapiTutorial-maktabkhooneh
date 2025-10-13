from pydantic import BaseModel, Field, field_serializer


class NameBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Person's name")

    @field_serializer("name")
    def serializer_name(self, value: str):
        return value.title()


class NameCreate(NameBase):
    pass


class NameUpdate(NameBase):
    pass


class Name(NameBase):
    id: int