from typing import Optional,List
from fastapi import Body, FastAPI, Response , status , HTTPException,Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .import schemas
from .database import SessionLocal, engine,get_db

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
        


# my_posts = [{"id":1,"title":"My first posts","content":"lets see how things work out here"},
#             {"id":2,"title":"WE UPP","content":"We really going upp"}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        
#     return None


@app.get("/sqlalchemy")
def test_post(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all
    return{"Data":posts}

@app.get("/")
def root():
    return {"message":"Hello API's"}


@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts



@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published),)
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).get(id)
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    else:
        return post
    
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post= db.query(models.Post).filter(models.Post.id==id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")
    deleted_post.delete(synchronize_session=False)
    db.commit()

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content= %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id==id)
    if updated_post == None:
        raise HTTPException(status_code=404,detail=f"post with id {id} doesn't exist")
    else:
        updated_post.update(post.model_dump())
        db.commit()
        return updated_post.first()
