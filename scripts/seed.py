#!/usr/bin/env python
# coding=utf-8
import os
import sys

# Agregar la raíz del proyecto al sys.path para permitir importaciones correctas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models import Role, Permission

def seed_roles_and_permissions(db):
    # 1. Definir permisos semilla
    permissions_data = [
        {"name": "view_recipes", "description": "Ver recetas"},
        {"name": "create_recipes", "description": "Crear recetas"},
        {"name": "edit_own_recipes", "description": "Editar tus propias recetas"},
        {"name": "delete_own_recipes", "description": "Eliminar tus propias recetas"},
        {"name": "edit_all_recipes", "description": "Editar cualquier receta"},
        {"name": "delete_all_recipes", "description": "Eliminar cualquier receta"},
        {"name": "manage_users", "description": "Gestionar usuarios"},
        {"name": "manage_roles", "description": "Gestionar roles y permisos"},
        {"name": "view_roles", "description": "Ver roles"},
        {"name": "view_permissions", "description": "Ver permisos"},
        {"name": "manage_permissions", "description": "Gestionar permisos"},
        {"name": "manage_difficulties", "description": "Gestionar dificultades"},
        {"name": "manage_ingredients", "description": "Gestionar ingredientes"},
        {"name": "download_books", "description": "Descargar libros"},
    ]

    # 2. Crear permisos en BD si no existen
    db_permissions = {}
    for perm_data in permissions_data:
        perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not perm:
            perm = Permission(name=perm_data["name"], description=perm_data["description"])
            db.add(perm)
            db.commit()
            db.refresh(perm)
        db_permissions[perm_data["name"]] = perm

    # 3. Definir roles semilla
    roles_data = [
        {
            "name": "usuario",
            "description": "Usuario básico",
            "permissions": ["view_recipes", "create_recipes", "edit_own_recipes", "delete_own_recipes"]
        },
        {
            "name": "usuario_premium",
            "description": "Usuario premium",
            "permissions": ["view_recipes", "create_recipes", "edit_own_recipes", "delete_own_recipes", "download_books"]
        },
        {
            "name": "administrador",
            "description": "Administrador del sistema",
            "permissions": ["view_recipes", "create_recipes", "edit_own_recipes", "delete_own_recipes", "edit_all_recipes", "delete_all_recipes", "manage_users", "manage_roles", "view_roles", "view_permissions", "manage_permissions", "manage_difficulties", "manage_ingredients", "download_books"]
        }
    ]

    # 4. Crear roles y asignar permisos
    for role_data in roles_data:
        role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not role:
            role = Role(name=role_data["name"], description=role_data["description"], is_active=True)
            db.add(role)
            db.commit()
            db.refresh(role)

        # Asignar permisos al rol
        for perm_name in role_data["permissions"]:
            perm_obj = db_permissions.get(perm_name)
            if perm_obj and perm_obj not in role.permissions:
                role.permissions.append(perm_obj)

    db.commit()
    print("✅ Semillas de roles y permisos creadas exitosamente!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_roles_and_permissions(db)
    finally:
        db.close()
