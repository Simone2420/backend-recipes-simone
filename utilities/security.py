from passlib.context import CryptContext
from jose import jwt

# Configuración de Passlib para usar Argon2
# Argon2 es el ganador de la Password Hashing Competition (PHC) y es altamente resistente
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Genera un hash seguro para la contraseña."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)


# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     db: Session = Depends(get_db)
# ) -> Usuario:
#     token = credentials.credentials
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Credenciales de autenticación inválidas",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email_str: str = payload.get("sub")
#         jti: str = payload.get("jti")
        
#         if email_str is None or jti is None:
#             raise credentials_exception
            
#         # Verificar si la sesión fue revocada (Logout)
#         if AuthService.is_token_revoked(db, jti=jti):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="La sesión ha expirado o ha sido cerrada",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
            
#     except jwt.PyJWTError:
#         raise credentials_exception
        
#     user = db.query(Usuario).filter(Usuario.email == email_str).first()
#     if user is None:
#         raise credentials_exception
#     if not user.activo:
#         raise HTTPException(status_code=400, detail="El usuario está inactivo")
        
#     # Añadimos el token jti al objeto user temporalmente si es necesario para logout
#     user.current_jti = jti
#     return user

# def check_permission(permiso_requerido: str):
#     """
#     Dependencia para RBAC. Verifica que el usuario tenga el permiso requerido en sus roles.
#     """
#     def _check(current_user: Usuario = Depends(get_current_user)):
#         # El administrador tiene acceso total por defecto
#         if any(role.nombre == "administrador" for role in current_user.roles):
#             return current_user
            
#         # Extraer todos los códigos de permisos asociados a los roles del usuario
#         permisos_usuario = {
#             permiso.codigo 
#             for role in current_user.roles 
#             for permiso in role.permisos
#         }
        
#         if permiso_requerido not in permisos_usuario:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"Acceso denegado. Se requiere el permiso: {permiso_requerido}"
#             )
            
#         return current_user
#     return _check