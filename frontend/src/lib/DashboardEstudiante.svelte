<svelte:options customElement="dashboard-estudiante" />

<script>
  const API = "http://127.0.0.1:8000";
  const shieldSrc = "data:image/png;base64,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";
  let token = localStorage.getItem("token");
  let correo = localStorage.getItem("correo");
  let idEstudiante = localStorage.getItem("id_estudiante");
  if (!token || localStorage.getItem("rol") !== "estudiante") window.location.href = "index.html";

  const headers = { "Content-Type": "application/json", Authorization: `Bearer ${token}` };

  let seccion = $state("tramite");
  let tramite = $state(null);
  let ceremonia = $state(null);
  let tiposGrado = $state([]);
  let documentosRequeridos = $state([]);
  let entregasDocumentos = $state([]);
  let cargando = $state(true);
  let error = $state("");

  let mostrarFormTramite = $state(false);
  let formTramite = $state({ id_tipo_grado: "", fecha_inicio: "" });
  let enviandoTramite = $state(false);
  let mensajeTramite = $state("");

  let mostrarFormEntrega = $state(false);
  let formEntrega = $state({ id_documento_requerido: "" });
  let enviandoEntrega = $state(false);
  let mensajeEntrega = $state("");

  async function cargarDatos() {
    cargando = true; error = "";
    try {
      const resTG = await fetch(`${API}/get_tipos_grado/`, { headers });
      if (resTG.ok) { const d = await resTG.json(); tiposGrado = d.resultado || []; }

      tramite = null;
      const resTramite = await fetch(`${API}/tramites_grado`, { headers });
      if (resTramite.ok) {
        const d = await resTramite.json();
        // La ruta ya filtra por estudiante cuando el rol es "estudiante"
        const lista = d.resultado || [];
        tramite = lista[0] || null;
        if (tramite?.id_tramite_grado) localStorage.setItem("id_tramite_grado", tramite.id_tramite_grado);
      }

      if (tramite) {
        await cargarEntregas();
        try {
          const resCer = await fetch(`${API}/tramites_grado/${tramite.id_tramite_grado}/ceremonia`, { headers });
          if (resCer.ok) {
            const d = await resCer.json();
            const raw = d.resultado?.[0] || d[0] || null;
            if (raw && typeof raw === "object") {
              if (raw.nombre || raw.fecha || raw.lugar || raw.horario) {
                ceremonia = raw;
              } else if (raw.id_ceremonia_grado) {
                const resCer2 = await fetch(`${API}/ceremonias/${raw.id_ceremonia_grado}`, { headers });
                if (resCer2.ok) {
                  const d2 = await resCer2.json();
                  ceremonia = d2.resultado || d2;
                } else {
                  ceremonia = raw;
                }
              } else {
                ceremonia = raw;
              }
            } else {
              ceremonia = null;
            }
          } else {
            ceremonia = null;
          }
        } catch { ceremonia = null; }
      }

      const resDoc = await fetch(`${API}/get_documentos_requeridos/`, { headers });
      if (resDoc.ok) { const d = await resDoc.json(); documentosRequeridos = d.resultado || []; }

    } catch (e) {
      error = "Error al cargar los datos. Verifica tu conexión.";
    } finally {
      cargando = false;
    }
  }

  async function cargarEntregas() {
    if (!tramite) return;
    try {
      const res = await fetch(`${API}/tramites_grado/${tramite.id_tramite_grado}/entregas`, { headers });
      if (res.ok) { const d = await res.json(); entregasDocumentos = d.resultado || []; }
      else entregasDocumentos = [];
    } catch { entregasDocumentos = []; }
  }

  async function crearTramite() {
    if (!formTramite.id_tipo_grado) { mensajeTramite = "Selecciona un tipo de grado."; return; }
    enviandoTramite = true; mensajeTramite = "";
    try {
      const body = {
        id_estudiante: parseInt(idEstudiante),
        id_tipo_grado: parseInt(formTramite.id_tipo_grado),
        fecha_inicio: formTramite.fecha_inicio || new Date().toISOString().split("T")[0],
        estado: "En Proceso", estado_pago: "Pendiente", estado_paz: "Pendiente"
      };
      const res = await fetch(`${API}/tramites_grado`, { method: "POST", headers, body: JSON.stringify(body) });
      const data = await res.json();
      if (res.ok) {
        if (data.id_tramite_grado) localStorage.setItem("id_tramite_grado", data.id_tramite_grado);
        mensajeTramite = "✅ Trámite iniciado correctamente.";
        mostrarFormTramite = false;
        formTramite = { id_tipo_grado: "", fecha_inicio: "" };
        await cargarDatos();
      } else {
        mensajeTramite = data.detail || "Error al crear el trámite.";
      }
    } catch { mensajeTramite = "Error de conexión."; }
    finally { enviandoTramite = false; }
  }

  async function entregarDocumento() {
    if (!formEntrega.id_documento_requerido) { mensajeEntrega = "Selecciona un documento."; return; }
    enviandoEntrega = true; mensajeEntrega = "";
    try {
      const body = {
        id_tramite_grado: tramite.id_tramite_grado,
        id_estudiante: parseInt(idEstudiante),
        id_documento_requerido: parseInt(formEntrega.id_documento_requerido),
        fecha_entrega: new Date().toISOString().split("T")[0],
        estado: "Pendiente"
      };
      const res = await fetch(`${API}/entregas_documentos`, { method: "POST", headers, body: JSON.stringify(body) });
      const data = await res.json();
      if (res.ok) {
        mensajeEntrega = "✅ Documento registrado como entregado.";
        mostrarFormEntrega = false;
        formEntrega = { id_documento_requerido: "" };
        await cargarEntregas();
      } else {
        mensajeEntrega = data.detail || "Error al registrar entrega.";
      }
    } catch { mensajeEntrega = "Error de conexión."; }
    finally { enviandoEntrega = false; }
  }

  function cambiarSeccion(s) { seccion = s; }
  function onNavChange(e) { cambiarSeccion(e.detail.value); }

  function nombreTipoGrado(id) {
    const t = tiposGrado.find(t => t.id_tipo_grado === id);
    return t ? t.nombre : `Tipo ${id}`;
  }

  function nombreDocumento(id) {
    const d = documentosRequeridos.find(d => d.id_documento_requerido === id);
    return d ? d.nombre : `Documento ${id}`;
  }

  function rowsEntregas() {
    return entregasDocumentos.map(e => ({
      nombre: nombreDocumento(e.id_documento_requerido),
      fecha: e.fecha_entrega || "—",
      estado: `<span class="badge" style="background:${colorBadge(e.estado)};color:white;font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px">${e.estado}</span>`
    }));
  }

  function rowsPendientes() {
    return documentosPendientes().map(d => ({
      nombre: d.nombre,
      estado: `<span class="badge" style="background:#f59e0b;color:white;font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px">Pendiente</span>`
    }));
  }

  function colorBadge(estado) {
    if (["Pagado","Aprobado","Entregado","Completado"].includes(estado)) return "#22c55e";
    if (["Rechazado","Cancelado"].includes(estado)) return "#ef4444";
    return "#f59e0b";
  }

  const columnsEntregas = JSON.stringify([
    { key: "nombre", label: "Documento" },
    { key: "fecha",  label: "Fecha entrega" },
    { key: "estado", label: "Estado" }
  ]);

  const columnsPendientes = JSON.stringify([
    { key: "nombre", label: "Documento" },
    { key: "estado", label: "Estado" }
  ]);

  function documentosPendientes() {
    const yaEntregados = entregasDocumentos.map(e => e.id_documento_requerido);
    return documentosRequeridos.filter(d => !yaEntregados.includes(d.id_documento_requerido));
  }

  let navItems = JSON.stringify([
    { label: "Mi Trámite",  value: "tramite"    },
    { label: "Documentos", value: "documentos" },
    { label: "Paz y Salvo",value: "paz"        },
    { label: "Ceremonia",  value: "ceremonia"  }
  ]);

  cargarDatos();
</script>

<svelte:document on:navchange={onNavChange} />

<div class="layout">
  <sidebar-nav
    titulo="Trámites de Grado"
    rol="Estudiante"
    {correo}
    {seccion}
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
            {seccion === "tramite" ? "Mi Trámite" :
             seccion === "documentos" ? "Documentos" :
             seccion === "paz" ? "Paz y Salvo" : "Ceremonia de Grado"}
          </h1>
          <span class="topbar-sub">Estudiante · {correo}</span>
        </div>
      </div>
    </div>

    <main class="contenido">
      {#if cargando}
        <loading-spinner mensaje="Cargando información..." color="#0d1b4b"></loading-spinner>
      {:else if error}
        <alert-message tipo="error" mensaje={error}></alert-message>
      {:else}

        <!-- MI TRÁMITE -->
        {#if seccion === "tramite"}
          {#if tramite}
            <div class="hero-card">
              <div class="hero-info">
                <span class="hero-correo">{correo}</span>
                <div class="hero-meta">
                  <span>{nombreTipoGrado(tramite.id_tipo_grado)}</span>
                  <span class="sep">·</span>
                  <span>{tramite.fecha_inicio || "—"}</span>
                </div>
              </div>
              <div class="hero-badges">
                <status-badge estado={tramite.estado}></status-badge>
                <status-badge estado={tramite.estado_pago}></status-badge>
                <status-badge estado={tramite.estado_paz}></status-badge>
              </div>
            </div>

            <div class="section-card" style="margin-top:16px">
              <div class="section-card-header">Información del Trámite</div>
              <div class="card-row"><span class="label">Estado</span><status-badge estado={tramite.estado}></status-badge></div>
              <div class="card-row"><span class="label">Tipo de grado</span><span class="valor">{nombreTipoGrado(tramite.id_tipo_grado)}</span></div>
              <div class="card-row"><span class="label">Fecha de inicio</span><span class="valor">{tramite.fecha_inicio || "—"}</span></div>
              <div class="card-row"><span class="label">Fecha de fin</span><span class="valor">{tramite.fecha_fin || "Pendiente"}</span></div>
              <div class="card-row"><span class="label">Monto</span><span class="valor">{tramite.monto ? `$${Number(tramite.monto).toLocaleString("es-CO")}` : "—"}</span></div>
              <div class="card-row"><span class="label">Estado de pago</span><status-badge estado={tramite.estado_pago}></status-badge></div>
            </div>

            <div class="section-card" style="margin-top:16px;max-width:100%">
              <div class="section-card-header-row">
                <span class="section-card-header" style="border:none;padding:0">Documentos entregados ({entregasDocumentos.length})</span>
                <button class="btn-primario btn-sm" onclick={() => { cambiarSeccion("documentos"); mensajeEntrega = ""; }}>+ Registrar entrega</button>
              </div>
              {#if entregasDocumentos.length > 0}
                <data-table columns={columnsEntregas} rows={JSON.stringify(rowsEntregas())}></data-table>
              {:else}
                <p class="sin-docs">Aún no has entregado documentos. <button class="link-btn" onclick={() => cambiarSeccion("documentos")}>Ir a Documentos</button></p>
              {/if}
            </div>

            {#if mensajeTramite}
              <alert-message tipo={mensajeTramite.startsWith("✅") ? "exito" : "error"} mensaje={mensajeTramite}></alert-message>
            {/if}

          {:else}
            <div class="vacio-card">
              <p class="vacio-titulo">No tienes un trámite de grado activo</p>
              <p class="vacio-desc">Para iniciar tu proceso de grado, haz clic en el botón de abajo.</p>
              {#if !mostrarFormTramite}
                <button class="btn-primario" onclick={() => { mostrarFormTramite = true; mensajeTramite = ""; }}>+ Iniciar trámite de grado</button>
              {:else}
                <div class="form-card">
                  <div class="form-titulo">Nuevo trámite de grado</div>
                  <label class="form-label" for="tipo_grado">Tipo de grado *</label>
                  <select id="tipo_grado" class="form-select" bind:value={formTramite.id_tipo_grado}>
                    <option value="">-- Selecciona --</option>
                    {#each tiposGrado as tg}
                      <option value={tg.id_tipo_grado}>{tg.nombre}</option>
                    {/each}
                  </select>
                  <label class="form-label" for="fecha_inicio">Fecha de inicio</label>
                  <input id="fecha_inicio" type="date" class="form-input" bind:value={formTramite.fecha_inicio} />
                  {#if mensajeTramite}
                    <alert-message tipo={mensajeTramite.startsWith("✅") ? "exito" : "error"} mensaje={mensajeTramite}></alert-message>
                  {/if}
                  <div class="form-acciones">
                    <button class="btn-secundario" onclick={() => { mostrarFormTramite = false; mensajeTramite = ""; }}>Cancelar</button>
                    <button class="btn-primario" onclick={crearTramite} disabled={enviandoTramite}>{enviandoTramite ? "Enviando..." : "Confirmar"}</button>
                  </div>
                </div>
              {/if}
            </div>
          {/if}
        {/if}

        <!-- DOCUMENTOS -->
        {#if seccion === "documentos"}
          {#if !tramite}
            <div class="vacio-card">
              <p class="vacio-titulo">Primero debes iniciar un trámite</p>
              <button class="btn-primario" onclick={() => cambiarSeccion("tramite")}>Ir a Mi Trámite</button>
            </div>
          {:else}
            {#if entregasDocumentos.length > 0}
              <div class="section-card" style="max-width:100%">
                <div class="section-card-header">Documentos entregados</div>
                <data-table columns={columnsEntregas} rows={JSON.stringify(rowsEntregas())}></data-table>
              </div>
            {/if}
            {#if documentosPendientes().length > 0}
              <div class="section-card" style="margin-top:16px;max-width:100%">
                <div class="section-card-header">Documentos pendientes</div>
                <data-table columns={columnsPendientes} rows={JSON.stringify(rowsPendientes())}></data-table>
              </div>
            {/if}
            {#if !mostrarFormEntrega}
              <button class="btn-primario" style="margin-top:20px" onclick={() => { mostrarFormEntrega = true; mensajeEntrega = ""; }}>+ Registrar entrega de documento</button>
            {:else}
              <div class="form-card" style="margin-top:16px">
                <div class="form-titulo">Registrar entrega</div>
                <label class="form-label" for="doc_req">Documento *</label>
                <select id="doc_req" class="form-select" bind:value={formEntrega.id_documento_requerido}>
                  <option value="">-- Selecciona --</option>
                  {#each documentosRequeridos as doc}
                    <option value={doc.id_documento_requerido}>{doc.nombre}</option>
                  {/each}
                </select>
                {#if mensajeEntrega}
                  <alert-message tipo={mensajeEntrega.startsWith("✅") ? "exito" : "error"} mensaje={mensajeEntrega}></alert-message>
                {/if}
                <div class="form-acciones">
                  <button class="btn-secundario" onclick={() => { mostrarFormEntrega = false; mensajeEntrega = ""; }}>Cancelar</button>
                  <button class="btn-primario" onclick={entregarDocumento} disabled={enviandoEntrega}>{enviandoEntrega ? "Registrando..." : "Confirmar entrega"}</button>
                </div>
              </div>
            {/if}
          {/if}
        {/if}

        <!-- PAZ Y SALVO -->
        {#if seccion === "paz"}
          {#if tramite}
            {#if tramite.estado_paz === "Aprobado"}
              <div class="info-box success">¡Tu paz y salvo ha sido aprobado!</div>
            {:else if tramite.estado_paz === "Rechazado"}
              <div class="info-box error">Tu paz y salvo fue rechazado. Contacta a la coordinación.</div>
            {:else}
              <div class="info-box">Tu paz y salvo está siendo revisado por la coordinación.</div>
            {/if}
            <div class="section-card" style="max-width:100%;margin-top:16px">
              <div class="section-card-header">Estado de Paz y Salvo</div>
              <data-table
                columns={JSON.stringify([{ key: "campo", label: "Detalle" }, { key: "valor", label: "" }])}
                rows={JSON.stringify([
                  { campo: "Estado", valor: `<span style="background:${tramite.estado_paz === 'Aprobado' ? '#22c55e' : tramite.estado_paz === 'Rechazado' ? '#ef4444' : '#f59e0b'};color:white;font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px">${tramite.estado_paz || 'Pendiente'}</span>` },
                  { campo: "Fecha de aprobación", valor: tramite.fecha_aprobacion_paz || "Pendiente" }
                ])}
              ></data-table>
            </div>
          {:else}
            <div class="vacio-card">
              <p class="vacio-titulo">Sin trámite activo</p>
              <button class="btn-primario" onclick={() => cambiarSeccion("tramite")}>Ir a Mi Trámite</button>
            </div>
          {/if}
        {/if}

        <!-- CEREMONIA -->
        {#if seccion === "ceremonia"}
          {#if ceremonia}
            <div class="info-box success" style="margin-bottom:20px">¡Estás asignado a una ceremonia de grado!</div>
            <div class="section-card" style="max-width:100%">
              <div class="section-card-header">Ceremonia de Grado</div>
              <data-table
                columns={JSON.stringify([{ key: "campo", label: "Detalle" }, { key: "valor", label: "" }])}
                rows={JSON.stringify([
                  { campo: "Nombre",    valor: ceremonia.nombre  || "Por confirmar" },
                  { campo: "Fecha",     valor: ceremonia.fecha ? new Date(ceremonia.fecha + "T00:00:00").toLocaleDateString("es-CO", { year:"numeric", month:"long", day:"numeric" }) : "Por confirmar" },
                  { campo: "Lugar",     valor: ceremonia.lugar   || "Por confirmar" },
                  { campo: "Horario",   valor: ceremonia.horario || "Por confirmar" },
                  { campo: "Capacidad", valor: ceremonia.capacidad ? `${ceremonia.capacidad} personas` : "Por confirmar" }
                ])}
              ></data-table>
            </div>
          {:else}
            <div class="vacio-card">
              <p class="vacio-titulo">{tramite ? "Ceremonia aún no asignada" : "Sin trámite activo"}</p>
              <p class="vacio-desc">{tramite ? "La coordinación asignará una ceremonia cuando tu trámite esté completo." : "Primero debes iniciar un trámite de grado."}</p>
              {#if !tramite}
                <button class="btn-primario" onclick={() => cambiarSeccion("tramite")}>Ir a Mi Trámite</button>
              {/if}
            </div>
          {/if}
        {/if}

      {/if}
    </main>
  </div>
</div>

<style>
  :host { display: block; font-family: Arial, Helvetica, sans-serif; min-height: 100vh; background: #f0f4ff; }
  .layout    { display: flex; min-height: 100vh; }
  .main-wrap { flex: 1; min-width: 0; display: flex; flex-direction: column; }

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

  .contenido { padding: 28px 32px; flex: 1; }

  .hero-card { background: white; border-radius: 14px; padding: 20px 24px; box-shadow: 0 2px 12px rgba(13,27,75,0.08); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; border-left: 4px solid #E8920C; }
  .hero-info  { display: flex; flex-direction: column; gap: 4px; }
  .hero-correo { font-size: 15px; font-weight: 700; color: #0d1b4b; }
  .hero-meta   { font-size: 13px; color: #222222; display: flex; gap: 6px; align-items: center; }
  .sep { color: #cbd5e1; }
  .hero-badges { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }

  .section-card {
    background: white;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(13,27,75,0.08);
    border-left: 4px solid #E8920C;
    max-width: 560px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .section-card-header { font-size: 15px; font-weight: 700; color: #0d1b4b; padding-bottom: 10px; border-bottom: 1px solid #e8f0ff; }
  .section-card-header-row { display: flex; justify-content: space-between; align-items: center; padding-bottom: 10px; border-bottom: 1px solid #e8f0ff; flex-wrap: wrap; gap: 8px; }

  .card-row { display: flex; justify-content: space-between; align-items: center; font-size: 14px; border-bottom: 1px solid #f0f4ff; padding-bottom: 10px; flex-wrap: wrap; gap: 8px; }
  .card-row:last-child { border-bottom: none; padding-bottom: 0; }
  .label { color: #222222; font-weight: 500; }
  .valor { color: #0d1b4b; font-weight: 600; }

  .vacio-card { background: white; border-radius: 16px; padding: 48px 32px; max-width: 480px; text-align: center; box-shadow: 0 2px 12px rgba(13,27,75,0.08); border-top: 4px solid #E8920C; }
  .vacio-titulo { font-size: 18px; font-weight: 700; color: #0d1b4b; margin: 0 0 8px; }
  .vacio-desc   { font-size: 14px; color: #333333; margin: 0 0 24px; line-height: 1.6; }

  .form-card { background: white; border-radius: 14px; padding: 24px; box-shadow: 0 2px 12px rgba(13,27,75,0.08); max-width: 480px; display: flex; flex-direction: column; gap: 12px; border-left: 4px solid #E8920C; }
  .form-titulo { font-size: 15px; font-weight: 700; color: #0d1b4b; }
  .form-label  { font-size: 13px; color: #222222; font-weight: 600; }

  .form-select, .form-input {
    width: 100%; padding: 10px 12px; border: 1.5px solid #cdd5e0; border-radius: 8px;
    font-size: 14px; background: #ffffff; box-sizing: border-box;
    color: #111111; -webkit-text-fill-color: #111111;
  }
  .form-select { appearance: none; -webkit-appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%230d1b4b' d='M6 8L1 3h10z'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; padding-right: 36px; cursor: pointer; }
  .form-select:focus, .form-input:focus { outline: none; border-color: #0d1b4b; box-shadow: 0 0 0 3px rgba(13,27,75,0.1); }

  .form-acciones { display: flex; gap: 10px; margin-top: 4px; }
  .btn-primario { background: #E8920C; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; transition: background 0.2s; }
  .btn-primario:hover:not(:disabled) { background: #c97a08; }
  .btn-primario:disabled { opacity: 0.6; cursor: not-allowed; }
  .btn-sm { padding: 6px 14px; font-size: 13px; }
  .btn-secundario { background: #f0f4ff; color: #0d1b4b; border: none; padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }
  .sin-docs { font-size: 14px; color: #333333; padding: 12px 0; margin: 0; }
  .link-btn { background: none; border: none; color: #0d1b4b; font-size: 14px; cursor: pointer; padding: 0; text-decoration: underline; font-weight: 600; }

  .info-box { background: #e8f0ff; color: #0d1b4b; border-radius: 10px; padding: 14px 18px; font-size: 14px; font-weight: 600; max-width: 560px; border-left: 4px solid #0d1b4b; }
  .info-box.success { background: #dcfce7; color: #166534; border-left-color: #22c55e; }
  .info-box.error   { background: #fee2e2; color: #b91c1c; border-left-color: #ef4444; }

  @media (max-width: 768px) {
    .topbar { padding: 14px 16px; }
    .contenido { padding: 16px; padding-top: 70px; }
    .section-card, .vacio-card, .form-card, .hero-card { max-width: 100%; padding: 16px; }
    .form-acciones { flex-direction: column; }
    .hero-card { flex-direction: column; align-items: flex-start; }
    .topbar-titulo { font-size: 17px; }
    .topbar-escudo { width: 40px; height: 40px; }
  }
</style>
