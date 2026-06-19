import os
import sys

# Agregar la raíz del proyecto al sys.path para permitir importaciones correctas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from config.database import SessionLocal
from passlib.context import CryptContext
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_admin():
    db = SessionLocal()
    try:
        # 1. Buscar el rol de administrador
        role = db.execute(
            text("SELECT id FROM roles WHERE name = 'administrador'")
        ).fetchone()
        
        if not role:
            print("❌ El rol de 'administrador' no existe. Por favor ejecuta primero: python scripts/seed.py")
            return
            
        role_id = role[0]
        
        # 2. Leer las credenciales desde variables de entorno
        admin_email = os.getenv("SEED_ADMIN_EMAIL")
        admin_pw = os.getenv("SEED_ADMIN_PASSWORD")
        
        # 3. Verificar si el usuario administrador ya existe
        admin_user = db.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": admin_email}
        ).fetchone()
        
        if not admin_user:
            hashed_pw = get_password_hash(admin_pw)
            db.execute(
                text("INSERT INTO users (username, email, password, is_active, created_at, updated_at) VALUES ('admin', :email, :password, 1, NOW(), NOW())"),
                {"email": admin_email, "password": hashed_pw}
            )
            
            admin_user = db.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": admin_email}
            ).fetchone()
            
            user_id = admin_user[0]
            
            # Asociar rol administrador
            db.execute(
                text("INSERT INTO user_roles (user_id, role_id, created_at, updated_at) VALUES (:user_id, :role_id, NOW(), NOW())"),
                {"user_id": user_id, "role_id": role_id}
            )
            db.commit()
            print(f"✅ Usuario administrador creado exitosamente!")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Contraseña: [Configurada en .env]")
        else:
            print("ℹ️ El usuario administrador ya existe.")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
