from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from repositories.comment_repository import CommentRepository
from models.auth import User

class CommentController:
    @staticmethod
    def create_comment(
        comment_create: CommentCreate, 
        current_user: User, 
        db: Session
    ) -> CommentResponse:
        repo = CommentRepository(db)
        comment = repo.create_comment(comment_create, current_user.id)
        return CommentResponse.model_validate(comment)
    
    @staticmethod
    def get_comment(comment_id: int, db: Session) -> CommentResponse:
        repo = CommentRepository(db)
        comment = repo.get_comment_by_id(comment_id)
        if not comment or not comment.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return CommentResponse.model_validate(comment)
    
    @staticmethod
    def get_comments_by_recipe(recipe_id: int, db: Session) -> list[CommentResponse]:
        repo = CommentRepository(db)
        comments = repo.get_comments_by_recipe(recipe_id)
        return [CommentResponse.model_validate(comment) for comment in comments]
    
    @staticmethod
    def update_comment(
        comment_id: int, 
        comment_update: CommentUpdate, 
        current_user: User, 
        db: Session
    ) -> CommentResponse:
        repo = CommentRepository(db)
        comment = repo.get_comment_by_id(comment_id)
        if not comment or not comment.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        
        is_admin = any(role.name.lower() == "admin" for role in current_user.roles)
        if comment.user_id != current_user.id and not is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")
        
        updated_comment = repo.update_comment(comment, comment_update)
        return CommentResponse.model_validate(updated_comment)
    
    @staticmethod
    def delete_comment(
        comment_id: int, 
        current_user: User, 
        db: Session
    ) -> CommentResponse:
        repo = CommentRepository(db)
        comment = repo.get_comment_by_id(comment_id)
        if not comment or not comment.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        
        is_admin = any(role.name.lower() == "admin" for role in current_user.roles)
        if comment.user_id != current_user.id and not is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
        
        deleted_comment = repo.delete_comment(comment)
        return CommentResponse.model_validate(deleted_comment)

