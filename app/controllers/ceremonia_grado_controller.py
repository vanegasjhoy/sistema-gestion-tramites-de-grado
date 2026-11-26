import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.ceremonia_grado_model import CeremoniaGrado
from fastapi.encoders import jsonable_encoder


class CeremoniaGradoController:

    def create_ceremonia(self, data: CeremoniaGrado):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO ceremonia_grado
                (nombre, fecha, lugar, horario, capacidad)
                VALUES (%s,%s,%s,%s,%s)""",
                (
                    data.nombre,
                    data.fecha,
                    data.lugar,
                    data.horario,
                    data.capacidad
                )
            )

            conn.commit()
            return {"resultado": "Ceremonia creada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_ceremonia(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_ceremonia_grado,
                nombre,
                fecha,
                lugar,
                horario,
                capacidad,
                active
                FROM ceremonia_grado
                WHERE id_ceremonia_grado=%s""",
                (id,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Ceremonia no encontrada")

            content = {
                "id_ceremonia_grado": result[0],
                "nombre": result[1],
                "fecha": result[2],
                "lugar": result[3],
                "horario": result[4],
                "capacidad": result[5],
                "active": result[6]
            }

            return jsonable_encoder(content)

        finally:
            conn.close()


    def get_ceremonias(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_ceremonia_grado,
                nombre,
                fecha,
                lugar,
                horario,
                capacidad,
                active
                FROM ceremonia_grado"""
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id_ceremonia_grado": data[0],
                    "nombre": data[1],
                    "fecha": data[2],
                    "lugar": data[3],
                    "horario": data[4],
                    "capacidad": data[5],
                    "active": data[6]
                }

                payload.append(content)

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="No hay ceremonias registradas")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_ceremonia(self, id: int, data: CeremoniaGrado):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE ceremonia_grado
                SET nombre=%s,
                    fecha=%s,
                    lugar=%s,
                    horario=%s,
                    capacidad=%s
                WHERE id_ceremonia_grado=%s""",
                (
                    data.nombre,
                    data.fecha,
                    data.lugar,
                    data.horario,
                    data.capacidad,
                    id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Ceremonia no encontrada")

            return {"resultado": "Ceremonia actualizada"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def delete_ceremonia(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE ceremonia_grado
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_ceremonia_grado=%s AND active=TRUE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Ceremonia de grado no encontrada")
            return {"resultado": "Ceremonia de grado desactivada"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
