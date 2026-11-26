import psycopg2
from app.models.entrega_documento_model import EntregaDocumento
from app.config.db_config import get_db_connection
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


class EntregaDocumentoController:

    def create_entrega_documento(self, data: EntregaDocumento):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO entrega_documento
                (id_tramite_grado, id_estudiante, id_documento_requerido, fecha_entrega, estado)
                VALUES (%s,%s,%s,%s,%s)""",
                (
                    data.id_tramite_grado,
                    data.id_estudiante,
                    data.id_documento_requerido,
                    data.fecha_entrega,
                    data.estado
                )
            )

            conn.commit()
            return {"resultado": "Entrega de documento registrada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_entrega_documento(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_entrega_documento,
                id_tramite_grado,
                id_estudiante,
                id_documento_requerido,
                fecha_entrega,
                estado,
                active
                FROM entrega_documento
                WHERE id_entrega_documento=%s""",
                (id,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Entrega no encontrada")

            content = {
                "id_entrega_documento": result[0],
                "id_tramite_grado": result[1],
                "id_estudiante": result[2],
                "id_documento_requerido": result[3],
                "fecha_entrega": result[4],
                "estado": result[5],
                "active": result[6]
            }

            return jsonable_encoder(content)

        finally:
            conn.close()


    def get_entregas_documentos(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_entrega_documento,
                id_tramite_grado,
                id_estudiante,
                id_documento_requerido,
                fecha_entrega,
                estado,
                active
                FROM entrega_documento"""
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id_entrega_documento": data[0],
                    "id_tramite_grado": data[1],
                    "id_estudiante": data[2],
                    "id_documento_requerido": data[3],
                    "fecha_entrega": data[4],
                    "estado": data[5],
                    "active": data[6]
                }
                payload.append(content)

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="No hay entregas registradas")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_entregas_por_tramite(self, id_tramite_grado: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                ed.id_entrega_documento,
                ed.id_tramite_grado,
                ed.id_estudiante,
                ed.id_documento_requerido,
                ed.fecha_entrega,
                ed.estado,
                dr.nombre AS nombre_documento,
                ed.active
                FROM entrega_documento ed
                LEFT JOIN documento_requerido dr ON ed.id_documento_requerido = dr.id_documento_requerido
                WHERE ed.id_tramite_grado=%s""",
                (id_tramite_grado,)
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id_entrega_documento": data[0],
                    "id_tramite_grado": data[1],
                    "id_estudiante": data[2],
                    "id_documento_requerido": data[3],
                    "fecha_entrega": data[4],
                    "estado": data[5],
                    "nombre_documento": data[6],
                    "active": data[7]
                }
                payload.append(content)

            return {"resultado": jsonable_encoder(payload)}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_entrega_documento(self, id: int, data: EntregaDocumento):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE entrega_documento
                SET id_tramite_grado=%s,
                    id_estudiante=%s,
                    id_documento_requerido=%s,
                    fecha_entrega=%s,
                    estado=%s
                WHERE id_entrega_documento=%s""",
                (
                    data.id_tramite_grado,
                    data.id_estudiante,
                    data.id_documento_requerido,
                    data.fecha_entrega,
                    data.estado,
                    id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Entrega no encontrada")

            return {"resultado": "Entrega actualizada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def delete_entrega_documento(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE entrega_documento
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_entrega_documento=%s AND active=TRUE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Entrega no encontrada")
            return {"resultado": "Entrega desactivada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
