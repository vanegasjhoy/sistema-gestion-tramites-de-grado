import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.tipo_documento_model import TipoDocumento


class TipoDocumentoController:

    def create_tipo_documento(self, data: TipoDocumento):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO tipo_documento (nombre) VALUES (%s)",
                (data.nombre,)
            )

            conn.commit()
            return {"resultado": "Tipo de documento creado"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_tipo_documento(self, id_tipo_documento: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id_tipo_documento, nombre, active FROM tipo_documento WHERE id_tipo_documento=%s",
                (id_tipo_documento,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")

            return jsonable_encoder({
                "id_tipo_documento": result[0],
                "nombre": result[1],
                "active": result[2]
            })

        finally:
            conn.close()


    def get_tipos_documento(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id_tipo_documento, nombre, active FROM tipo_documento")

            result = cursor.fetchall()

            payload = [{
                "id_tipo_documento": data[0],
                "nombre": data[1],
                "active": data[2]
            } for data in result]

            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay tipos de documento")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_tipo_documento(self, id_tipo_documento: int, data: TipoDocumento):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE tipo_documento SET nombre=%s WHERE id_tipo_documento=%s",
                (data.nombre, id_tipo_documento)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")

            return {"resultado": "Tipo de documento actualizado"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def delete_tipo_documento(self, id_tipo_documento: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE tipo_documento
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_tipo_documento=%s AND active=TRUE""",
                (id_tipo_documento,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
            return {"resultado": "Tipo de documento desactivado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
