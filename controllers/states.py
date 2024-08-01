import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import State, UserRole

from models.db import get_db
from auth.authorizations import authorize
from auth.authentications import get_current_user
from models.shcemas import StateSchema

stateApp = APIRouter(prefix="/states", tags=["states"])

logger = logging.getLogger(__name__)

@stateApp.post('', response_model=StateSchema)
@authorize(role=[UserRole.ADMIN])
def add_state(state: StateSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    state_orm = State(**state.dict())
    
    try:
        db.add(state_orm)
        db.commit()
        db.refresh(state_orm)
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"IntegrityError occurred: {ie}")
        raise HTTPException(status_code=400, detail="State already exists or data integrity issue.")
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while adding the state.")
    
    return state_orm


@stateApp.get('', response_model=List[StateSchema])
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def get_states(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        states = db.query(State).all()
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching states.")
    
    return states


@stateApp.get('/{state_id}', response_model=StateSchema)
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def get_state(state_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    state = db.query(State).filter(State.id == state_id).first()
    if not state:
        raise HTTPException(status_code=404, detail="State not found.")
    return state


@stateApp.put('/{state_id}', response_model=StateSchema)
@authorize(role=[UserRole.ADMIN])
def update_state(state_id: int, state: StateSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    state_orm = db.query(State).filter(State.id == state_id).first()
    if not state_orm:
        raise HTTPException(status_code=404, detail="State not found.")
    
    for key, value in state.dict(exclude_unset=True).items():
        setattr(state_orm, key, value)
    
    try:
        db.commit()
        db.refresh(state_orm)
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while updating the state.")
    
    return state_orm


@stateApp.delete('/{state_id}')
@authorize(role=[UserRole.ADMIN])
def delete_state(state_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    state_orm = db.query(State).filter(State.id == state_id).first()
    if not state_orm:
        raise HTTPException(status_code=404, detail="State not found.")
    
    try:
        db.delete(state_orm)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while deleting the state.")
    
    return {"message": "State deleted successfully."}
