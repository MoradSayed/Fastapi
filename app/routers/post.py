from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/posts", 
    tags= ['Posts']
)

# @router.get('/', response_model= List[schemas.Post])
@router.get('/', response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):
    #sql
    # cursor.execute(""" select * from posts """)
    # posts = cursor.fetchall()

    #sqlalchemy
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()

    return posts


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #sql
    # cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s) returning * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    #sqlalchemy
    new_post = models.Post(owner_id = current_user.id, **post.dict()) # **post.dict() means that u unpack all the incoming inputs from the dictionary of the pydantic model
    db.add(new_post) # add the new post to the table
    db.commit() # commit the changes
    db.refresh(new_post) # save it to the new_post variable 
    return new_post


@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    #sql
    # cursor.execute(""" select * from posts where id = %s """, (id, ))
    # post = cursor.fetchone()

    #sqlalchemy
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id: {id} was not found')
    
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #sql
    # cursor.execute(""" delete from posts where id = %s returning *""", (id, ))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    #sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id: {id} was not found')
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f'not authorized to perform the requested action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #sql
    # cursor.execute(""" update posts set title = %s, content = %s, published = %s where id = %s returning * """, (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    #sqlalchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)

    the_post = post_query.first()

    if the_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id: {id} was not found')
    
    if the_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f'not authorized to perform the requested action')

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
