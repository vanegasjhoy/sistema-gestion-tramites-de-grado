<svelte:options customElement="sidebar-nav" />

<script>
  let {
    titulo = "Trámites de Grado",
    rol = "",
    correo = "",
    seccion = "",
    items = "[]",
    color = "#0d1b4b"
  } = $props();

  let parsedItems = $derived((() => { try { return JSON.parse(items); } catch { return []; } })());
  let menuAbierto = $state(false);

  function navClick(value) {
    menuAbierto = false;
    // Despachar solo al document para evitar eventos duplicados.
    // Los dashboards escuchan navchange en document vía onMount.
    document.dispatchEvent(new CustomEvent("navchange", { detail: { value } }));
  }

  let modalLogoutVisible = $state(false);

  function cerrarSesion() {
    modalLogoutVisible = true;
    requestAnimationFrame(() => {
      window.__modal = {
        confirmar: () => { modalLogoutVisible = false; localStorage.clear(); window.location.href = "index.html"; },
        cancelar:  () => { modalLogoutVisible = false; },
      };
    });
  }
</script>

<confirm-modal
  visible={modalLogoutVisible}
  titulo="¿Cerrar sesión?"
  mensaje="Se cerrará tu sesión y serás redirigido al inicio. ¿Deseas continuar?"
  tipo="advertencia"
  textoAceptar="Cerrar sesión"
  textoCancelar="Cancelar"
></confirm-modal>

<button class="hamburger" aria-label="Abrir menú" style="background:{color}" onclick={() => menuAbierto = !menuAbierto}>
  {menuAbierto ? "✕" : "☰"}
</button>

{#if menuAbierto}
  <button class="overlay" onclick={() => menuAbierto = false} aria-label="Cerrar menú"></button>
{/if}

<aside class="sidebar" class:abierto={menuAbierto} style="background:{color}">
  <div class="sidebar-header">
    <!-- Escudo CUL -->
    <div class="escudo-wrap">
      <img
        src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Escudo_CUL.png/200px-Escudo_CUL.png"
        alt="CUL"
        class="escudo-circulo"
        onerror={(e) => { e.target.style.display='none'; }}
      />
    </div>
    <h2>{titulo}</h2>
    {#if rol}<p class="rol-badge">{rol}</p>{/if}
    {#if correo}<p class="correo-badge">{correo}</p>{/if}
  </div>
  <nav>
    {#each parsedItems as item}
      <button
        aria-label={item.label}
        class:active={seccion === item.value}
        onclick={() => navClick(item.value)}
      >{item.label}</button>
    {/each}
  </nav>
  <button class="btn-cerrar" onclick={cerrarSesion}>Cerrar sesión</button>
</aside>

<style>
  :host { display: block; }
  .hamburger { display: none; position: fixed; top: 12px; left: 12px; z-index: 200; color: white; border: none; border-radius: 8px; width: 40px; height: 40px; font-size: 18px; cursor: pointer; }
  .sidebar { width: 240px; color: white; display: flex; flex-direction: column; padding: 24px 16px; gap: 8px; flex-shrink: 0; height: 100vh; position: sticky; top: 0; border-right: 3px solid #E8920C; }
  .escudo-wrap { display: flex; justify-content: center; margin-bottom: 10px; }
  .escudo-circulo { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; border: 3px solid #E8920C; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.35); display: block; }
  .sidebar-header h2 { font-size: 15px; margin-bottom: 4px; font-weight: 700; color: white; text-align: center; }
  .rol-badge { background: #E8920C; display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; margin-bottom: 8px; color: white; font-weight: 600; }
  .correo-badge { font-size: 11px; color: rgba(255,255,255,0.75); margin-bottom: 16px; word-break: break-all; }
  nav { display: flex; flex-direction: column; gap: 6px; flex: 1; }
  nav button { background: transparent; border: none; color: rgba(255,255,255,0.85); text-align: left; padding: 10px 12px; border-radius: 8px; font-size: 14px; cursor: pointer; transition: 0.2s; width: 100%; font-weight: 500; }
  nav button:hover, nav button.active { background: #E8920C; color: white; font-weight: 700; }
  .btn-cerrar { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.25); color: white; padding: 10px; border-radius: 8px; cursor: pointer; font-size: 14px; width: 100%; }
  .btn-cerrar:hover { background: rgba(255,255,255,0.2); }
  .overlay { display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 100; border: none; cursor: pointer; padding: 0; }

  @media (max-width: 768px) {
    .hamburger { display: flex; align-items: center; justify-content: center; }
    .sidebar { position: fixed; top: 0; left: -280px; width: 260px; z-index: 150; transition: left 0.3s ease; padding-top: 60px; }
    .sidebar.abierto { left: 0; }
  }
</style>
