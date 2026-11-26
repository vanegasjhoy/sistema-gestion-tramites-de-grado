import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.programa_model import Programa
from fastapi.encoders import jsonable_encoder


class ProgramaController:

    def create_programa(self, data: Programa):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO programa (nombre, id_facultad)
                VALUES (%s,%s)""",
                (data.nombre, data.id_facultad)
            )
            conn.commit()
            return {"resultado": "Programa creado"}
        finally:
            conn.close()

    def get_programa(self, id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_programa, nombre, id_facultad, active FROM programa WHERE id_programa=%s",
            (id,)
        )
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        content = {
            "id_programa": result[0],
            "nombre": result[1],
            "id_facultad": result[2],
            "active": result[3]
        }
        conn.close()
        return jsonable_encoder(content)

    def get_programas(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Retorna TODOS (activos e inactivos) con el campo active incluido
        cursor.execute("SELECT id_programa, nombre, id_facultad, active FROM programa ORDER BY nombre")
        result = cursor.fetchall()
        payload = []
        for data in result:
            content = {
                "id_programa": data[0],
                "nombre": data[1],
                "id_facultad": data[2],
                "active": data[3]
            }
            payload.append(content)
        conn.close()
        if result:
            return {"resultado": jsonable_encoder(payload)}
        else:
            raise HTTPException(status_code=404, detail="No hay programas")

    def update_programa(self, id: int, data: Programa):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE programa
            SET nombre=%s, id_facultad=%s
            WHERE id_programa=%s""",
            (data.nombre, data.id_facultad, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Programa no encontrado")
        conn.close()
        return {"resultado": "Programa actualizado"}

    def delete_programa(self, id: int):
        """Soft delete: marca active=FALSE"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE programa
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_programa=%s AND active=TRUE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Programa no encontrado o ya inactivo")
            return {"resultado": "Programa desactivado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def activar_programa(self, id: int):
        """Reactiva un programa previamente desactivado"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE programa
                SET active=TRUE, deleted_at=NULL
                WHERE id_programa=%s AND active=FALSE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Programa no encontrado o ya activo")
            return {"resultado": "Programa activado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
