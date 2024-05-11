from sqlalchemy import Column, Integer, String
from dataBase import Base

class MySchoolClasses(Base):
    __tablename__ = "MySchoolClass"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    schoolName = Column(String, nullable=False)
    teacherName = Column(String, nullable=False)
    studentCount = Column(Integer, nullable=False)