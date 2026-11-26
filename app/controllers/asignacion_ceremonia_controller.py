import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.asignacion_ceremonia_model import AsignacionCeremonia
from fastapi.encoders import jsonable_encoder


class AsignacionCeremoniaController:

    def create_asignacion_ceremonia(self, data: AsignacionCeremonia):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO asignacion_ceremonia
                (id_tramite_grado, id_ceremonia_grado)
                VALUES (%s,%s)""",
                (
                    data.id_tramite_grado,
                    data.id_ceremonia_grado
                )
            )

            conn.commit()
            return {"resultado": "Asignación de ceremonia creada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_asignacion_ceremonia(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_asignacion_ceremonia,
                id_tramite_grado,
                id_ceremonia_grado,
                active
                FROM asignacion_ceremonia
                WHERE id_asignacion_ceremonia=%s""",
                (id,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Asignación no encontrada")

            content = {
                "id_asignacion_ceremonia": result[0],
                "id_tramite_grado": result[1],
                "id_ceremonia_grado": result[2],
                "active": result[3]
            }

            return jsonable_encoder(content)

        finally:
            conn.close()


    def get_asignaciones_ceremonia(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_asignacion_ceremonia,
                id_tramite_grado,
                id_ceremonia_grado,
                active
                FROM asignacion_ceremonia"""
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id_asignacion_ceremonia": data[0],
                    "id_tramite_grado": data[1],
                    "id_ceremonia_grado": data[2],
                    "active": data[3]
                }
                payload.append(content)

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="No hay asignaciones")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_asignaciones_por_tramite(self, id_tramite_grado: int):
        """Obtener ceremonia asignada a un trámite específico, con datos completos de la ceremonia"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                ac.id_asignacion_ceremonia,
                ac.id_tramite_grado,
                ac.id_ceremonia_grado,
                cg.nombre,
                cg.fecha,
                cg.lugar,
                cg.horario,
                cg.capacidad,
                ac.active
                FROM asignacion_ceremonia ac
                INNER JOIN ceremonia_grado cg ON ac.id_ceremonia_grado = cg.id_ceremonia_grado
                WHERE ac.id_tramite_grado=%s AND ac.active=TRUE""",
                (id_tramite_grado,)
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id_asignacion_ceremonia": data[0],
                    "id_tramite_grado": data[1],
                    "id_ceremonia_grado": data[2],
                    "nombre": data[3],
                    "fecha": data[4],
                    "lugar": data[5],
                    "horario": data[6],
                    "capacidad": data[7],
                    "active": data[8]
                }
                payload.append(content)

            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="Este trámite no tiene ceremonia asignada")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_asignacion_ceremonia(self, id: int, data: AsignacionCeremonia):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE asignacion_ceremonia
                SET id_tramite_grado=%s,
                    id_ceremonia_grado=%s
                WHERE id_asignacion_ceremonia=%s""",
                (
                    data.id_tramite_grado,
                    data.id_ceremonia_grado,
                    id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Asignación no encontrada")

            return {"resultado": "Asignación actualizada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def delete_asignacion_ceremonia(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE asignacion_ceremonia
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_asignacion_ceremonia=%s AND active=TRUE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Asignación de ceremonia no encontrada")
            return {"resultado": "Asignación de ceremonia desactivada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
