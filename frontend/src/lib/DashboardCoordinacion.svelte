<svelte:options customElement="dashboard-coordinacion" />

<script>
  const API = "http://127.0.0.1:8000";
  const shieldSrc = "data:image/png;base64,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";

  let token = localStorage.getItem("token");
  let correo = localStorage.getItem("correo");
  if (!token || localStorage.getItem("rol") !== "coordinacion") window.location.href = "index.html";

  const headers = { "Content-Type": "application/json", Authorization: `Bearer ${token}` };

  let seccion = $state("solicitudes");
  let tramites = $state([]);
  let tramiteSeleccionado = $state(null);
  let documentosTramite = $state([]);
  let ceremonias = $state([]);
  let ceremoniaSeleccionada = $state("");
  let cargando = $state(true);
  let error = $state("");
  let mensajeExito = $state("");
  let menuAbierto = $state(false);

  const powerBiUrl = "https://app.powerbi.com/reportEmbed?reportId=643fe267-eec7-4752-acf8-e7824beedbda&autoAuth=true&ctid=740be6bd-fd36-470e-94d9-0f0c777fadb9";

  function colorEstado(estado) {
    if (["Completado","Pagado","Aprobado","Entregado"].includes(estado)) return "#22c55e";
    if (["Cancelado","Rechazado"].includes(estado)) return "#ef4444";
    return "#f59e0b";
  }

  function badgeHtml(estado) {
    return `<span class="badge" style="background:${colorEstado(estado)}">${estado ?? "—"}</span>`;
  }

  let filasTramites = $derived(tramites.map(t => ({
    nombre_estudiante: t.nombre_estudiante || `ID: ${t.id_estudiante}`,
    documento_estudiante: t.documento_estudiante || "—",
    estado: badgeHtml(t.estado),
    estado_pago: badgeHtml(t.estado_pago),
    estado_paz: badgeHtml(t.estado_paz),
    acciones: `<button class="btn-accion verde" data-accion="ver" data-id="${t.id_tramite_grado}">Ver detalle</button>`
  })));

  let filasCeremonias = $derived(ceremonias.map(c => ({
    nombre: c.nombre || "—",
    fecha: c.fecha,
    lugar: c.lugar || "—",
    horario: c.horario || "—",
    capacidad: c.capacidad || "—"
  })));

  let filasDocumentos = $derived(documentosTramite.map(doc => ({
    nombre_documento: doc.nombre_documento || `Doc ID: ${doc.id_documento_requerido}`,
    fecha_entrega: doc.fecha_entrega || "—",
    estado: badgeHtml(doc.estado),
    acciones: `
      <button class="btn-accion verde" data-accion="aprobar" data-id="${doc.id_entrega_documento}">Aprobar</button>
      <button class="btn-accion rojo" data-accion="rechazar" data-id="${doc.id_entrega_documento}">Rechazar</button>
    `
  })));

  const columnsTramites = JSON.stringify([
    { key: "nombre_estudiante", label: "Estudiante" },
    { key: "documento_estudiante", label: "Documento" },
    { key: "estado", label: "Estado" },
    { key: "estado_pago", label: "Pago" },
    { key: "estado_paz", label: "Paz y salvo" },
    { key: "acciones", label: "Acciones" }
  ]);

  const columnsDocumentos = JSON.stringify([
    { key: "nombre_documento", label: "Documento" },
    { key: "fecha_entrega", label: "Fecha entrega" },
    { key: "estado", label: "Estado" },
    { key: "acciones", label: "Acciones" }
  ]);

  async function cargarTramites() {
    cargando = true; error = "";
    try {
      const res = await fetch(`${API}/tramites_grado`, { headers });
      const data = await res.json();
      if (res.ok) tramites = data.resultado || [];
      else error = data.detail || "Error al cargar solicitudes.";
    } catch (e) { error = "Error al cargar solicitudes."; }
    finally { cargando = false; }
  }

  async function cargarCeremonias() {
    try {
      const res = await fetch(`${API}/ceremonias`, { headers });
      const data = await res.json();
      if (res.ok) ceremonias = data.resultado || [];
    } catch (e) {}
  }

  async function verDetalles(idTramite) {
    tramiteSeleccionado = tramites.find(t => t.id_tramite_grado === idTramite);
    ceremoniaSeleccionada = "";
    modalDetalle = true;
    try {
      const res = await fetch(`${API}/tramites_grado/${idTramite}/entregas`, { headers });
      const data = await res.json();
      if (res.ok) documentosTramite = data.resultado || data || [];
    } catch (e) {}
  }

  async function actualizarEstadoDoc(idEntrega, nuevoEstado) {
    const doc = documentosTramite.find(d => d.id_entrega_documento === idEntrega);
    if (!doc) return;
    try {
      const res = await fetch(`${API}/entregas_documentos/${idEntrega}`, {
        method: "PUT", headers,
        body: JSON.stringify({
          id_tramite_grado: doc.id_tramite_grado,
          id_estudiante: doc.id_estudiante,
          id_documento_requerido: doc.id_documento_requerido,
          fecha_entrega: doc.fecha_entrega,
          estado: nuevoEstado
        })
      });
      if (res.ok) {
        documentosTramite = documentosTramite.map(d =>
          d.id_entrega_documento === idEntrega ? { ...d, estado: nuevoEstado } : d
        );
        mostrarExito("Estado de documento actualizado.");
      }
    } catch (e) {}
  }

  async function actualizarPaz(idTramite, estadoPaz) {
    try {
      const res = await fetch(`${API}/tramites_grado/${idTramite}/paz?estado_paz=${estadoPaz}`, { method: "PATCH", headers });
      if (res.ok) {
        tramiteSeleccionado = { ...tramiteSeleccionado, estado_paz: estadoPaz };
        mostrarExito("Paz y salvo actualizado.");
      }
    } catch (e) {}
  }

  async function asignarCeremonia(idTramite) {
    if (!ceremoniaSeleccionada) return;
    try {
      const res = await fetch(`${API}/asignaciones_ceremonia`, {
        method: "POST", headers,
        body: JSON.stringify({ id_tramite_grado: idTramite, id_ceremonia_grado: parseInt(ceremoniaSeleccionada) })
      });
      if (res.ok) mostrarExito("Ceremonia asignada correctamente.");
    } catch (e) {}
  }

  function onTableAction(e) {
    const { id, accion } = e.detail;
    if (accion === "ver") verDetalles(parseInt(id));
    else if (accion === "aprobar") actualizarEstadoDoc(parseInt(id), "Entregado");
    else if (accion === "rechazar") actualizarEstadoDoc(parseInt(id), "Rechazado");
  }

  function mostrarExito(msg) { mensajeExito = msg; setTimeout(() => mensajeExito = "", 3000); }
  function cambiarSeccion(s) { seccion = s; tramiteSeleccionado = null; menuAbierto = false; }

  // ===== MODAL DETALLE =====
  let modalDetalle = $state(false);

  // ===== MODAL DE CONFIRMACIÓN (logout) =====
  let modalVisible      = $state(false);
  let modalTitulo       = $state("");
  let modalMensaje      = $state("");
  let modalTipo         = $state("advertencia");
  let modalTextoAceptar = $state("Confirmar");

  function confirmar({ titulo, mensaje, tipo = "advertencia", textoAceptar = "Confirmar", onconfirm }) {
    modalTitulo       = titulo;
    modalMensaje      = mensaje;
    modalTipo         = tipo;
    modalTextoAceptar = textoAceptar;
    modalVisible      = true;
    requestAnimationFrame(() => {
      window.__modal = {
        confirmar: () => { modalVisible = false; onconfirm(); },
        cancelar:  () => { modalVisible = false; },
      };
    });
  }

  function cerrarSesion() {
    confirmar({
      titulo: "¿Cerrar sesión?",
      mensaje: "Se cerrará tu sesión y serás redirigido al inicio. ¿Deseas continuar?",
      tipo: "advertencia",
      textoAceptar: "Cerrar sesión",
      onconfirm: () => { localStorage.clear(); window.location.href = "index.html"; }
    });
  }

  let navItems = JSON.stringify([
    { label: "Solicitudes",  value: "solicitudes"  },
    { label: "Ceremonias",   value: "ceremonias"   },
    { label: "Estadísticas", value: "estadisticas" }
  ]);

  function onNavChange(e) { cambiarSeccion(e.detail.value); }

  cargarTramites();
  cargarCeremonias();
</script>

<svelte:document on:navchange={onNavChange} />

<div class="layout" role="presentation">
  <confirm-modal
    visible={modalVisible}
    titulo={modalTitulo}
    mensaje={modalMensaje}
    tipo={modalTipo}
    textoAceptar={modalTextoAceptar}
  ></confirm-modal>
  <sidebar-nav
    titulo="Trámites de Grado"
    rol="Coordinación"
    {correo}
    seccion={seccion === "detalle" ? "solicitudes" : seccion}
    items={navItems}
    color="#0d1b4b"
  ></sidebar-nav>

  <div class="main-wrap">
    <!-- TOP BAR -->
    <div class="topbar">
      <div class="topbar-inner">
        <img src={shieldSrc} alt="Escudo CUL" class="topbar-escudo" />
        <div class="topbar-texts">
          <h1 class="topbar-titulo">
            {seccion === "solicitudes" ? "Solicitudes" :
             seccion === "detalle" ? "Detalle del trámite" :
             seccion === "ceremonias" ? "Ceremonias" : "Métricas de Gestión"}
          </h1>
          <span class="topbar-sub">Panel de Coordinación · {correo}</span>
        </div>
      </div>
    </div>

    <main class="contenido">
      {#if mensajeExito}
        <alert-message tipo="exito" mensaje={mensajeExito}></alert-message>
      {/if}
      {#if error}
        <alert-message tipo="error" mensaje={error}></alert-message>
      {/if}

      {#if cargando && seccion !== "estadisticas"}
        <loading-spinner mensaje="Cargando solicitudes..." color="#0d1b4b"></loading-spinner>

      {:else if seccion === "solicitudes"}
        <data-table
          columns={columnsTramites}
          rows={JSON.stringify(filasTramites)}
          ontableaction={onTableAction}
        ></data-table>

      {:else if seccion === "ceremonias"}
        {#if ceremonias.length > 0}
          <data-table
            columns={JSON.stringify([
              { key: "nombre", label: "Nombre" },
              { key: "fecha", label: "Fecha" },
              { key: "lugar", label: "Lugar" },
              { key: "horario", label: "Horario" },
              { key: "capacidad", label: "Capacidad" }
            ])}
          rows={JSON.stringify(filasCeremonias)}
          ></data-table>
        {:else}
          <div class="vacio">No hay ceremonias registradas.</div>
        {/if}

      {:else if seccion === "estadisticas"}
        <div class="bi-container">
          <iframe
            title="tramite_grado"
            src={powerBiUrl}
            frameborder="0"
            allowfullscreen={true}>
          </iframe>
        </div>
      {/if}
    </main>
  </div>
</div>

{#if modalDetalle && tramiteSeleccionado}
  <div class="modal-backdrop" role="presentation" onclick={() => modalDetalle = false}></div>
  <div class="modal-detalle" role="dialog" aria-modal="true" aria-labelledby="modal-detalle-titulo">
    <div class="modal-detalle-header">
      <h2 id="modal-detalle-titulo">Detalle del Trámite</h2>
      <button class="modal-close-btn" onclick={() => modalDetalle = false} aria-label="Cerrar">✕</button>
    </div>
    <div class="modal-detalle-body">
      <div class="section-card" style="margin-bottom:20px">
        <div class="section-card-header">Información del Estudiante</div>
        <div class="card-row">
          <span class="label">Estudiante</span>
          <span class="valor">{tramiteSeleccionado.nombre_estudiante || `ID: ${tramiteSeleccionado.id_estudiante}`}</span>
        </div>
        <div class="card-row">
          <span class="label">Documento</span>
          <span class="valor">{tramiteSeleccionado.documento_estudiante || "—"}</span>
        </div>
        <div class="card-row">
          <span class="label">Correo</span>
          <span class="valor">{tramiteSeleccionado.correo_estudiante || "—"}</span>
        </div>
        <div class="card-row">
          <span class="label">Estado trámite</span>
          <status-badge estado={tramiteSeleccionado.estado}></status-badge>
        </div>
        <div class="card-row">
          <span class="label">Estado pago</span>
          <status-badge estado={tramiteSeleccionado.estado_pago}></status-badge>
        </div>
        <div class="card-row">
          <span class="label">Paz y salvo</span>
          <div class="acciones-fila">
            <status-badge estado={tramiteSeleccionado.estado_paz}></status-badge>
            <button class="btn-accion verde" onclick={() => tramiteSeleccionado && actualizarPaz(tramiteSeleccionado.id_tramite_grado, "Aprobado")}>Aprobar</button>
            <button class="btn-accion rojo" onclick={() => tramiteSeleccionado && actualizarPaz(tramiteSeleccionado.id_tramite_grado, "Rechazado")}>Rechazar</button>
          </div>
        </div>
        <div class="card-row">
          <span class="label">Asignar ceremonia</span>
          <div class="acciones-fila">
            <select class="inp-select" bind:value={ceremoniaSeleccionada}>
              <option value="">Seleccionar...</option>
              {#each ceremonias as c}
                <option value={c.id_ceremonia_grado}>{c.nombre || c.fecha} — {c.lugar}</option>
              {/each}
            </select>
            <button class="btn-accion verde" onclick={() => tramiteSeleccionado && asignarCeremonia(tramiteSeleccionado.id_tramite_grado)}>Asignar</button>
          </div>
        </div>
      </div>

      <div class="section-card-header-standalone">Documentos entregados</div>
      {#if documentosTramite.length > 0}
        <data-table
          columns={columnsDocumentos}
          rows={JSON.stringify(filasDocumentos)}
          ontableaction={onTableAction}
        ></data-table>
      {:else}
        <div class="vacio">No hay documentos entregados.</div>
      {/if}
    </div>
  </div>
{/if}

<style>
  :host { display: block; font-family: Arial, Helvetica, sans-serif; min-height: 100vh; background: #f0f4ff; }

  .layout    { display: flex; min-height: 100vh; }
  .main-wrap { flex: 1; min-width: 0; display: flex; flex-direction: column; }

  /* TOP BAR */
  .topbar {
    background: linear-gradient(135deg, #0d1b4b 0%, #1a3a8f 70%, #E8920C 100%);
    padding: 18px 32px;
    border-bottom: 4px solid #E8920C;
  }
  .topbar-inner  { display: flex; align-items: center; gap: 16px; }
  .topbar-escudo { width: 52px; height: 52px; border-radius: 50%; object-fit: cover; box-shadow: 0 2px 6px rgba(0,0,0,0.4); }
  .topbar-texts  { display: flex; flex-direction: column; gap: 2px; }
  .topbar-titulo { font-size: 22px; font-weight: 700; color: white; margin: 0; }
  .topbar-sub    { font-size: 12px; color: rgba(255,255,255,0.75); }

  /* CONTENT */
  main.contenido { padding: 28px 32px; flex: 1; }

  .section-card {
    background: white;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(13,27,75,0.08);
    border-left: 4px solid #E8920C;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .section-card-header {
    font-size: 15px;
    font-weight: 700;
    color: #0d1b4b;
    padding-bottom: 10px;
    border-bottom: 1px solid #e8f0ff;
  }
  .section-card-header-standalone {
    font-size: 15px;
    font-weight: 700;
    color: #0d1b4b;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e8f0ff;
  }

  .card-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    border-bottom: 1px solid #f0f4ff;
    padding-bottom: 10px;
    flex-wrap: wrap;
    gap: 8px;
  }
  .card-row:last-child { border-bottom: none; padding-bottom: 0; }
  .label { color: #222222; font-weight: 500; }
  .valor { color: #0d1b4b; font-weight: 600; }

  .acciones-fila { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }

  .inp-select {
    padding: 8px 12px;
    border: 1.5px solid #cdd5e0;
    border-radius: 8px;
    font-size: 13px;
    background: #ffffff;
    color: #111111;
    cursor: pointer;
  }
  .inp-select:focus { outline: none; border-color: #0d1b4b; box-shadow: 0 0 0 3px rgba(13,27,75,0.1); }

  .bi-container {
    background: white;
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 2px 12px rgba(13,27,75,0.08);
    height: 80vh;
    width: 100%;
  }
  .bi-container iframe { width: 100%; height: 100%; border-radius: 8px; }

  .vacio {
    color: #64748b;
    padding: 40px;
    text-align: center;
    font-size: 15px;
    background: white;
    border-radius: 14px;
    box-shadow: 0 2px 12px rgba(13,27,75,0.08);
  }

  :global(.badge) { color: white; font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }
  :global(.btn-accion) { border: none; padding: 5px 12px; border-radius: 6px; font-size: 12px; cursor: pointer; color: white; font-weight: 600; }
  :global(.btn-accion.verde) { background: #22c55e; }
  :global(.btn-accion.rojo)  { background: #ef4444; }

  /* ===== MODAL DETALLE ===== */
  .modal-backdrop {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.45);
    backdrop-filter: blur(3px);
    z-index: 900;
    animation: fadeBg 0.18s ease;
  }
  @keyframes fadeBg { from { opacity: 0; } to { opacity: 1; } }

  .modal-detalle {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    z-index: 901;
    background: #ffffff;
    border-radius: 16px;
    width: min(700px, 96vw);
    max-height: 88vh;
    display: flex;
    flex-direction: column;
    box-shadow: 0 24px 48px rgba(13,27,75,0.18), 0 4px 12px rgba(13,27,75,0.10);
    border-top: 4px solid #E8920C;
    animation: popIn 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
    overflow: hidden;
  }
  @keyframes popIn {
    from { opacity: 0; transform: translate(-50%, -48%) scale(0.94); }
    to   { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  }

  .modal-detalle-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px 16px;
    border-bottom: 2px solid #e8f0ff;
    flex-shrink: 0;
  }
  .modal-detalle-header h2 {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #0d1b4b;
    margin: 0;
  }
  .modal-close-btn {
    background: none; border: none; cursor: pointer;
    font-size: 18px; color: #64748b; padding: 4px 8px;
    border-radius: 6px; transition: background 0.15s, color 0.15s;
  }
  .modal-close-btn:hover { background: #f0f4ff; color: #0d1b4b; }

  .modal-detalle-body {
    overflow-y: auto;
    padding: 20px 24px 24px;
    flex: 1;
  }

  @media (max-width: 768px) {
    .topbar { padding: 14px 16px; }
    main.contenido { padding: 16px; padding-top: 70px; }
    .section-card { max-width: 100%; padding: 16px; }
    .topbar-titulo { font-size: 17px; }
    .topbar-escudo { width: 40px; height: 40px; }
    .bi-container { height: 60vh; }
    .acciones-fila { flex-direction: column; align-items: flex-start; }
    .modal-detalle { width: 98vw; max-height: 95vh; }
    .modal-detalle-body { padding: 14px; }
  }
</style>
