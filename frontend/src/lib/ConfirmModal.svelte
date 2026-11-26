<svelte:options customElement="confirm-modal" />

<script>
  let {
    titulo        = "¿Confirmar acción?",
    mensaje       = "",
    textoAceptar  = "Confirmar",
    textoCancelar = "Cancelar",
    tipo          = "peligro",
    visible       = false,
  } = $props();

  function aceptar() {
    if (window.__modal && typeof window.__modal.confirmar === "function") {
      window.__modal.confirmar();
    }
  }

  function cancelar() {
    if (window.__modal && typeof window.__modal.cancelar === "function") {
      window.__modal.cancelar();
    }
  }

  function onKeydown(e) {
    if (!visible) return;
    if (e.key === "Escape") cancelar();
    if (e.key === "Enter")  aceptar();
  }

  const colores = {
    peligro:     { btn: "#ef4444", hover: "#dc2626", ring: "rgba(239,68,68,0.18)" },
    advertencia: { btn: "#E8920C", hover: "#c97a08", ring: "rgba(232,146,12,0.18)" },
    info:        { btn: "#0d1b4b", hover: "#1a3a8f", ring: "rgba(13,27,75,0.18)" },
  };

  let cfg = $derived(colores[tipo] ?? colores.peligro);
</script>

<svelte:window onkeydown={onKeydown} />

{#if visible}
  <div class="backdrop" role="presentation" onclick={cancelar}></div>

  <div class="modal" role="alertdialog" aria-modal="true" aria-labelledby="modal-titulo">
    <h2 class="modal-titulo" id="modal-titulo">{titulo}</h2>

    {#if mensaje}
      <p class="modal-mensaje">{mensaje}</p>
    {/if}

    <div class="modal-acciones">
      <button class="btn-cancelar" onclick={cancelar}>{textoCancelar}</button>
      <button
        class="btn-confirmar"
        style="background:{cfg.btn}; --hover:{cfg.hover}; --ring:{cfg.ring};"
        onclick={aceptar}
      >{textoAceptar}</button>
    </div>
  </div>
{/if}

<style>
  :host { display: contents; }

  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(3px);
    z-index: 900;
    animation: fadeBg 0.18s ease;
  }

  @keyframes fadeBg {
    from { opacity: 0; }
    to   { opacity: 1; }
  }

  .modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 901;
    background: #ffffff;
    border-radius: 16px;
    padding: 36px 32px 28px;
    width: min(420px, 92vw);
    box-shadow: 0 24px 48px rgba(13,27,75,0.18), 0 4px 12px rgba(13,27,75,0.10);
    text-align: center;
    animation: popIn 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
    border-top: 4px solid #E8920C;
  }

  @keyframes popIn {
    from { opacity: 0; transform: translate(-50%, -48%) scale(0.94); }
    to   { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  }

  .modal-titulo {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #0d1b4b;
    margin: 0 0 10px;
    line-height: 1.3;
  }

  .modal-mensaje {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    color: #4b5563;
    margin: 0 0 24px;
    line-height: 1.55;
  }

  .modal-acciones {
    display: flex;
    gap: 10px;
    justify-content: center;
  }

  .btn-cancelar,
  .btn-confirmar {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    cursor: pointer;
    transition: background 0.18s, box-shadow 0.18s, transform 0.1s;
    min-width: 110px;
  }

  .btn-cancelar { background: #2d3148; color: #cbd5e1; }
  .btn-cancelar:hover { background: #3a4060; }
  .btn-cancelar:active { transform: scale(0.97); }

  .btn-confirmar { color: #ffffff; }
  .btn-confirmar:hover {
    background: var(--hover) !important;
    box-shadow: 0 0 0 4px var(--ring);
  }
  .btn-confirmar:active { transform: scale(0.97); }
</style>
