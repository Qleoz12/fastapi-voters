from controllers import municipality, security, states, users, voters, votersTables
from fastapi import FastAPI, Depends, Body
import uvicorn
import sys
import os
import logging

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from models.db import engine, Base
from models.models import User

# Create tables in the database
# Create all tables in the database. This is equivalent to "Create Table" statements in raw SQL.
from models.preload_data import load_users, load_states_and_municipalities

Base.metadata.create_all(bind=engine)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath('.'))

app = FastAPI()

# Include routes from 'users' module
app.include_router(users.usersApp)
app.include_router(voters.voterApp)
app.include_router(votersTables.voterTablesApp)
app.include_router(security.securitysApp)
app.include_router(municipality.municipalityApp)
app.include_router(states.stateApp)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Home page"}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    load_states_and_municipalities()
    load_users()


if __name__ == "__main__":
    logger.info("Starting the application")
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    except Exception as e:
        logger.error(f"An error occurred while running the application: {e}")
