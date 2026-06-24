#!/usr/bin/env python
# coding=utf-8
import os
import sys
import argparse

# Agregar la raíz del proyecto al sys.path para permitir importaciones correctas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from config.database import SessionLocal
from models import User, Role, Permission
from main import app
from fastapi.routing import APIRoute

# Configuración de colores para la consola
USE_COLOR = sys.stdout.isatty()

def color_text(text, color_code):
    if USE_COLOR:
        return f"\033[{color_code}m{text}\033[0m"
    return text

GREEN = "92"
RED = "91"
YELLOW = "93"
BLUE = "94"
CYAN = "96"
BOLD = "1"

def get_dependant_calls(dependant):
    """Obtiene de forma recursiva todas las funciones de dependencias de un Dependant de FastAPI."""
    calls = []
    if dependant.call:
        calls.append(dependant.call)
    for sub_dep in dependant.dependencies:
        calls.extend(get_dependant_calls(sub_dep))
    return calls

def get_route_requirements(route):
    """Analiza las dependencias de una ruta de FastAPI para determinar sus requerimientos de seguridad."""
    dependants = [route.dependant]
    if hasattr(route, "dependencies") and route.dependencies:
        dependants.extend(route.dependencies)
        
    calls = []
    for dep in dependants:
        calls.extend(get_dependant_calls(dep))
        
    requires_auth = False
    required_permission = None
    
    for call in calls:
        call_name = getattr(call, "__name__", "")
        # Detectar el decorador check_permission (devuelve la función local _check)
        if call_name == "_check" and hasattr(call, "__code__"):
            freevars = call.__code__.co_freevars
            closure = getattr(call, "__closure__", None)
            if closure and "required_permission" in freevars:
                idx = freevars.index("required_permission")
                required_permission = closure[idx].cell_contents
                requires_auth = True
        # Detectar get_current_user directo
        elif call_name == "get_current_user":
            requires_auth = True
            
    return requires_auth, required_permission

def get_all_routes_info():
    """Recorre las rutas de FastAPI y extrae su información detallada."""
    routes_info = []
    
    def process_router(router_or_app, prefix=""):
        for route in router_or_app.routes:
            route_type = type(route).__name__
            if route_type == "_IncludedRouter":
                sub_router = route.original_router
                sub_prefix = prefix + (route.include_context.prefix or "")
                process_router(sub_router, sub_prefix)
            elif route_type == "APIRoute":
                full_path = (prefix + route.path).replace("//", "/")
                # Ignorar rutas de documentación por defecto
                if any(x in full_path for x in ["/openapi.json", "/docs", "/redoc"]):
                    continue
                requires_auth, required_permission = get_route_requirements(route)
                routes_info.append({
                    "path": full_path,
                    "methods": list(route.methods),
                    "endpoint": route.endpoint.__name__,
                    "requires_auth": requires_auth,
                    "required_permission": required_permission
                })
                
    process_router(app)
    # Ordenar rutas por path y luego por métodos
    routes_info.sort(key=lambda x: (x["path"], x["methods"]))
    return routes_info

def check_user_access(user, route_info):
    """Determina si un usuario tiene acceso a una ruta específica."""
    if not user.is_active:
        return False, "Usuario inactivo"
        
    requires_auth = route_info["requires_auth"]
    required_permission = route_info["required_permission"]
    
    # 1. Rutas públicas
    if not requires_auth:
        return True, "Público"
        
    # 2. Rutas que solo requieren autenticación
    if requires_auth and not required_permission:
        return True, "Autenticado"
        
    # 3. Rutas que requieren un permiso específico
    # El rol de Administrador tiene acceso completo a todo por defecto
    is_admin = any(role.name.lower().startswith("admin") for role in user.roles)
    if is_admin:
        return True, f"Admin (Permiso {required_permission} concedido implícitamente)"
        
    # Obtener todos los nombres de los permisos asignados a los roles del usuario
    user_permissions = {
        perm.name 
        for role in user.roles 
        for perm in role.permissions
    }
    
    if required_permission in user_permissions:
        return True, f"Permiso concedido ({required_permission})"
        
    return False, f"Falta permiso: {required_permission}"

def display_roles_summary(db: Session):
    """Muestra un resumen de los roles y permisos registrados en la base de datos."""
    roles = db.query(Role).all()
    print("\n" + color_text("=== RESUMEN DE ROLES Y PERMISOS EN BASE DE DATOS ===", BOLD))
    if not roles:
        print("No se encontraron roles configurados.")
        return
        
    for role in roles:
        status_text = color_text("Activo", GREEN) if role.is_active else color_text("Inactivo", RED)
        print(f"\nRol: {color_text(role.name, BOLD)} ({status_text})")
        print(f"Descripción: {role.description or 'Sin descripción'}")
        permissions = [p.name for p in role.permissions]
        if permissions:
            print(f"Permisos ({len(permissions)}): {', '.join(sorted(permissions))}")
        else:
            print("Permisos: Ninguno")
    print("-" * 60)

def display_routes_summary(routes_info):
    """Muestra todas las rutas disponibles y sus requerimientos de seguridad."""
    print("\n" + color_text("=== RUTAS DE LA API Y REQUERIMIENTOS ===", BOLD))
    print(f"{'MÉTODO':<8} | {'RUTA':<50} | {'REQUERIMIENTO':<40}")
    print("-" * 105)
    
    for r in routes_info:
        methods = ", ".join(r["methods"])
        
        # Determinar texto de requerimiento
        if r["required_permission"]:
            req_text = color_text(f"Permiso: {r['required_permission']}", YELLOW)
        elif r["requires_auth"]:
            req_text = color_text("Autenticación básica", BLUE)
        else:
            req_text = color_text("Público (Libre)", GREEN)
            
        print(f"{methods:<8} | {r['path']:<50} | {req_text:<40}")
    print("-" * 105)

def display_user_permissions(db: Session, routes_info, filter_email=None):
    """Analiza y muestra el acceso detallado a las rutas para los usuarios."""
    query = db.query(User)
    if filter_email:
        query = query.filter(User.email == filter_email)
        
    users = query.all()
    if not users:
        if filter_email:
            print(color_text(f"\n❌ No se encontró ningún usuario con el email: {filter_email}", RED))
        else:
            print(color_text("\n❌ No se encontraron usuarios en la base de datos.", RED))
        return
        
    for user in users:
        print("\n" + "=" * 80)
        print(f"Usuario: {color_text(user.username, BOLD)} | Email: {color_text(user.email, BOLD)}")
        status_text = color_text("ACTIVO", GREEN) if user.is_active else color_text("INACTIVO", RED)
        user_roles = [r.name for r in user.roles]
        roles_str = ", ".join(user_roles) if user_roles else "Ninguno"
        print(f"Estado: {status_text} | Roles: [{color_text(roles_str, BLUE)}]")
        
        # Extraer permisos individuales del usuario para mostrar
        if any(r.name.lower().startswith("admin") for r in user.roles):
            print(f"Permisos efectivos: {color_text('Acceso total (Administrador)', GREEN)}")
        else:
            user_perms = sorted(list({p.name for r in user.roles for p in r.permissions}))
            perms_str = ", ".join(user_perms) if user_perms else "Ninguno"
            print(f"Permisos asignados: {perms_str}")
            
        print("-" * 80)
        print(f"{'ACCESO':<8} | {'MÉTODO':<8} | {'RUTA':<45} | {'DETALLE/MOTIVO':<35}")
        print("-" * 80)
        
        allowed_count = 0
        total_count = len(routes_info)
        
        for r in routes_info:
            has_access, reason = check_user_access(user, r)
            methods = ", ".join(r["methods"])
            
            if has_access:
                allowed_count += 1
                access_indicator = color_text("  [✓]  ", GREEN)
                reason_colored = color_text(reason, GREEN)
            else:
                access_indicator = color_text("  [✗]  ", RED)
                reason_colored = color_text(reason, RED)
                
            print(f"{access_indicator:<8} | {methods:<8} | {r['path']:<45} | {reason_colored:<35}")
            
        print("-" * 80)
        percentage = (allowed_count / total_count) * 100 if total_count > 0 else 0
        print(f"Resumen de acceso: {color_text(f'{allowed_count}/{total_count} rutas accesibles ({percentage:.1f}%)', BOLD)}")
        
def main_cli():
    parser = argparse.ArgumentParser(
        description="Script de utilidad para auditar qué permisos y accesos tienen los usuarios sobre las rutas de la API de Recetas."
    )
    parser.add_argument(
        "--routes", action="store_true", help="Muestra el listado completo de rutas de la API y sus requerimientos de seguridad."
    )
    parser.add_argument(
        "--roles", action="store_true", help="Muestra un resumen de los roles y permisos creados en la base de datos."
    )
    parser.add_argument(
        "--user", type=str, help="Filtra la auditoría de acceso para un usuario específico por su dirección de email."
    )
    
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        routes_info = get_all_routes_info()
        
        # Si no se pasa ninguna opción, mostramos la auditoría de todos los usuarios
        if not (args.routes or args.roles or args.user):
            display_roles_summary(db)
            display_routes_summary(routes_info)
            display_user_permissions(db, routes_info)
        else:
            if args.roles:
                display_roles_summary(db)
            if args.routes:
                display_routes_summary(routes_info)
            if args.user or (not args.roles and not args.routes):
                display_user_permissions(db, routes_info, filter_email=args.user)
                
    except Exception as e:
        print(color_text(f"Ocurrió un error al ejecutar el script: {e}", RED))
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main_cli()
