from typing import Optional
from fastapi import Body, FastAPI, Response , status , HTTPException
from pydantic import BaseModel
from random import randrange
app = FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    rating : Optional[int] = None
    
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
    return my_posts



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.model_dump()
    post_dict["id"]= randrange(1,1000000000)
    my_posts.append(post_dict)
    return post_dict

@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    else:
        return post
    
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    for p in my_posts:
        if(p["id"]==id):
            my_posts.remove(p)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} was not found")

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    i=0
    for p in my_posts:
        if p["id"]==id:
            my_posts[i]['title']=post.title
            my_posts[i]['content']=post.content
            my_posts[i]['published']=post.published
            my_posts[i]['rating']=post.rating
            return {"updated post":my_posts[i]}
        i+=1
    raise HTTPException(status_code=404,detail=f"post with id {id} doesn't exist")
        