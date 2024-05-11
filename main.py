from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from dataBase import Engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=Engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MySchoolClasses(BaseModel):
    name: str = Field(min_lengh=1)
    schoolName: str = Field(min_length=1, max_length=50)
    teacherName: str = Field(min_length=1, max_length=50)
    studentCount: int = Field(gt=1, lt=100)

MyClasses = []

@app.get("/read-list")
def read_school_class(db: Session = Depends(get_db)):
    return db.query(models.MySchoolClasses).all()

@app.post("/add-list")
def create_school_class(mySchoolClass: MySchoolClasses, db: Session = Depends(get_db)) :
    school_class = models.MySchoolClasses()
    school_class.name = mySchoolClass.name
    school_class.schoolName = mySchoolClass.schoolName
    school_class.studentCount = mySchoolClass.studentCount
    school_class.teacherName = mySchoolClass.teacherName

    db.add(school_class)
    db.commit()

@app.post("/{schoolclass_id}")
def schoolClassUpdate(schoolclass_id: int, mySchoolClass: MySchoolClasses, db: Session = Depends(get_db)) :
    school_class = db.query(models.MySchoolClasses).filter(models.MySchoolClasses.id == schoolclass_id).first()
    
    if school_class is None:
        print("The school class is not exsist !")

    school_class.name = mySchoolClass.name
    school_class.schoolName = mySchoolClass.schoolName
    school_class.studentCount = mySchoolClass.studentCount
    school_class.teacherName = mySchoolClass.teacherName

    db.add(school_class)
    db.commit()

    return mySchoolClass

@app.post("/delete/{schoolclass_id}")
def delete_school_class(schoolclass_id: int, db: Session = Depends(get_db)) :
    school_class = db.query(models.MySchoolClasses).filter(models.MySchoolClasses.id == schoolclass_id).first()
    
    if school_class is None:
        print("The school class is not exsist !")

    db.query(models.MySchoolClasses).filter(models.MySchoolClasses.id == schoolclass_id).delete()
    db.commit()

    return {"delete record" : school_class}

# ----------------------------------------------------------------------------------------

# Hello World
@app.get("/")
def say_hello():
    return {"Hello" : "World"}

myList = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Show Name
@app.get("/about/{name}")
def about(name : int) :
    return {"date" : name}

@app.get("/add-get/{number:int}")
def addToList(number : int) :
    myList.append(number)
    return myList

# Show My List
@app.get("/myList/")
def getList() :
    return {"myList" : myList}

# post
@app.post("/add-post/")
def addToList(number : int) :
    myList.append(number)
    return myList

# put
@app.put("/update/")
def updateList(index:int, newNumber:int):
    myList[index] = newNumber
    return {"updateList" : myList}

# delete
@app.delete("/delete/")
def deleteList(number:int):
    myList.remove(number)
    return {"newList" : myList}
    