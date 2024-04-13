from typing import Optional
from fastapi import Body, FastAPI, Response , status , HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    
x=0    

while True:
    
    if x>10:
        break
    try:
        conn = psycopg2.connect(host='localhost',database='postproject',user='postgres',password='#luma1765',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection succesful")
        break
    except Exception as error:
        print("Conneting to Datbase failed")
        print("Error: ",error)
        time.sleep(3)
        x+=1


my_posts = [{"id":1,"title":"My first posts","content":"lets see how things work out here"},
            {"id":2,"title":"WE UPP","content":"We really going upp"}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
    return None
    
@app.get("/")
def root():
    return {"message":"Hello API's"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return posts



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO post (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published),)
    new_post = cursor.fetchone()
    conn.commit()
    return new_post

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM post WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    else:
        return post
    
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM post WHERE id = %s returning *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE post SET title=%s, content= %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=404,detail=f"post with id {id} doesn't exist")
    else:
        return post
