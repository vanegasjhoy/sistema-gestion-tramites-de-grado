from fastapi import Header, HTTPException
from app.auth import verificar_token

# Roles válidos en el sistema: 'estudiante', 'coordinacion', 'admin'


def get_usuario_actual(authorization: str = Header(...)):
    """
    Verifica el token JWT. Permite acceso a cualquier rol autenticado.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    token = authorization.replace("Bearer ", "")
    payload = verificar_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    return payload


def solo_admin(authorization: str = Header(...)):
    """
    Solo permite acceso al rol 'admin'.
    """
    payload = get_usuario_actual(authorization)

    if payload.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol admin")

    return payload


def coordinacion_o_admin(authorization: str = Header(...)):
    """
    Permite acceso a 'coordinacion' y 'admin'.
    Usado para rutas donde coordinación gestiona solicitudes de estudiantes.
    """
    payload = get_usuario_actual(authorization)

    if payload.get("rol") not in ["coordinacion", "admin"]:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol coordinacion o admin")

    return payload
