
from sqlite3 import IntegrityError
from typing import List

from auth.authorizations import authorize
from fastapi import APIRouter
from fastapi import Depends ,status,HTTPException

from auth.authentications import get_current_user
from models.db import get_db
from models.models import UserRole, VotersTable
from models.shcemas import UserSchema, VoterSchema, VotersTableSchema
from sqlalchemy.orm import Session

voterTablesApp = APIRouter(prefix="/votersTable",
                           tags=["voters"])


@voterTablesApp.post('/')
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def add(votersTable: VotersTableSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    existing_user = db.query(VotersTable).filter(
        VotersTable.code == votersTable.code,
        VotersTable.municipality_id == votersTable.municipality_id).first()
    if existing_user:
        return {"message": "already created", "user": existing_user}
    try:
        vtrsTblORM = VotersTable(**votersTable.dict())
        db.add(vtrsTblORM)
        db.commit()
        db.refresh(vtrsTblORM)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while adding the voter")
    return {"message": "added successfully", "VotersTable": vtrsTblORM}


@voterTablesApp.get('/', response_model=List[VotersTableSchema])
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def read_all(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    voters = db.query(VotersTable).all()
    return voters


@voterTablesApp.get('/{voter_id}', response_model=VotersTableSchema)
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def read_voter(voter_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    voter = db.query(VotersTable).filter(VotersTable.id == voter_id).first()
    if not voter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voter not found")
    return voter


@voterTablesApp.put('/{voter_id}', response_model=VotersTableSchema)
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def update(voter_id: int, votersTable: VotersTableSchema, db: Session = Depends(get_db),
           current_user: dict = Depends(get_current_user)):
    voter = db.query(VotersTable).filter(VotersTable.id == voter_id).first()
    if not voter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voter not found")

    for key, value in votersTable.dict(exclude_unset=True).items():
        setattr(voter, key, value)

    try:
        db.commit()
        db.refresh(voter)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while updating the voter")

    return voter


@voterTablesApp.delete('/{voter_id}', response_model=dict)
@authorize(role=[UserRole.ADMIN])
def delete(voter_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    voter = db.query(VotersTable).filter(VotersTable.id == voter_id).first()
    if not voter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Voter not found")

    try:
        db.delete(voter)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred while deleting the voter")

    return {"message": "deleted successfully"}