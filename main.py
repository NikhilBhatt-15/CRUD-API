from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating : Optional[int] = None
    
@app.get("/")
def root():
    return {"message":"Hello API's"}

@app.get("/posts/{id}")
def get_post(id):
    x=""
    if id=="3":
        x="Nikhil"
    else:
        x="Kapil"
    return{"Post-"+x:"Here we are"}


@app.post("/posts")
def create_posts(post:Post):
    print(post)
    return {"new_post":f"title {post.title} content:   {post.content}"}