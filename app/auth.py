from jose import jwt
import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "clave_secreta_cambiar_en_produccion")
EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", 2))


# ===== CONTRASEÑA =====

def encriptar_contrasena(contrasena: str) -> str:
    """Encripta la contraseña con bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contrasena.encode("utf-8"), salt).decode("utf-8")


def verificar_contrasena(contrasena: str, hash: str) -> bool:
    """Verifica si la contraseña coincide con el hash"""
    return bcrypt.checkpw(contrasena.encode("utf-8"), hash.encode("utf-8"))


# ===== JWT =====

# DESPUÉS ✅
def crear_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=EXPIRES_HOURS)
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    # Asegurar que siempre retorne string
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token


def verificar_token(token: str) -> dict | None:
    """Verifica el JWT y retorna el payload o None si es inválido"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido
