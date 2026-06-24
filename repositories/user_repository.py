from sqlalchemy.orm import Session
from models import User
from schemas.auth import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user: UserCreate) -> User:
        from models import Role
        new_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
        )
        # Asignar rol de usuario por defecto
        default_role = self.db.query(Role).filter(Role.name == "usuario").first()
        if default_role:
            new_user.roles.append(default_role)
            
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, db_user: User, user_update: UserUpdate) -> User:
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
        
    def delete_user(self, db_user: User) -> User:
        db_user.is_active = False
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()