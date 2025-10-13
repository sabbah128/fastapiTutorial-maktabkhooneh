from pydantic import BaseModel, field_validator, field_serializer, Field


class PersonBaseSchema(BaseModel):
    name: str= Field(..., description="Name Person")

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError("Name must be less than 32 characters.")
        if not value.isalpha():
            raise ValueError("Name must be only alphabetic characters.")
        return value
    
    @field_serializer("name")
    def serializer_name(self, value: str):
        return value.title()


class PersonSchema(PersonBaseSchema):
    pass


class ResponseSchema(PersonBaseSchema):
    id: int


class UpdateSchema(PersonBaseSchema):
    pass