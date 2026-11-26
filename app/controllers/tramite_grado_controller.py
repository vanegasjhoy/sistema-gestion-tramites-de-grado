import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.tramite_grado_model import TramiteGrado
from app.services.email_service import notif_paz_ysalvo_actualizado, notif_estado_pago_actualizado
import threading


class TramiteGradoController:

    def create_tramite_grado(self, data: TramiteGrado):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """INSERT INTO tramite_grado
                (id_estudiante, id_tipo_grado, fecha_inicio, fecha_fin, estado,
                monto, fecha_pago, metodo_pago, estado_pago,
                id_tipo_paz_ysalvo, fecha_aprobacion_paz, estado_paz)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                RETURNING id_tramite_grado""",
                (
                    data.id_estudiante,
                    data.id_tipo_grado,
                    data.fecha_inicio,
                    data.fecha_fin,
                    data.estado,
                    data.monto,
                    data.fecha_pago,
                    data.metodo_pago,
                    data.estado_pago,
                    data.id_tipo_paz_ysalvo,
                    data.fecha_aprobacion_paz,
                    data.estado_paz
                )
            )

            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"resultado": "Trámite de grado creado", "id_tramite_grado": new_id}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_tramite_grado(self, id_tramite_grado: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                tg.id_tramite_grado, tg.id_estudiante, tg.id_tipo_grado,
                tg.fecha_inicio, tg.fecha_fin, tg.estado,
                tg.monto, tg.fecha_pago, tg.metodo_pago, tg.estado_pago,
                tg.id_tipo_paz_ysalvo, tg.fecha_aprobacion_paz, tg.estado_paz,
                e.nombre, e.apellido, e.documento, e.correo,
                tg.active
                FROM tramite_grado tg
                LEFT JOIN estudiante e ON tg.id_estudiante = e.id_estudiante
                WHERE tg.id_tramite_grado=%s""",
                (id_tramite_grado,)
            )

            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Trámite de grado no encontrado")

            content = {
                "id_tramite_grado": result[0],
                "id_estudiante": result[1],
                "id_tipo_grado": result[2],
                "fecha_inicio": result[3],
                "fecha_fin": result[4],
                "estado": result[5],
                "monto": result[6],
                "fecha_pago": result[7],
                "metodo_pago": result[8],
                "estado_pago": result[9],
                "id_tipo_paz_ysalvo": result[10],
                "fecha_aprobacion_paz": result[11],
                "estado_paz": result[12],
                "nombre_estudiante": f"{result[13]} {result[14]}" if result[13] else None,
                "documento_estudiante": result[15],
                "correo_estudiante": result[16],
                "active": result[17]
            }

            return jsonable_encoder(content)

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_tramites_grado(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT
                tg.id_tramite_grado, tg.id_estudiante, tg.id_tipo_grado,
                tg.fecha_inicio, tg.fecha_fin, tg.estado,
                tg.monto, tg.fecha_pago, tg.metodo_pago, tg.estado_pago,
                tg.id_tipo_paz_ysalvo, tg.fecha_aprobacion_paz, tg.estado_paz,
                e.nombre, e.apellido, e.documento, e.correo,
                tg.active
                FROM tramite_grado tg
                LEFT JOIN estudiante e ON tg.id_estudiante = e.id_estudiante"""
            )

            result = cursor.fetchall()

            payload = []

            for data in result:
                payload.append({
                    "id_tramite_grado": data[0],
                    "id_estudiante": data[1],
                    "id_tipo_grado": data[2],
                    "fecha_inicio": data[3],
                    "fecha_fin": data[4],
                    "estado": data[5],
                    "monto": data[6],
                    "fecha_pago": data[7],
                    "metodo_pago": data[8],
                    "estado_pago": data[9],
                    "id_tipo_paz_ysalvo": data[10],
                    "fecha_aprobacion_paz": data[11],
                    "estado_paz": data[12],
                    "nombre_estudiante": f"{data[13]} {data[14]}" if data[13] else None,
                    "documento_estudiante": data[15],
                    "correo_estudiante": data[16],
                    "active": data[17]
                })

            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay trámites de grado")

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_tramite_grado(self, id_tramite_grado: int, data: TramiteGrado):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """UPDATE tramite_grado
                SET id_estudiante=%s,
                    id_tipo_grado=%s,
                    fecha_inicio=%s,
                    fecha_fin=%s,
                    estado=%s,
                    monto=%s,
                    fecha_pago=%s,
                    metodo_pago=%s,
                    estado_pago=%s,
                    id_tipo_paz_ysalvo=%s,
                    fecha_aprobacion_paz=%s,
                    estado_paz=%s
                WHERE id_tramite_grado=%s""",
                (
                    data.id_estudiante,
                    data.id_tipo_grado,
                    data.fecha_inicio,
                    data.fecha_fin,
                    data.estado,
                    data.monto,
                    data.fecha_pago,
                    data.metodo_pago,
                    data.estado_pago,
                    data.id_tipo_paz_ysalvo,
                    data.fecha_aprobacion_paz,
                    data.estado_paz,
                    id_tramite_grado
                )
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Trámite de grado no encontrado")

            return {"resultado": "Trámite de grado actualizado"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def delete_tramite_grado(self, id_tramite_grado: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE tramite_grado
                SET active=FALSE, deleted_at=(NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'America/Bogota')
                WHERE id_tramite_grado=%s AND active=TRUE""",
                (id_tramite_grado,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Trámite de grado no encontrado")
            return {"resultado": "Trámite de grado desactivado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()


    def update_estado_pago(self, id_tramite_grado: int, estado_pago: str):
        """Actualizar solo el estado del pago y notificar al estudiante"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT e.correo, e.nombre || ' ' || e.apellido
                FROM tramite_grado tg
                LEFT JOIN estudiante e ON tg.id_estudiante = e.id_estudiante
                WHERE tg.id_tramite_grado=%s""",
                (id_tramite_grado,)
            )
            row = cursor.fetchone()
            correo_estudiante = row[0] if row else None
            nombre_estudiante = row[1] if row else "Estudiante"

            cursor.execute(
                """UPDATE tramite_grado
                SET estado_pago=%s
                WHERE id_tramite_grado=%s""",
                (estado_pago, id_tramite_grado)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Trámite de grado no encontrado")

            if correo_estudiante:
                threading.Thread(
                    target=notif_estado_pago_actualizado,
                    args=(correo_estudiante, nombre_estudiante, estado_pago),
                    daemon=True
                ).start()

            return {"resultado": f"Estado de pago actualizado a '{estado_pago}'"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def update_estado_paz(self, id_tramite_grado: int, estado_paz: str):
        """Actualizar solo el estado del paz y salvo y notificar al estudiante"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """SELECT e.correo, e.nombre || ' ' || e.apellido
                FROM tramite_grado tg
                LEFT JOIN estudiante e ON tg.id_estudiante = e.id_estudiante
                WHERE tg.id_tramite_grado=%s""",
                (id_tramite_grado,)
            )
            row = cursor.fetchone()
            correo_estudiante = row[0] if row else None
            nombre_estudiante = row[1] if row else "Estudiante"

            cursor.execute(
                """UPDATE tramite_grado
                SET estado_paz=%s
                WHERE id_tramite_grado=%s""",
                (estado_paz, id_tramite_grado)
            )

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Trámite de grado no encontrado")

            if correo_estudiante:
                threading.Thread(
                    target=notif_paz_ysalvo_actualizado,
                    args=(correo_estudiante, nombre_estudiante, estado_paz),
                    daemon=True
                ).start()

            return {"resultado": f"Estado de paz y salvo actualizado a '{estado_paz}'"}

        except psycopg2.Error as err:
            print(err)
            conn.rollback()

        finally:
            conn.close()


    def get_tramites_por_estudiante(self, id_estudiante: int):
        """Retorna los trámites de un estudiante específico"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT
                id_tramite_grado, id_estudiante, id_tipo_grado,
                fecha_inicio, fecha_fin, estado,
                monto, fecha_pago, metodo_pago, estado_pago,
                id_tipo_paz_ysalvo, fecha_aprobacion_paz, estado_paz,
                active
                FROM tramite_grado
                WHERE id_estudiante=%s""",
                (id_estudiante,)
            )
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    "id_tramite_grado": data[0],
                    "id_estudiante": data[1],
                    "id_tipo_grado": data[2],
                    "fecha_inicio": data[3],
                    "fecha_fin": data[4],
                    "estado": data[5],
                    "monto": data[6],
                    "fecha_pago": data[7],
                    "metodo_pago": data[8],
                    "estado_pago": data[9],
                    "id_tipo_paz_ysalvo": data[10],
                    "fecha_aprobacion_paz": data[11],
                    "estado_paz": data[12],
                    "active": data[13]
                })
            return {"resultado": jsonable_encoder(payload)}
        except psycopg2.Error as err:
            print(err)
        finally:
            conn.close()
