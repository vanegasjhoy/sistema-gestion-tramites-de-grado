<svelte:options customElement="data-table" />

<script>
  let {
    columns = "[]",
    rows = "[]",
  } = $props();

  let parsedColumns = $derived((() => { try { return JSON.parse(columns); } catch { return []; } })());
  let parsedRows    = $derived((() => { try { return JSON.parse(rows);    } catch { return []; } })());

  let busqueda = $state("");
  let pagina   = $state(1);
  let porPagina = $state(10);
  let ordenCol  = $state("");
  let ordenDir  = $state("asc"); // asc o desc

  // Reset page when search or rows change
  $effect(() => { busqueda; parsedRows; pagina = 1; });

  // Strip HTML tags for searching/sorting
  function textoPlano(html) {
    if (!html) return "";
    return String(html).replace(/<[^>]*>/g, "").trim().toLowerCase();
  }

  let filasFiltradas = $derived((() => {
    let f = parsedRows;
    const q = busqueda.trim().toLowerCase();
    if (q) {
      f = f.filter(row =>
        parsedColumns.some(col => textoPlano(row[col.key] ?? "").includes(q))
      );
    }
    if (ordenCol) {
      const col = ordenCol;
      const dir = ordenDir;
      f = [...f].sort((a, b) => {
        const va = textoPlano(a[col] ?? "");
        const vb = textoPlano(b[col] ?? "");
        return dir === "asc" ? va.localeCompare(vb) : vb.localeCompare(va);
      });
    }
    return f;
  })());

  // Páginas a mostrar (con ellipsis)
  let paginas = $derived(
    Array.from({ length: totalPaginas }, (_, i) => i + 1).filter(p =>
      p === 1 || p === totalPaginas || Math.abs(p - paginaActual) <= 1
    )
  );

  let totalPaginas = $derived(Math.max(1, Math.ceil(filasFiltradas.length / porPagina)));
  let paginaActual = $derived(Math.min(pagina, totalPaginas));
  let filasPagina  = $derived(filasFiltradas.slice((paginaActual - 1) * porPagina, paginaActual * porPagina));

  function ordenar(col) {
    if (ordenCol === col) {
      ordenDir = ordenDir === "asc" ? "desc" : "asc";
    } else {
      ordenCol = col;
      ordenDir = "asc";
    }
  }

  function handleClick(e) {
    const btn = e.target.closest("[data-accion]");
    if (!btn) return;
    e.stopPropagation();
    const detail = { id: btn.dataset.id, accion: btn.dataset.accion };
    const host = btn.getRootNode()?.host;
    if (host) {
      host.dispatchEvent(new CustomEvent("tableaction", {
        detail,
        bubbles: true,
        composed: true
      }));
    }
    // Also dispatch to document so dashboards outside shadow DOM can listen
    document.dispatchEvent(new CustomEvent("tableaction", { detail }));
  }
</script>

<div class="wrapper">
  <!-- Controles superiores -->
  <div class="controles">
    <div class="mostrar">
      Mostrar
      <select bind:value={porPagina}>
        <option value={5}>5</option>
        <option value={10}>10</option>
        <option value={25}>25</option>
        <option value={50}>50</option>
      </select>
      entradas
    </div>
    <div class="buscar">
      Buscar:
      <input
        type="search"
        placeholder="Filtrar..."
        bind:value={busqueda}
      />
    </div>
  </div>

  <!-- Tabla -->
  <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
  <div class="tabla-scroll" role="presentation" onclick={handleClick}>
    <table>
      <thead>
        <tr>
          {#each parsedColumns as col}
            <th
              class:sortable={true}
              class:asc={ordenCol === col.key && ordenDir === "asc"}
              class:desc={ordenCol === col.key && ordenDir === "desc"}
              onclick={() => ordenar(col.key)}
            >
              {col.label}
              <span class="sort-icon">
                {#if ordenCol === col.key}
                  {ordenDir === "asc" ? "↑" : "↓"}
                {:else}
                  ↕
                {/if}
              </span>
            </th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#if filasPagina.length === 0}
          <tr>
            <td colspan={parsedColumns.length} class="vacio">
              {busqueda ? "Sin resultados para esa búsqueda." : "No hay datos."}
            </td>
          </tr>
        {:else}
          {#each filasPagina as row}
            <tr>
              {#each parsedColumns as col}
                <td>{@html row[col.key] ?? "—"}</td>
              {/each}
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>

  <!-- Pie: info + paginación -->
  <div class="pie">
    <span class="info-entradas">
      {#if filasFiltradas.length === 0}
        Sin entradas
      {:else}
        Mostrando {(paginaActual - 1) * porPagina + 1}–{Math.min(paginaActual * porPagina, filasFiltradas.length)} de {filasFiltradas.length}
        {#if busqueda} (filtrado de {parsedRows.length} total){/if}
      {/if}
    </span>
    <div class="paginacion">
      <button aria-label="Primera página" disabled={paginaActual <= 1} onclick={() => pagina = 1}>«</button>
      <button aria-label="Página anterior" disabled={paginaActual <= 1} onclick={() => pagina = paginaActual - 1}>‹</button>
      {#each paginas as p, i}
        {#if i > 0 && paginas[i - 1] !== p - 1}
          <span class="ellipsis">…</span>
        {/if}
        <button
          aria-label="Página {p}"
          class:current={p === paginaActual}
          onclick={() => pagina = p}
        >{p}</button>
      {/each}
      <button aria-label="Página siguiente" disabled={paginaActual >= totalPaginas} onclick={() => pagina = paginaActual + 1}>›</button>
      <button aria-label="Última página" disabled={paginaActual >= totalPaginas} onclick={() => pagina = totalPaginas}>»</button>
    </div>
  </div>
</div>

<style>
  :host { display: block; }

  .wrapper {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    overflow: hidden;
  }

  /* Controles */
  .controles {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    flex-wrap: wrap;
    gap: 8px;
    font-size: 13px;
    color: #475569;
  }
  .mostrar select {
    margin: 0 4px;
    padding: 3px 6px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 13px;
  }
  .buscar input {
    margin-left: 6px;
    padding: 5px 10px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 13px;
    outline: none;
    width: 180px;
  }
  .buscar input:focus { border-color: #94a3b8; }

  /* Tabla */
  .tabla-scroll { overflow-x: auto; }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  thead th {
    background: #f8fafc;
    color: #374151;
    font-weight: 600;
    text-align: left;
    padding: 10px 12px;
    border-bottom: 2px solid #e2e8f0;
    white-space: nowrap;
    user-select: none;
    cursor: pointer;
  }
  thead th:hover { background: #f1f5f9; }
  .sort-icon { font-size: 11px; color: #94a3b8; margin-left: 4px; }
  thead th.asc .sort-icon,
  thead th.desc .sort-icon { color: #3b82f6; }

  tbody tr { border-bottom: 1px solid #f1f5f9; }
  tbody tr:last-child { border-bottom: none; }
  tbody tr:hover { background: #f8fafc; }
  tbody td {
    padding: 10px 12px;
    vertical-align: middle;
    text-align: left;
    color: #1e293b;
  }
  .vacio { text-align: center; color: #94a3b8; padding: 32px; font-size: 14px; }

  /* Pie */
  .pie {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 14px;
    flex-wrap: wrap;
    gap: 8px;
  }
  .info-entradas { font-size: 12px; color: #64748b; }

  .paginacion { display: flex; gap: 4px; align-items: center; }
  .paginacion button {
    padding: 4px 10px;
    border: 1px solid #e2e8f0;
    background: white;
    border-radius: 6px;
    font-size: 13px;
    cursor: pointer;
    color: #1e293b;
    transition: background 0.15s;
    min-width: 32px;
  }
  .paginacion button:hover:not(:disabled):not(.current) { background: #f1f5f9; }
  .paginacion button.current { background: #3b82f6; color: white; border-color: #3b82f6; }
  .paginacion button:disabled { opacity: 0.35; cursor: default; }
  .ellipsis { color: #94a3b8; padding: 0 2px; font-size: 13px; }

  /* Badges y botones de acción (vienen como HTML crudo) */
  :global(.badge) {
    display: inline-block;
    color: white;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    line-height: 1.4;
    white-space: nowrap;
  }
  :global(.btn-accion) {
    border: none;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
    color: white;
    font-weight: 500;
    transition: opacity 0.15s;
  }
  :global(.btn-accion:hover) { opacity: 0.85; }
  :global(.btn-accion.rojo)  { background: #ef4444; }
  :global(.btn-accion.verde) { background: #16a34a; }
</style>
