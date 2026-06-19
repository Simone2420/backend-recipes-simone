import os
import sys

# Agregar la raíz del proyecto al sys.path para permitir importaciones correctas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from config.database import SessionLocal

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
    permission_ids = {}
    for perm_data in permissions_data:
        res = db.execute(
            text("SELECT id FROM permissions WHERE name = :name"),
            {"name": perm_data["name"]}
        ).fetchone()
        
        if not res:
            db.execute(
                text("INSERT INTO permissions (name, description, created_at, updated_at) VALUES (:name, :description, NOW(), NOW())"),
                {"name": perm_data["name"], "description": perm_data["description"]}
            )
            # Obtener el id insertado
            res = db.execute(
                text("SELECT id FROM permissions WHERE name = :name"),
                {"name": perm_data["name"]}
            ).fetchone()
            
        permission_ids[perm_data["name"]] = res[0]

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
        role_res = db.execute(
            text("SELECT id FROM roles WHERE name = :name"),
            {"name": role_data["name"]}
        ).fetchone()
        
        if not role_res:
            db.execute(
                text("INSERT INTO roles (name, description, is_active, created_at, updated_at) VALUES (:name, :description, 1, NOW(), NOW())"),
                {"name": role_data["name"], "description": role_data["description"]}
            )
            role_res = db.execute(
                text("SELECT id FROM roles WHERE name = :name"),
                {"name": role_data["name"]}
            ).fetchone()

        role_id = role_res[0]

        # Asignar permisos al rol
        for perm_name in role_data["permissions"]:
            perm_id = permission_ids[perm_name]
            # Verificar si la relación ya existe
            existing = db.execute(
                text("SELECT id FROM role_permissions WHERE role_id = :role_id AND permission_id = :perm_id"),
                {"role_id": role_id, "perm_id": perm_id}
            ).fetchone()
            
            if not existing:
                db.execute(
                    text("INSERT INTO role_permissions (role_id, permission_id, created_at, updated_at) VALUES (:role_id, :perm_id, NOW(), NOW())"),
                    {"role_id": role_id, "perm_id": perm_id}
                )

    db.commit()
    print("✅ Semillas de roles y permisos creadas exitosamente!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_roles_and_permissions(db)
    finally:
        db.close()
