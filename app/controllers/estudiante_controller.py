import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from app.models.estudiante_model import Estudiante
from fastapi.encoders import jsonable_encoder


class EstudianteController:

    def create_estudiante(self, data: Estudiante):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO estudiante
                (nombre, apellido, documento, id_tipo_documento,
                correo, id_programa, id_tipo_grado, fecha_nacimiento, genero)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_estudiante""",
                (
                    data.nombre,
                    data.apellido,
                    data.documento,
                    data.id_tipo_documento,
                    data.correo,
                    data.id_programa,
                    data.id_tipo_grado,
                    data.fecha_nacimiento,
                    data.genero
                )
            )

            row = cursor.fetchone()
            id_estudiante = row[0] if row else None
            conn.commit()
            return {"resultado": "Estudiante creado", "id_estudiante": id_estudiante}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_estudiante(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_estudiante,
                nombre,
                apellido,
                documento,
                id_tipo_documento,
                correo,
                id_programa,
                id_tipo_grado,
                fecha_nacimiento,
                genero,
                active
                FROM estudiante
                WHERE id_estudiante=%s""",
                (id,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            content = {
                "id_estudiante": result[0],
                "nombre": result[1],
                "apellido": result[2],
                "documento": result[3],
                "id_tipo_documento": result[4],
                "correo": result[5],
                "id_programa": result[6],
                "id_tipo_grado": result[7],
                "fecha_nacimiento": result[8],
                "genero": result[9],
                "active": result[10]
            }

            return jsonable_encoder(content)

        finally:
            conn.close()


    def get_estudiantes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                id_estudiante,
                nombre,
                apellido,
                documento,
                id_tipo_documento,
                correo,
                id_programa,
                id_tipo_grado,
                fecha_nacimiento,
                genero,
                active
                FROM estudiante"""
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                content = {
                    "id_estudiante": data[0],
                    "nombre": data[1],
                    "apellido": data[2],
                    "documento": data[3],
                    "id_tipo_documento": data[4],
                    "correo": data[5],
                    "id_programa": data[6],
                    "id_tipo_grado": data[7],
                    "fecha_nacimiento": data[8],
                    "genero": data[9],
                    "active": data[10]
                }

                payload.append(content)

            json_data = jsonable_encoder(payload)

            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="No hay estudiantes")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_estudiante(self, id: int, data: Estudiante):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE estudiante
                SET nombre=%s,
                    apellido=%s,
                    documento=%s,
                    id_tipo_documento=%s,
                    correo=%s,
                    id_programa=%s,
                    id_tipo_grado=%s,
                    fecha_nacimiento=%s,
                    genero=%s
                WHERE id_estudiante=%s""",
                (
                    data.nombre,
                    data.apellido,
                    data.documento,
                    data.id_tipo_documento,
                    data.correo,
                    data.id_programa,
                    data.id_tipo_grado,
                    data.fecha_nacimiento,
                    data.genero,
                    id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            return {"resultado": "Estudiante actualizado"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def delete_estudiante(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE estudiante
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_estudiante=%s AND active=TRUE""",
                (id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")
            return {"resultado": "Estudiante desactivado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()


    def verificar_aplica_grado(self, id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 1. Verificar que el estudiante tiene un trámite activo
            cursor.execute("""
                SELECT id_tramite_grado
                FROM tramite_grado
                WHERE id_estudiante = %s
                AND active = TRUE
                ORDER BY fecha_inicio DESC
                LIMIT 1
            """, (id,))

            tramite = cursor.fetchone()

            if not tramite:
                return {
                    "aplica_grado": False,
                    "mensaje": "El estudiante no tiene un trámite de grado activo"
                }

            id_tramite = tramite[0]

            # 2. Verificar pago (ahora está en tramite_grado)
            cursor.execute("""
                SELECT estado_pago
                FROM tramite_grado
                WHERE id_tramite_grado = %s
            """, (id_tramite,))

            estado_pago = cursor.fetchone()[0]

            if estado_pago != 'Pagado':
                return {
                    "aplica_grado": False,
                    "mensaje": "El estudiante no ha pagado el trámite de grado"
                }

            # 3. Verificar documentos pendientes (ahora conectados al trámite)
            cursor.execute("""
                SELECT COUNT(*)
                FROM documento_requerido dr
                LEFT JOIN entrega_documento ed
                ON dr.id_documento_requerido = ed.id_documento_requerido
                AND ed.id_tramite_grado = %s
                WHERE ed.estado != 'Entregado' OR ed.estado IS NULL
            """, (id_tramite,))

            documentos_pendientes = cursor.fetchone()[0]

            if documentos_pendientes > 0:
                return {
                    "aplica_grado": False,
                    "mensaje": "El estudiante tiene documentos pendientes"
                }

            # 4. Verificar paz y salvo (ahora está en tramite_grado)
            cursor.execute("""
                SELECT estado_paz
                FROM tramite_grado
                WHERE id_tramite_grado = %s
            """, (id_tramite,))

            estado_paz = cursor.fetchone()[0]

            if estado_paz != 'Aprobado':
                return {
                    "aplica_grado": False,
                    "mensaje": "El estudiante tiene paz y salvo pendiente"
                }

            return {
                "aplica_grado": True,
                "mensaje": "El estudiante cumple todos los requisitos para grado"
            }

        except psycopg2.Error as err:
            print(err)

        finally:
            conn.close()
