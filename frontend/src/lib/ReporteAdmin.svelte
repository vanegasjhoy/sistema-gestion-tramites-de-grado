<svelte:options customElement="reporte-admin" />

<script>
  const API = "http://127.0.0.1:8000";

  let {
    token = "",
    correo = ""
  } = $props();

  // Parámetros de búsqueda (mínimo 3 según especificación)
  let filtroEstado      = $state("");
  let filtroEstadoPago  = $state("");
  let filtroEstadoPaz   = $state("");
  let filtroFechaInicio = $state("");
  let filtroFechaFin    = $state("");
  let tipoReporte       = $state("tramites");

  let generando   = $state(false);
  let mensajeExito = $state("");
  let mensajeError = $state("");

  const headers = { "Content-Type": "application/json", Authorization: `Bearer ${token}` };

  async function generarReporte() {
    if (!token) {
      mensajeError = "Sin token de autenticación.";
      return;
    }
    generando = true;
    mensajeExito = "";
    mensajeError = "";

    try {
      const params = new URLSearchParams();
      if (filtroEstado)      params.set("estado",       filtroEstado);
      if (filtroEstadoPago)  params.set("estado_pago",  filtroEstadoPago);
      if (filtroEstadoPaz)   params.set("estado_paz",   filtroEstadoPaz);
      if (filtroFechaInicio) params.set("fecha_inicio", filtroFechaInicio);
      if (filtroFechaFin)    params.set("fecha_fin",    filtroFechaFin);
      params.set("correo_admin", correo);

      const endpoint = tipoReporte === "tramites"
        ? `/reportes/tramites?${params}`
        : `/reportes/estudiantes?${params}`;

      const res = await fetch(`${API}${endpoint}`, { headers });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        mensajeError = err.detail || "Error al generar el reporte.";
        return;
      }

      // Descargar el PDF
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement("a");
      a.href     = url;
      a.download = `reporte_${tipoReporte}_${new Date().toISOString().split("T")[0]}.pdf`;
      a.click();
      URL.revokeObjectURL(url);

      mensajeExito = "✅ Reporte generado y descargado. Se envió notificación al correo del administrador.";
    } catch (e) {
      mensajeError = "Error de conexión al generar el reporte.";
    } finally {
      generando = false;
    }
  }

  function limpiarFiltros() {
    filtroEstado = "";
    filtroEstadoPago = "";
    filtroEstadoPaz = "";
    filtroFechaInicio = "";
    filtroFechaFin = "";
    mensajeExito = "";
    mensajeError = "";
  }
</script>

<div class="reporte-container">
  <div class="reporte-header">
    <h3>Módulo de Reportes</h3>
    <p class="subtitulo">Genera reportes en PDF filtrando por los parámetros necesarios</p>
  </div>

  <!-- Tipo de reporte -->
  <div class="campo-grupo">
    <label class="campo-label" id="label-tipo-reporte">Tipo de reporte</label>
    <div class="radio-group" role="radiogroup" aria-labelledby="label-tipo-reporte">
      <label class="radio-option" class:activo={tipoReporte === "tramites"}>
        <input type="radio" bind:group={tipoReporte} value="tramites" />
        Trámites de grado
      </label>
      <label class="radio-option" class:activo={tipoReporte === "estudiantes"}>
        <input type="radio" bind:group={tipoReporte} value="estudiantes" />
        Estudiantes
      </label>
    </div>
  </div>

  <!-- Filtros — mínimo 3 parámetros de búsqueda -->
  <div class="filtros-grid">

    <div class="campo-grupo">
      <label class="campo-label" for="filtro-estado">Estado del trámite</label>
      <select id="filtro-estado" bind:value={filtroEstado}>
        <option value="">Todos</option>
        <option value="En Proceso">En Proceso</option>
        <option value="Completado">Completado</option>
        <option value="Cancelado">Cancelado</option>
      </select>
    </div>

    <div class="campo-grupo">
      <label class="campo-label" for="filtro-pago">Estado de pago</label>
      <select id="filtro-pago" bind:value={filtroEstadoPago}>
        <option value="">Todos</option>
        <option value="Pendiente">Pendiente</option>
        <option value="Pagado">Pagado</option>
        <option value="Rechazado">Rechazado</option>
      </select>
    </div>

    <div class="campo-grupo">
      <label class="campo-label" for="filtro-paz">Estado paz y salvo</label>
      <select id="filtro-paz" bind:value={filtroEstadoPaz}>
        <option value="">Todos</option>
        <option value="Pendiente">Pendiente</option>
        <option value="Aprobado">Aprobado</option>
        <option value="Rechazado">Rechazado</option>
      </select>
    </div>

    <div class="campo-grupo">
      <label class="campo-label" for="filtro-fecha-inicio">Fecha inicio (desde)</label>
      <input id="filtro-fecha-inicio" type="date" bind:value={filtroFechaInicio} />
    </div>

    <div class="campo-grupo">
      <label class="campo-label" for="filtro-fecha-fin">Fecha inicio (hasta)</label>
      <input id="filtro-fecha-fin" type="date" bind:value={filtroFechaFin} />
    </div>

  </div>

  <!-- Mensajes -->
  {#if mensajeExito}
    <alert-message tipo="exito" mensaje={mensajeExito}></alert-message>
  {/if}
  {#if mensajeError}
    <alert-message tipo="error" mensaje={mensajeError}></alert-message>
  {/if}

  <!-- Acciones -->
  <div class="acciones">
    <button class="btn-limpiar" onclick={limpiarFiltros}>
      Limpiar filtros
    </button>
    <button class="btn-generar" onclick={generarReporte} disabled={generando}>
      {#if generando}
        <loading-spinner mensaje="" color="#ffffff"></loading-spinner>
        Generando...
      {:else}
        Generar PDF
      {/if}
    </button>
  </div>

  <div class="info-box">
    <strong>Nota:</strong> Al generar el reporte recibirás una notificación en tu correo
    <strong>{correo}</strong> con un resumen de los filtros aplicados.
  </div>
</div>

<style>
  :host { display: block; }

  .reporte-container {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    max-width: 760px;
  }

  .reporte-header { margin-bottom: 20px; }
  .reporte-header h3 { font-size: 17px; color: #1e293b; margin: 0 0 4px; }
  .subtitulo { color: #64748b; font-size: 13px; margin: 0; }

  .filtros-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 14px;
    margin-bottom: 20px;
  }

  .campo-grupo { display: flex; flex-direction: column; gap: 6px; }
  .campo-label { font-size: 12px; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 0.04em; }

  select, input[type="date"] {
    padding: 10px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 14px;
    color: #1e293b;
    background: white;
    width: 100%;
    box-sizing: border-box;
  }

  select:focus, input:focus {
    outline: none;
    border-color: #0d6efd;
    box-shadow: 0 0 0 3px rgba(13,110,253,0.1);
  }

  .radio-group { display: flex; gap: 10px; flex-wrap: wrap; }
  .radio-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border: 1.5px solid #e2e8f0;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    color: #475569;
    transition: all 0.15s;
  }
  .radio-option.activo {
    border-color: #0d6efd;
    background: #eff6ff;
    color: #0d6efd;
    font-weight: 600;
  }
  .radio-option input { display: none; }

  .acciones {
    display: flex;
    gap: 12px;
    margin-top: 20px;
    align-items: center;
  }

  .btn-generar {
    background: #0d6efd;
    color: white;
    border: none;
    padding: 11px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: background 0.15s;
  }
  .btn-generar:hover:not(:disabled) { background: #0b5ed7; }
  .btn-generar:disabled { background: #94a3b8; cursor: not-allowed; }

  .btn-limpiar {
    background: transparent;
    color: #64748b;
    border: 1px solid #e2e8f0;
    padding: 11px 18px;
    border-radius: 8px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .btn-limpiar:hover { background: #f8fafc; border-color: #cbd5e1; }

  .info-box {
    margin-top: 16px;
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    color: #0369a1;
  }

  @media (max-width: 768px) {
    .filtros-grid { grid-template-columns: 1fr 1fr; }
    .reporte-container { padding: 16px; }
  }

  @media (max-width: 480px) {
    .filtros-grid { grid-template-columns: 1fr; }
  }
</style>
