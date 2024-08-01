from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, constr, EmailStr



# User Pydantic schema
from models.models import UserRole


class UserSchema(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str
    rol: UserRole
    municipality_id: int
    address: str
    picture: Optional[str] = None  # URL of the picture

    # voters: List['VoterSchema'] = []  # List of related voters

    class Config:
        from_attributes = True

class UserSchemaStandart(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    rol: UserRole
    municipality_id: int
    address: str
    picture: Optional[str] = None  # URL of the picture

    # voters: List['VoterSchema'] = []  # List of related voters

    class Config:
        from_attributes = True


# Municipality Pydantic schema
class MunicipalitySchema(BaseModel):
    id: int
    name: str
    # departamento_id: Optional[int]
    mesas_de_votacion: List['VotersTableSchema'] = []

    class Config:
        from_attributes = True

class StateSchema(BaseModel):
    id: int
    name: str
    c_digo_dane_del_departamento: int
    region: str

    class Config:
        orm_mode = True

# Voter Pydantic schema
class VoterSchema(BaseModel):
    id: Optional[int] = None
    dni: str
    address: str
    user_id: str
    voters_table_id: int

    class Config:
        from_attributes = True


# VotersTable Pydantic schema
class VotersTableSchema(BaseModel):
    id: Optional[int] = None
    code: str
    municipality_id: int

    class Config:
        from_attributes = True


# Resolve forward references
UserSchema.update_forward_refs()
MunicipalitySchema.update_forward_refs()
VoterSchema.update_forward_refs()
VotersTableSchema.update_forward_refs()
