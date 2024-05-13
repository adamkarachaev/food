from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DishDB(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
