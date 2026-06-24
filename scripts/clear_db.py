#!/usr/bin/env python
# coding=utf-8
import os
import sys
import argparse

# Agregar la raíz del proyecto al sys.path para permitir importaciones correctas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base
# Importar todos los modelos para registrarlos en el Base.metadata
from models import (
    User, Role, UserRole, Permission, RolePermission, Session, Audit,
    Recipe, Difficulty, RecipeInfo, RecipeRating, RecipeImage,
    Ingredient, IngredientImage, RecipeIngredient, Comment, Step, StepImage
)

def clear_database(force=False):
    if not force:
        print("⚠️  " + "\033[91m\033[1m" + "¡ATENCIÓN!" + "\033[0m" + " Esto eliminará permanentemente todas las tablas y datos de la base de datos.")
        confirm = input("¿Estás completamente seguro de que deseas continuar? [y/N]: ").strip().lower()
        if confirm != 'y':
            print("❌ Operación cancelada por el usuario.")
            return

    print("🔄 Borrando todas las tablas de la base de datos...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️  Creando tablas vacías...")
    Base.metadata.create_all(bind=engine)
    
    print("\033[92m✅ Base de datos limpiada y restablecida exitosamente.\033[0m")
    print("💡 Puedes ejecutar 'python scripts/seed.py' para repoblar la base de datos con los datos semilla.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para limpiar y recrear la base de datos.")
    parser.add_argument("-y", "--force", action="store_true", help="Omitir la confirmación interactiva de borrado.")
    args = parser.parse_args()
    
    clear_database(force=args.force)
