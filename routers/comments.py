
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.comment_controller import CommentController
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from utilities.security import get_current_user
from models.auth import User

router = APIRouter()

@router.post("/", response_model=CommentResponse, status_code=201)
def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: CommentController = Depends()):
    return controller.create_comment(comment, current_user, db)

@router.get("/recipe/{recipe_id}", response_model=list[CommentResponse])
def get_comments_by_recipe(recipe_id: int, db: Session = Depends(get_db), controller: CommentController = Depends()):
    return controller.get_comments_by_recipe(recipe_id, db)

@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db), controller: CommentController = Depends()):
    return controller.get_comment(comment_id, db)

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment: CommentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: CommentController = Depends()):
    return controller.update_comment(comment_id, comment, current_user, db)

@router.delete("/{comment_id}", response_model=CommentResponse)
def delete_comment(comment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), controller: CommentController = Depends()):
    return controller.delete_comment(comment_id, current_user, db)

