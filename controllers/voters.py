import logging

from fastapi import HTTPException  # Correct import
from auth.authentications import get_current_user
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from auth.authorizations import authorize
from models.db import get_db
from models.models import Municipality, Voters, UserRole, User
from models.shcemas import UserSchema, VoterSchema
from sqlalchemy.orm import Session

voterApp = APIRouter(prefix="/voters",
                   tags=["voters"])

logger = logging.getLogger(__name__)

@voterApp.post('')
@authorize(role=[UserRole.ADMIN,UserRole.LEAD])
def add(voter: VoterSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    
    # Check if email already exists
    existing_user = db.query(Voters).filter(Voters.dni == voter.dni).first()
    if existing_user:
        return {"message": "already created", "voters": existing_user}
    
    vtrsORM=Voters(**voter.dict())
    vtrsORM.coordinates="0,0"
    vtrsORM.leader_id=current_user.id
    
    try:
        db.add(vtrsORM)
        db.commit()
        db.refresh(vtrsORM)
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"IntegrityError occurred: {ie}")
        raise HTTPException(status_code=400, detail="Voter already exists or data integrity issue.")
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while adding the voter.")
    
    return {"message": "added successfully", "voters": vtrsORM}


@voterApp.get('')
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def get(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    try:
        all_voters=[]
        if current_user.rol==UserRole.ADMIN:
            all_voters=db.query(Voters).all()
        if current_user.rol==UserRole.LEAD:
            leader = db.query(User).filter(User.id == current_user.id).first()
            all_voters = leader.leads  # Get all voters associated with this leader
        
        count = len(all_voters)
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"IntegrityError occurred: {ie}")
        raise HTTPException(status_code=400, detail="Voter already exists or data integrity issue.")
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while adding the voter.")

    return {"message": "added successfully","count": count, "voters": all_voters}


@voterApp.get('/municipality/{municipality_id}')
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def get_voters_by_municipality(municipality_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Use the relationship to access voters tables and their voters
    all_voters = []
    try:
         # Retrieve the municipality, including related voters tables and their voters
        municipality = db.query(Municipality).filter(Municipality.id == municipality_id).first()

        if not municipality:
            raise HTTPException(status_code=404, detail="Municipality not found.")
        
         # Get all voters table IDs associated with the municipality
        voters_table_ids = [voters_table.id for voters_table in municipality.voters_tables]

        if not voters_table_ids:
            return {"message": "No voters tables found for this municipality.", "count": 0, "voters": []}

       # Check the role of the current user
        if current_user.rol == UserRole.ADMIN:
            # Admins have full access
            all_voters = db.query(Voters).filter(Voters.voters_table_id.in_(voters_table_ids)).all()
        elif current_user.rol == UserRole.LEAD:
            
            # Filter voters based on both municipality and the leader's own tables
            all_voters = db.query(Voters).filter(
                Voters.voters_table_id.in_(voters_table_ids),
                Voters.leader_id.in_(current_user.id)
            ).all()
        else:
            raise HTTPException(status_code=403, detail="Access forbidden for this role.")
        

        count = len(all_voters)
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"IntegrityError occurred: {ie}")
        raise HTTPException(status_code=400, detail="Data integrity issue.")
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching voters.")

    return {"message": "retrieved successfully", "count": count, "voters": all_voters}


@voterApp.get('/votersTable/{voter_table_id}')
@authorize(role=[UserRole.ADMIN, UserRole.LEAD])
def get_voters_by_voters_table(voter_table_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    try:
        all_voters = []
        if current_user.rol == UserRole.ADMIN:
            # Admins have full access
            all_voters = db.query(Voters).filter(Voters.voters_table_id == voter_table_id).all()
        elif current_user.rol == UserRole.LEAD:
            all_voters = db.query(Voters).filter(Voters.voters_table_id == voter_table_id,
                                                 Voters.leader_id==current_user.id).all()
        else:
            raise HTTPException(status_code=403, detail="Access forbidden for this role.")

        count = len(all_voters)
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"IntegrityError occurred: {ie}")
        raise HTTPException(status_code=400, detail="Data integrity issue.")
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching voters.")

    return {"message": "retrieved successfully", "count": count, "voters": all_voters}