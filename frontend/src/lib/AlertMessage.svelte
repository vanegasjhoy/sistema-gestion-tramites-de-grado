<svelte:options customElement="alert-message" />

<script>
  let { tipo = "info", mensaje = "", visible = $bindable(true) } = $props();

  function config(t) {
    if (t === "exito") return { bg: "#dcfce7", color: "#166534", icon: "✅" };
    if (t === "error") return { bg: "#fee2e2", color: "#b91c1c", icon: "❌" };
    if (t === "advertencia") return { bg: "#fef3c7", color: "#92400e", icon: "⚠️" };
    return { bg: "#eff6ff", color: "#1e40af", icon: "ℹ️" };
  }

  let cfg = $derived(config(tipo));

  function cerrar() { visible = false; }
</script>

{#if visible && mensaje}
  <div class="alerta" style="background:{cfg.bg};color:{cfg.color}">
    <span class="icon">{cfg.icon}</span>
    <span class="txt">{mensaje}</span>
    <button class="cerrar" onclick={cerrar} style="color:{cfg.color}">✕</button>
  </div>
{/if}

<style>
  :host { display: block; }
  .alerta {
    display: flex;
    align-items: center;
    gap: 10px;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    font-family: 'Segoe UI', system-ui, sans-serif;
    animation: fadeIn 0.3s ease;
  }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  .icon { font-size: 16px; flex-shrink: 0; }
  .txt { flex: 1; line-height: 1.4; }
  .cerrar { background: none; border: none; font-size: 14px; cursor: pointer; padding: 0; margin-left: auto; opacity: 0.7; flex-shrink: 0; }
  .cerrar:hover { opacity: 1; }
</style>
