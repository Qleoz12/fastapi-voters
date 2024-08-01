import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import Municipality, UserRole
from models.db import get_db
from auth.authorizations import authorize
from auth.authentications import get_current_user
from models.shcemas import MunicipalitySchema

municipalityApp = APIRouter(prefix="/municipalities", tags=["municipalities"])

logger = logging.getLogger(__name__)

@municipalityApp.post('', response_model=MunicipalitySchema)
@authorize(role=[UserRole.ADMIN])
def add_municipality(municipality: MunicipalitySchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    municipality_orm = Municipality(**municipality.dict())
    
    try:
        db.add(municipality_orm)
        db.commit()
        db.refresh(municipality_orm)
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"IntegrityError occurred: {ie}")
        raise HTTPException(status_code=400, detail="Municipality already exists or data integrity issue.")
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while adding the municipality.")
    
    return municipality_orm


@municipalityApp.get('', response_model=List[MunicipalitySchema])
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def get_municipalities(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        municipalities = db.query(Municipality).all()
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching municipalities.")
    
    return municipalities


@municipalityApp.get('/{municipality_id}', response_model=MunicipalitySchema)
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def get_municipality(municipality_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    municipality = db.query(Municipality).filter(Municipality.id == municipality_id).first()
    if not municipality:
        raise HTTPException(status_code=404, detail="Municipality not found.")
    return municipality


@municipalityApp.put('/{municipality_id}', response_model=MunicipalitySchema)
@authorize(role=[UserRole.ADMIN])
def update_municipality(municipality_id: int, municipality: MunicipalitySchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    municipality_orm = db.query(Municipality).filter(Municipality.id == municipality_id).first()
    if not municipality_orm:
        raise HTTPException(status_code=404, detail="Municipality not found.")
    
    for key, value in municipality.dict(exclude_unset=True).items():
        setattr(municipality_orm, key, value)
    
    try:
        db.commit()
        db.refresh(municipality_orm)
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while updating the municipality.")
    
    return municipality_orm


@municipalityApp.delete('/{municipality_id}')
@authorize(role=[UserRole.ADMIN])
def delete_municipality(municipality_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    municipality_orm = db.query(Municipality).filter(Municipality.id == municipality_id).first()
    if not municipality_orm:
        raise HTTPException(status_code=404, detail="Municipality not found.")
    
    try:
        db.delete(municipality_orm)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while deleting the municipality.")
    
    return {"message": "Municipality deleted successfully."}
