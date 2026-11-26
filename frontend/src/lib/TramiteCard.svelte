<svelte:options customElement="tramite-card" />

<script>
  let {
    estado = "En Proceso",
    estudiante = "Estudiante",
    tipo_grado = "Pregrado",
    fecha_inicio = "",
    estado_pago = "Pendiente",
    estado_paz = "Pendiente"
  } = $props();

  // Color según estado del trámite
  function colorEstado(estado) {
    if (estado === "Completado") return "#22c55e";
    if (estado === "Cancelado") return "#ef4444";
    return "#f59e0b";
  }

  // Color según estado de pago
  function colorPago(estado) {
    if (["Pagado", "Aprobado", "Entregado"].includes(estado)) return "#22c55e";
    if (["Rechazado", "Cancelado"].includes(estado)) return "#ef4444";
    return "#f59e0b";
  }
</script>

<div class="tramite-card">
  <div class="header">
    <span class="nombre">{estudiante}</span>
    <span class="badge" style="background-color: {colorEstado(estado)}">{estado}</span>
  </div>

  <div class="info">
    <div class="fila">
      <span class="label">Tipo de grado:</span>
      <span class="valor">{tipo_grado}</span>
    </div>
    <div class="fila">
      <span class="label">Fecha inicio:</span>
      <span class="valor">{fecha_inicio || "—"}</span>
    </div>
    <div class="fila">
      <span class="label">Pago:</span>
      <span class="badge-small" style="background-color: {colorPago(estado_pago)}">{estado_pago}</span>
    </div>
    <div class="fila">
      <span class="label">Paz y salvo:</span>
      <span class="badge-small" style="background-color: {colorPago(estado_paz)}">{estado_paz}</span>
    </div>
  </div>
</div>

<style>
  .tramite-card {
    font-family: sans-serif;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    max-width: 320px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .nombre {
    font-weight: 600;
    font-size: 15px;
    color: #1e293b;
  }

  .badge {
    color: white;
    font-size: 12px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
  }

  .badge-small {
    color: white;
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 20px;
  }

  .info {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .fila {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
  }

  .label {
    color: #64748b;
  }

  .valor {
    color: #1e293b;
    font-weight: 500;
  }
</style>
