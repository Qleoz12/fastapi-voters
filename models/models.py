import uuid

from sqlalchemy import Column, Integer, String, Enum,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import enum

# Enum para los roles de usuario
from models.db import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    LEAD = "lead"
    USER = "user"

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True,default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(Enum(UserRole, name="userrole"), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipality.id'), nullable=False)
    address = Column(String, nullable=False)
    picture = Column(String, nullable=True)  # URL de la foto

    # Relationship to Voters (as a voter)
    voters = relationship('Voters', back_populates='user', foreign_keys='Voters.user_id')

    # Relationship to Voters (as a leader)
    leads = relationship('Voters', back_populates='leader', foreign_keys='Voters.leader_id')



class Municipality(Base):
    __tablename__ = 'municipality'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    c_digo_dane_del_municipio =Column(String, nullable=False)
    c_digo_dane_del_departamento = Column(Integer, nullable=False)
    region =Column(String, nullable=False)
    state_id=Column(Integer, ForeignKey('state.id'), nullable=False)
    # Relationship to VotersTable
    voters_tables = relationship('VotersTable', back_populates='municipality')

class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    c_digo_dane_del_departamento = Column(Integer, nullable=False)
    region =Column(String, nullable=False)

# Entidad Votante
class Voters(Base):
    __tablename__ = 'voters'

    id = Column(String, primary_key=True, index=True,default=lambda: str(uuid.uuid4()))
    dni = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    coordinates = Column(String, nullable=False)  # Coordenadas obtenidas por georreferenciación
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    voters_table_id = Column(Integer, ForeignKey('voters_table.id'), nullable=False)
    leader_id = Column(String, ForeignKey('users.id'), nullable=False)

    voters_table = relationship('VotersTable', back_populates='voters')
    # Relationship to User (as a voter)
    user = relationship('User', back_populates='voters', foreign_keys=[user_id])
    # Relationship to Leader
    leader = relationship('User', back_populates='leads', foreign_keys=[leader_id])


# Entidad MesaDeVotacion
class VotersTable(Base):
    __tablename__ = 'voters_table'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    municipality_id = Column(Integer, ForeignKey('municipality.id'), nullable=False)

    # municipality = relationship('Municipality', back_populates='voters_table')
    municipality  = relationship('Municipality', back_populates='voters_tables')
    # Relationship to Voters
    voters = relationship('Voters', back_populates='voters_table')