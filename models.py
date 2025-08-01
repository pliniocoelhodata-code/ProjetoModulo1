from sqlalchemy import Column, Integer, String, Float
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    category = Column(String)
    image = Column(String)
