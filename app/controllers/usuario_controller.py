import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.usuario_model import Usuario, UsuarioLogin
from app.auth import encriptar_contrasena, verificar_contrasena, crear_token
from app.services.email_service import notif_usuario_creado, notif_usuario_eliminado
import threading


class UsuarioController:

    def create_usuario(self, data: Usuario):
        """Crear un nuevo usuario (registro)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            contrasena_hash = encriptar_contrasena(data.contrasena)

            cursor.execute(
                """INSERT INTO usuario
                (correo, contrasena, rol, id_estudiante)
                VALUES (%s,%s,%s,%s)""",
                (
                    data.correo,
                    contrasena_hash,
                    data.rol,
                    data.id_estudiante
                )
            )

            conn.commit()

            threading.Thread(
                target=notif_usuario_creado,
                args=(data.correo, data.correo, data.rol),
                daemon=True
            ).start()

            return {"resultado": "Usuario creado correctamente"}

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def login(self, data: UsuarioLogin):
        """Login: verifica credenciales y retorna JWT"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT id_usuario, correo, contrasena, rol, id_estudiante
                FROM usuario
                WHERE correo=%s AND active=TRUE""",
                (data.correo,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            id_usuario, correo, contrasena_hash, rol, id_estudiante = result

            if not verificar_contrasena(data.contrasena, contrasena_hash):
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")

            token = crear_token({
                "id_usuario": id_usuario,
                "correo": correo,
                "rol": rol,
                "id_estudiante": id_estudiante
            })

            return {
                "token": token,
                "usuario": {
                    "id_usuario": id_usuario,
                    "correo": correo,
                    "rol": rol,
                    "id_estudiante": id_estudiante
                }
            }

        except psycopg2.Error as err:
            print(err)

        finally:
            conn.close()


    def get_usuario(self, id_usuario: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT id_usuario, correo, rol, id_estudiante, active
                FROM usuario
                WHERE id_usuario=%s""",
                (id_usuario,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            content = {
                "id_usuario": result[0],
                "correo": result[1],
                "rol": result[2],
                "id_estudiante": result[3],
                "active": result[4]
            }

            return jsonable_encoder(content)

        finally:
            conn.close()


    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT id_usuario, correo, rol, id_estudiante, active
                FROM usuario"""
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                payload.append({
                    "id_usuario": data[0],
                    "correo": data[1],
                    "rol": data[2],
                    "id_estudiante": data[3],
                    "active": data[4]
                })

            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay usuarios")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_usuario(self, id_usuario: int, data: Usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            contrasena_hash = encriptar_contrasena(data.contrasena)

            cursor.execute(
                """UPDATE usuario
                SET correo=%s,
                    contrasena=%s,
                    rol=%s,
                    id_estudiante=%s
                WHERE id_usuario=%s""",
                (
                    data.correo,
                    contrasena_hash,
                    data.rol,
                    data.id_estudiante,
                    id_usuario
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            return {"resultado": "Usuario actualizado"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def delete_usuario(self, id_usuario: int):
        """Soft delete: marca active=FALSE"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT correo FROM usuario WHERE id_usuario=%s", (id_usuario,))
            row = cursor.fetchone()
            correo_eliminado = row[0] if row else None

            cursor.execute(
                """UPDATE usuario
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_usuario=%s AND active=TRUE""",
                (id_usuario,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado o ya inactivo")

            if correo_eliminado:
                threading.Thread(
                    target=notif_usuario_eliminado,
                    args=(correo_eliminado, correo_eliminado),
                    daemon=True
                ).start()

            return {"resultado": "Usuario desactivado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()


    def activar_usuario(self, id_usuario: int):
        """Reactiva un usuario previamente desactivado"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE usuario
                SET active=TRUE, deleted_at=NULL
                WHERE id_usuario=%s AND active=FALSE""",
                (id_usuario,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado o ya activo")

            return {"resultado": "Usuario activado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
