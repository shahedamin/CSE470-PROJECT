from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import  relationship
from database import Base,engine



class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))
    username = Column(String(20))
    gender = Column(String(10))
    phone = Column(String(15))
    email = Column(String(50), unique=True, index=True)
    password_hash = Column(String(100))
    
    # Additional fields for volunteer
    age = Column(Integer) # It will be date of birth in the second sprint
    blood_group = Column(String(5))
    # priority_level = Column(String(20))
    # Also there will be a field for profile picture

    
    events = relationship("EventPublishModel", back_populates="author")

class EventPublishModel(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    description = Column(String(500))
    author_id = Column(Integer, ForeignKey('users.id'))
    location = Column(String(30))
    date = Column(DateTime) # It will be only date later
    time = Column(DateTime)  # It will be only time later
    organizer_company = Column(String(50))

    author = relationship("UserModel", back_populates="events")
    # later there will be added image field 



Base.metadata.create_all(bind=engine)

