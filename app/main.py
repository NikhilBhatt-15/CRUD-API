from typing import Optional,List
from fastapi import Body, FastAPI, Response , status , HTTPException,Depends,APIRouter
from pydantic import BaseModel
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,utils
from .import schemas
from .database import SessionLocal, engine,get_db
from .Routers import post,user,auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


    


while True:
    
    
    try:
        conn = psycopg2.connect(host='localhost',database='postproject',user='postgres',password='#luma1765',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection succesful")
        break
    except Exception as error:
        print("Conneting to Datbase failed")
        print("Error: ",error)
        time.sleep(3)
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/sqlalchemy")
def test_post(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all
    return{"Data":posts}

@app.get("/")
def root():
    return {"message":"Hello API's"}





        