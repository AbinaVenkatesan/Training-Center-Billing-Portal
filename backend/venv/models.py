from sqlalchemy import Column, Integer, String
from database import Base

# COURSE TABLE
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    fee = Column(Integer)



class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    course_id = Column(Integer)
    amount = Column(Integer)
    status = Column(String)  # paid / pending