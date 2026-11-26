import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.facultad_model import Facultad
from fastapi.encoders import jsonable_encoder


class FacultadController:

    def create_facultad(self, data: Facultad):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO facultad (nombre)
                VALUES (%s)""",
                (data.nombre,)
            )
            conn.commit()
            return {"resultado": "Facultad creada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_facultad(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_facultad, nombre, active FROM facultad WHERE id_facultad=%s",
                (id,)
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
            return jsonable_encoder({"id_facultad": result[0], "nombre": result[1], "active": result[2]})
        finally:
            conn.close()

    def get_facultades(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Retorna TODAS (activas e inactivas) para que el admin vea el estado real
            cursor.execute("SELECT id_facultad, nombre, active FROM facultad ORDER BY nombre")
            result = cursor.fetchall()
            if result:
                payload = [{"id_facultad": d[0], "nombre": d[1], "active": d[2]} for d in result]
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay facultades")
        finally:
            conn.close()

    def update_facultad(self, id: int, data: Facultad):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE facultad SET nombre=%s WHERE id_facultad=%s AND active=TRUE",
                (data.nombre, id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Facultad no encontrada")
            return {"resultado": "Facultad actualizada"}
        finally:
            conn.close()

    def delete_facultad(self, id: int):
        """Soft delete: marca active=FALSE"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE facultad
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_facultad=%s AND active=TRUE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Facultad no encontrada o ya inactiva")
            return {"resultado": "Facultad desactivada"}
        finally:
            conn.close()

    def activar_facultad(self, id: int):
        """Reactiva una facultad previamente desactivada"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE facultad
                SET active=TRUE, deleted_at=NULL
                WHERE id_facultad=%s AND active=FALSE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Facultad no encontrada o ya activa")
            return {"resultado": "Facultad activada"}
        finally:
            conn.close()
