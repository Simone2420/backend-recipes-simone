from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate, CommentUpdate

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_comment_by_id(self, comment_id: int) -> Comment:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()
        
    def get_comments_by_recipe(self, recipe_id: int) -> list[Comment]:
        return self.db.query(Comment).filter(Comment.recipe_id == recipe_id, Comment.is_active == True).all()
        
    def create_comment(self, comment: CommentCreate, user_id: int) -> Comment:
        db_comment = Comment(
            recipe_id=comment.recipe_id,
            user_id=user_id,
            title=comment.title,
            comment=comment.comment
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment
        
    def update_comment(self, db_comment: Comment, comment_update: CommentUpdate) -> Comment:
        update_data = comment_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_comment, key, value)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment
        
    def delete_comment(self, db_comment: Comment) -> Comment:
        db_comment.is_active = False
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment
