import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS") 


def enviar_correo(
    destinatario: str,
    asunto: str,
    cuerpo_html: str,
    pdf_adjunto: bytes = None,
    nombre_adjunto: str = "reporte.pdf"
) -> bool:
    """
    Envía un correo HTML al destinatario.
    Si se proporciona pdf_adjunto (bytes), lo adjunta al correo.
    Retorna True si fue exitoso, False si falló.
    """
    try:
        msg = MIMEMultipart("mixed")
        msg["Subject"] = asunto
        msg["From"] = f"Trámites de Grado <{SMTP_USER}>"
        msg["To"] = destinatario

        # Parte HTML
        parte_alternativa = MIMEMultipart("alternative")
        parte_html = MIMEText(cuerpo_html, "html", "utf-8")
        parte_alternativa.attach(parte_html)
        msg.attach(parte_alternativa)

        # Adjunto PDF (opcional)
        if pdf_adjunto:
            adjunto = MIMEBase("application", "pdf")
            adjunto.set_payload(pdf_adjunto)
            encoders.encode_base64(adjunto)
            adjunto.add_header(
                "Content-Disposition",
                "attachment",
                filename=nombre_adjunto
            )
            msg.attach(adjunto)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, destinatario, msg.as_string())

        print(f"[EMAIL] Correo enviado a {destinatario} — {asunto}")
        return True

    except Exception as e:
        print(f"[EMAIL ERROR] No se pudo enviar a {destinatario}: {e}")
        return False


# ─── Plantillas de correo ──────────────────────────────────────────────────────

def _base_template(contenido: str) -> str:
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #f1f5f9; padding: 0; margin: 0;">
      <div style="max-width: 600px; margin: 32px auto; background: white;
                  border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
        <div style="background: #1e293b; padding: 24px 32px;">
          <h1 style="color: white; margin: 0; font-size: 20px;">🎓 Sistema de Trámites de Grado</h1>
        </div>
        <div style="padding: 32px;">
          {contenido}
        </div>
        <div style="background: #f8fafc; padding: 16px 32px; text-align: center;
                    color: #94a3b8; font-size: 12px; border-top: 1px solid #e2e8f0;">
          Este correo fue generado automáticamente. No responder.
        </div>
      </div>
    </body>
    </html>
    """


def notif_usuario_creado(destinatario: str, correo_nuevo: str, rol: str) -> bool:
    cuerpo = _base_template(f"""
        <h2 style="color:#1e293b;">👤 Nuevo usuario registrado</h2>
        <p style="color:#64748b;">Se ha creado un nuevo usuario en el sistema:</p>
        <table style="width:100%; border-collapse:collapse; margin:16px 0;">
          <tr><td style="padding:8px; color:#64748b; width:40%;">Correo:</td>
              <td style="padding:8px; color:#1e293b; font-weight:600;">{correo_nuevo}</td></tr>
          <tr style="background:#f8fafc;">
              <td style="padding:8px; color:#64748b;">Rol:</td>
              <td style="padding:8px; color:#1e293b; font-weight:600;">{rol}</td></tr>
        </table>
        <p style="color:#64748b; font-size:13px;">Si no reconoces esta acción, contacta al administrador.</p>
    """)
    return enviar_correo(destinatario, "✅ Nuevo usuario creado — Trámites de Grado", cuerpo)


def notif_usuario_eliminado(destinatario: str, correo_eliminado: str) -> bool:
    cuerpo = _base_template(f"""
        <h2 style="color:#ef4444;">🗑️ Usuario desactivado</h2>
        <p style="color:#64748b;">El siguiente usuario ha sido desactivado del sistema:</p>
        <div style="background:#fef2f2; border-left:4px solid #ef4444;
                    padding:12px 16px; border-radius:0 8px 8px 0; margin:16px 0;">
          <strong style="color:#1e293b;">{correo_eliminado}</strong>
        </div>
        <p style="color:#64748b; font-size:13px;">Si consideras que esto es un error, contacta al administrador.</p>
    """)
    return enviar_correo(destinatario, "⚠️ Usuario desactivado — Trámites de Grado", cuerpo)


def notif_reporte_generado(
    destinatario: str,
    parametros: dict,
    total_resultados: int,
    pdf_bytes: bytes = None,
    nombre_pdf: str = "reporte.pdf"
) -> bool:
    params_html = "".join([
        f"<tr {'style=\"background:#f8fafc;\"' if i % 2 else ''}>"
        f"<td style='padding:8px;color:#64748b;'>{k}:</td>"
        f"<td style='padding:8px;color:#1e293b;font-weight:600;'>{v}</td></tr>"
        for i, (k, v) in enumerate(parametros.items()) if v
    ])
    adjunto_info = (
        f'''<div style="background:#eff6ff; border-left:4px solid #3b82f6;
                    padding:12px 16px; border-radius:0 8px 8px 0; margin:16px 0;">
          📎 <strong style="color:#1d4ed8;">El reporte PDF está adjunto a este correo.</strong>
        </div>'''
        if pdf_bytes else
        "<p style=\"color:#64748b; font-size:13px;\">El PDF fue descargado por el administrador.</p>"
    )
    cuerpo = _base_template(f"""
        <h2 style="color:#1e293b;">📊 Reporte generado</h2>
        <p style="color:#64748b;">Se ha generado un reporte con los siguientes parámetros:</p>
        <table style="width:100%; border-collapse:collapse; margin:16px 0;">
          {params_html}
        </table>
        <div style="background:#f0fdf4; border-left:4px solid #22c55e;
                    padding:12px 16px; border-radius:0 8px 8px 0; margin:16px 0;">
          <strong style="color:#16a34a;">Total de resultados: {total_resultados}</strong>
        </div>
        {adjunto_info}
    """)
    return enviar_correo(
        destinatario,
        "📊 Reporte generado — Trámites de Grado",
        cuerpo,
        pdf_adjunto=pdf_bytes,
        nombre_adjunto=nombre_pdf
    )


def notif_paz_ysalvo_actualizado(destinatario: str, nombre_estudiante: str, nuevo_estado: str) -> bool:
    color = "#22c55e" if nuevo_estado == "Aprobado" else "#ef4444"
    emoji = "✅" if nuevo_estado == "Aprobado" else "❌"
    cuerpo = _base_template(f"""
        <h2 style="color:#1e293b;">{emoji} Paz y salvo actualizado</h2>
        <p style="color:#64748b;">El paz y salvo del estudiante <strong>{nombre_estudiante}</strong>
        ha sido actualizado:</p>
        <div style="background:#f8fafc; border-left:4px solid {color};
                    padding:16px; border-radius:0 8px 8px 0; margin:16px 0; text-align:center;">
          <span style="font-size:18px; font-weight:700; color:{color};">{nuevo_estado}</span>
        </div>
        <p style="color:#64748b; font-size:13px;">Ingresa al sistema para más detalles.</p>
    """)
    return enviar_correo(destinatario, f"{emoji} Paz y salvo {nuevo_estado} — Trámites de Grado", cuerpo)


def notif_estado_pago_actualizado(destinatario: str, nombre_estudiante: str, nuevo_estado: str) -> bool:
    color = "#22c55e" if nuevo_estado == "Pagado" else "#ef4444" if nuevo_estado == "Rechazado" else "#f59e0b"
    emoji = "💳" if nuevo_estado == "Pagado" else "❌" if nuevo_estado == "Rechazado" else "⏳"
    cuerpo = _base_template(f"""
        <h2 style="color:#1e293b;">{emoji} Estado de pago actualizado</h2>
        <p style="color:#64748b;">El estado de pago del trámite de grado de <strong>{nombre_estudiante}</strong>
        ha sido actualizado:</p>
        <div style="background:#f8fafc; border-left:4px solid {color};
                    padding:16px; border-radius:0 8px 8px 0; margin:16px 0; text-align:center;">
          <span style="font-size:18px; font-weight:700; color:{color};">{nuevo_estado}</span>
        </div>
        <p style="color:#64748b; font-size:13px;">Ingresa al sistema para ver el detalle de tu trámite.</p>
    """)
    return enviar_correo(destinatario, f"{emoji} Estado de pago {nuevo_estado} — Trámites de Grado", cuerpo)
