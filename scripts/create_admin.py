#!/usr/bin/env python
# coding=utf-8
import os
import sys

# Agregar la raíz del proyecto al sys.path para permitir importaciones correctas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from passlib.context import CryptContext
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_admin():
    from models import User, Role
    db = SessionLocal()
    try:
        # 1. Buscar el rol de administrador
        role = db.query(Role).filter(Role.name == "administrador").first()
        
        if not role:
            print("❌ El rol de 'administrador' no existe. Por favor ejecuta primero: python scripts/seed.py")
            return
            
        # 2. Leer las credenciales desde variables de entorno
        admin_email = os.getenv("SEED_ADMIN_EMAIL")
        admin_pw = os.getenv("SEED_ADMIN_PASSWORD")
        
        # 3. Verificar si el usuario administrador ya existe
        admin_user = db.query(User).filter(User.email == admin_email).first()
        
        if not admin_user:
            hashed_pw = get_password_hash(admin_pw)
            new_admin = User(
                username="admin",
                email=admin_email,
                password=hashed_pw,
                is_active=True
            )
            # Asociar rol administrador
            new_admin.roles.append(role)
            
            db.add(new_admin)
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
