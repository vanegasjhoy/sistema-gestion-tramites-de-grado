import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from app.config.db_config import get_db_connection
from app.services.email_service import notif_reporte_generado
import io
from datetime import date


def _generar_pdf_bytes(titulo: str, parametros: dict, filas: list, columnas: list) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            leftMargin=1.5*cm, rightMargin=1.5*cm,
            topMargin=2*cm, bottomMargin=2*cm
        )

        styles = getSampleStyleSheet()
        ancho_disponible = landscape(A4)[0] - 3*cm  # ~25.3 cm

        # ── Estilos ──────────────────────────────────────────────────────────────
        estilo_titulo = ParagraphStyle(
            "titulo",
            parent=styles["Title"],
            fontSize=16,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=4
        )
        estilo_sub = ParagraphStyle(
            "sub",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=3
        )
        estilo_param = ParagraphStyle(
            "param", parent=styles["Normal"], fontSize=9,
            textColor=colors.HexColor("#475569")
        )
        # Estilo para celdas con texto largo (permite word wrap)
        estilo_celda = ParagraphStyle(
            "celda",
            parent=styles["Normal"],
            fontSize=7,
            leading=9,
            wordWrap="CJK"
        )
        estilo_celda_centro = ParagraphStyle(
            "celda_centro",
            parent=styles["Normal"],
            fontSize=7,
            leading=9,
            alignment=1,  # CENTER
            wordWrap="CJK"
        )

        story = []

        # ── Encabezado ───────────────────────────────────────────────────────────
        story.append(Paragraph("Sistema de Gestión de Trámites de Grado", estilo_titulo))
        story.append(Paragraph(titulo, estilo_sub))
        story.append(Paragraph(f"Generado el: {date.today().strftime('%d/%m/%Y')}", estilo_sub))
        story.append(Spacer(1, 0.3*cm))

        # ── Filtros ──────────────────────────────────────────────────────────────
        params_validos = {k: v for k, v in parametros.items() if v}
        if params_validos:
            params_texto = "  |  ".join([f"<b>{k}:</b> {v}" for k, v in params_validos.items()])
            story.append(Paragraph(f"Filtros aplicados: {params_texto}", estilo_param))
            story.append(Spacer(1, 0.3*cm))

        # ── Anchos de columna por nombre ─────────────────────────────────────────
        # Definimos proporciones relativas para cada columna conocida.
        # Columnas desconocidas reciben peso 1.0 (promedio).
        PESOS = {
            # Reporte trámites
            "ID":           0.4,
            "Estudiante":   1.6,
            "Documento":    1.1,
            "Correo":       2.2,
            "Programa":     1.8,
            "Estado":       1.0,
            "Pago":         0.9,
            "Paz y Salvo":  1.0,
            "Fecha Inicio": 1.0,
            "Fecha Fin":    1.0,
            "Monto":        0.9,
            # Reporte estudiantes
            "Facultad":     1.6,
            "Estado Trámite": 1.0,
            "Estado Pago":  0.9,
            "Estado Paz":   0.9,
        }

        pesos = [PESOS.get(col, 1.0) for col in columnas]
        suma_pesos = sum(pesos)
        anchos = [ancho_disponible * (p / suma_pesos) for p in pesos]

        # ── Convertir celdas de texto largo a Paragraph para word wrap ───────────
        # Columnas que deben alinearse al centro
        COLS_CENTRO = {"ID", "Documento", "Estado", "Pago", "Paz y Salvo",
                       "Fecha Inicio", "Fecha Fin", "Monto",
                       "Estado Trámite", "Estado Pago", "Estado Paz"}
        # Columnas que deben alinearse a la izquierda (texto largo)
        COLS_IZQUIERDA = {"Estudiante", "Correo", "Programa", "Facultad"}

        def wrap(val, col_name):
            """Convierte strings largos a Paragraph para que hagan word wrap."""
            if col_name in COLS_IZQUIERDA:
                return Paragraph(str(val), estilo_celda)
            return Paragraph(str(val), estilo_celda_centro)

        # Encabezados (como strings simples, el TableStyle los centra)
        header_row = list(columnas)

        # Filas de datos con Paragraph
        filas_wrapped = []
        for fila in filas:
            fila_wrapped = [wrap(val, col) for val, col in zip(fila, columnas)]
            filas_wrapped.append(fila_wrapped)

        data_tabla = [header_row] + filas_wrapped

        tabla = Table(data_tabla, colWidths=anchos, repeatRows=1)
        tabla.setStyle(TableStyle([
            # ── Encabezado ──
            ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#1e293b")),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0),  8),
            ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
            ("VALIGN",        (0, 0), (-1, 0),  "MIDDLE"),
            ("TOPPADDING",    (0, 0), (-1, 0),  7),
            ("BOTTOMPADDING", (0, 0), (-1, 0),  7),
            ("LINEBELOW",     (0, 0), (-1, 0),  1.5, colors.HexColor("#0d6efd")),
            # ── Filas de datos ──
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("VALIGN",        (0, 1), (-1, -1),  "MIDDLE"),
            ("TOPPADDING",    (0, 1), (-1, -1),  5),
            ("BOTTOMPADDING", (0, 1), (-1, -1),  5),
            ("LEFTPADDING",   (0, 0), (-1, -1),  4),
            ("RIGHTPADDING",  (0, 0), (-1, -1),  4),
            # ── Bordes ──
            ("GRID",          (0, 0), (-1, -1),  0.5, colors.HexColor("#e2e8f0")),
        ]))

        story.append(tabla)
        story.append(Spacer(1, 0.3*cm))

        # ── Pie de página ────────────────────────────────────────────────────────
        estilo_pie = ParagraphStyle(
            "pie", parent=styles["Normal"], fontSize=8,
            textColor=colors.HexColor("#94a3b8"), alignment=1
        )
        story.append(Paragraph(
            f"Total de registros: {len(filas)}  —  Universidad | Oficina de Registro y Control",
            estilo_pie
        ))

        doc.build(story)
        return buffer.getvalue()

    except ImportError:
        raise RuntimeError("reportlab no instalado. Ejecuta: pip install reportlab")


class ReporteController:

    def generar_reporte_tramites(
        self,
        estado: str = None,
        estado_pago: str = None,
        estado_paz: str = None,
        fecha_inicio: str = None,
        fecha_fin: str = None,
        id_programa: int = None,
        correo_admin: str = None
    ):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    tg.id_tramite_grado,
                    e.nombre || ' ' || e.apellido AS estudiante,
                    e.documento,
                    e.correo,
                    p.nombre AS programa,
                    tg.estado,
                    tg.estado_pago,
                    tg.estado_paz,
                    tg.fecha_inicio,
                    tg.fecha_fin,
                    tg.monto
                FROM tramite_grado tg
                LEFT JOIN estudiante e   ON tg.id_estudiante = e.id_estudiante
                LEFT JOIN programa p     ON e.id_programa    = p.id_programa
                WHERE tg.active = TRUE
            """

            params = []
            if estado:
                query += " AND tg.estado = %s"
                params.append(estado)
            if estado_pago:
                query += " AND tg.estado_pago = %s"
                params.append(estado_pago)
            if estado_paz:
                query += " AND tg.estado_paz = %s"
                params.append(estado_paz)
            if fecha_inicio:
                query += " AND tg.fecha_inicio >= %s"
                params.append(fecha_inicio)
            if fecha_fin:
                query += " AND tg.fecha_inicio <= %s"
                params.append(fecha_fin)
            if id_programa:
                query += " AND e.id_programa = %s"
                params.append(id_programa)

            query += " ORDER BY tg.id_tramite_grado DESC"

            cursor.execute(query, params)
            resultados = cursor.fetchall()

            columnas = [
                "ID", "Estudiante", "Documento", "Correo",
                "Programa", "Estado", "Pago", "Paz y Salvo",
                "Fecha Inicio", "Fecha Fin", "Monto"
            ]

            filas = []
            for r in resultados:
                fila = []
                for val in r:
                    if val is None:
                        fila.append("—")
                    elif hasattr(val, "strftime"):
                        fila.append(val.strftime("%d/%m/%Y"))
                    else:
                        fila.append(str(val))
                filas.append(fila)

            parametros_pdf = {
                "Estado": estado or "Todos",
                "Pago": estado_pago or "Todos",
                "Paz y Salvo": estado_paz or "Todos",
                "Desde": fecha_inicio or "—",
                "Hasta": fecha_fin or "—",
            }

            pdf_bytes = _generar_pdf_bytes(
                titulo="Reporte de Trámites de Grado",
                parametros=parametros_pdf,
                filas=filas,
                columnas=columnas
            )

            if correo_admin:
                parametros_notif = {
                    "Estado trámite": estado or "Todos",
                    "Estado pago": estado_pago or "Todos",
                    "Estado paz y salvo": estado_paz or "Todos",
                    "Fecha inicio desde": fecha_inicio or "—",
                    "Fecha inicio hasta": fecha_fin or "—",
                }
                notif_reporte_generado(
                    correo_admin,
                    parametros_notif,
                    len(filas),
                    pdf_bytes=pdf_bytes,
                    nombre_pdf="reporte_tramites.pdf"
                )

            return StreamingResponse(
                io.BytesIO(pdf_bytes),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=reporte_tramites.pdf"}
            )

        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Error al consultar la base de datos")
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def generar_reporte_estudiantes(
        self,
        id_programa: int = None,
        estado_tramite: str = None,
        correo_admin: str = None
    ):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    e.nombre || ' ' || e.apellido AS estudiante,
                    e.documento,
                    e.correo,
                    p.nombre AS programa,
                    f.nombre AS facultad,
                    tg.estado,
                    tg.estado_pago,
                    tg.estado_paz
                FROM estudiante e
                LEFT JOIN programa p ON e.id_programa = p.id_programa
                LEFT JOIN facultad f ON p.id_facultad = f.id_facultad
                LEFT JOIN tramite_grado tg ON e.id_estudiante = tg.id_estudiante
                WHERE e.active = TRUE
            """
            params = []
            if id_programa:
                query += " AND e.id_programa = %s"
                params.append(id_programa)
            if estado_tramite:
                query += " AND tg.estado = %s"
                params.append(estado_tramite)

            query += " ORDER BY e.apellido, e.nombre"
            cursor.execute(query, params)
            resultados = cursor.fetchall()

            columnas = ["Estudiante", "Documento", "Correo", "Programa", "Facultad",
                        "Estado Trámite", "Estado Pago", "Estado Paz"]
            filas = [[str(v) if v is not None else "—" for v in r] for r in resultados]

            pdf_bytes = _generar_pdf_bytes(
                titulo="Reporte de Estudiantes",
                parametros={"Programa": str(id_programa) if id_programa else "Todos",
                            "Estado": estado_tramite or "Todos"},
                filas=filas,
                columnas=columnas
            )

            if correo_admin:
                notif_reporte_generado(
                    correo_admin,
                    {"Programa": id_programa or "Todos", "Estado": estado_tramite or "Todos"},
                    len(filas),
                    pdf_bytes=pdf_bytes,
                    nombre_pdf="reporte_estudiantes.pdf"
                )

            return StreamingResponse(
                io.BytesIO(pdf_bytes),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=reporte_estudiantes.pdf"}
            )

        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except psycopg2.Error as err:
            print(err)
            raise HTTPException(status_code=500, detail="Error al consultar la base de datos")
        finally:
            try:
                conn.close()
            except Exception:
                pass
