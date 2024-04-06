
from datetime import datetime
from fastapi import FastAPI, HTTPException,  Depends,status,APIRouter
import schemas, models, services
from middleware import JWTMiddleware

from database import SessionLocal
from sqlalchemy.orm import Session
from typing import List 
from database import get_db

app = FastAPI()
# Add middleware to the app
app.add_middleware(JWTMiddleware)



# This will be use for user registration
@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user_data = services.create_user(db, user)
        return user_data  # Return the dictionary containing both user and access_token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# This will be use for user login
@app.post("/user_login/", response_model=schemas.UserResponse)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = services.authenticate_user(email, password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )  
      
    return user


# API endpoint to fetch user's name by email
# @app.get("/user/name/")
# def get_user_name(token: str, db: Session = Depends(get_db)):
#     user_name = services.get_user_name_by_email(db,token)
#     if user_name is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"user_name": user_name}

# def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     email = services.get_email_from_token(token)
#     if email is None:
#         raise HTTPException(status_code=401, detail="Invalid token")
    
#     user_info = services.get_user_info_by_email(db, email)
#     if user_info is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return {"user_info": user_info}






































# This will be use for updeting a specific user informatin  
@app.put("/update-account/{user_id}")
def update_account(user_id: int, updated_info: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = services.update_user(db, user_id, updated_info)
    if updated_user:
        return updated_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

# This will be use for delete a specific user
@app.delete("/delete-account/")
def delete_account(email: str, password: str, db: Session = Depends(get_db)):
    if services.delete_user(db, email, password):
        return {"message": "Account deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete account. Check email and password.",
        )

# Define an APIRouter instance
router = APIRouter()   

# Create an event 
@router.post("/events/", response_model=schemas.EventSchema)
def create_event(event: schemas.EventSchema, db: Session = Depends(get_db)):
    return services.launch_event(db, event)

# Get all event details  
@router.get("/events/")
def get_all_events(db: Session = Depends(get_db)):
    return db.query(models.EventPublishModel).all()

# Get all event details of a specific date 
# Need to modify it for only date input
@router.get("/events/date/", response_model=List[schemas.EventSchema])
def get_events_by_date_endpoint(date: datetime, db: Session = Depends(get_db)):
    return services.get_events_by_date(db, date)

# Get all event details of a specific location
@router.get("/events/location/", response_model=List[schemas.EventSchema])
def get_events_by_location_endpoint(location: str, db: Session = Depends(get_db)):
    events = services.get_events_by_location(db, location)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for the specified location.")
    return events

# Endpoint to modify an event details
@router.put("/events/{event_id}")
def modify_event_endpoint(event_id: int, event_data: schemas.EventSchema, db: Session = Depends(get_db)):
    modified = services.modify_event(db, event_id, event_data)
    if not modified:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event modified successfully"}

# Endpoint to delete an event
@router.delete("/events/{event_id}")
def delete_event_endpoint(event_id: int, db: Session = Depends(get_db)):
    deleted = services.delete_event(db, event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}


# Include the router in the main application
app.include_router(router, prefix="/api")





# API endpoint to fetch user's pending and accepted events by email
@app.get("/user_events/", response_model=schemas.UserEventList)
def get_user_events(email: str, db: Session = Depends(get_db)):
    user_events = services.get_user_events_by_email(db, email)
    if user_events is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserEventList(user_events=user_events)

# API endpoint to fetch event details by event id 
@app.get("/events/{event_id}", response_model=schemas.EventSchema)
def read_event(event_id: int, db: Session = Depends(get_db)):
    event =services.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# # API endpoint to accept an event
# @app.post("/events/{event_id}/accept", response_model=schemas.UserEvent)
# def accept_event_api(event_id: int, current_user: models.UserModel = Depends(middleware.get_current_user), db: Session = Depends(get_db)):
#     return services.accept_event(db, current_user.id, event_id)

# # API endpoint to reject an event
# @app.post("/events/{event_id}/reject")
# def reject_event_api(event_id: int, current_user: models.UserModel = Depends(middleware.get_current_user), db: Session = Depends(get_db)):
#     services.reject_event(db, current_user.id, event_id)
#     return {"message": "Event rejected successfully"}

#-------------------------------------------------------------------------------------------------------------------------------------