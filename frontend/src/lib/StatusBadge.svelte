<svelte:options customElement="status-badge" />

<script>
  let { estado = "", tipo = "estado" } = $props();

  function color(e, t) {
    if (t === "activo") return e === "true" || e === true ? "#22c55e" : "#94a3b8";
    const positivos = ["Completado", "Pagado", "Aprobado", "Entregado", "Aprobada", "Activo"];
    const negativos = ["Cancelado", "Rechazado", "Inactivo"];
    if (positivos.includes(e)) return "#22c55e";
    if (negativos.includes(e)) return "#ef4444";
    return "#f59e0b";
  }

  let bg = $derived(color(estado, tipo));

  function getLabel(e, t) {
    if (t !== "activo") return e;
    return (e === "true" || e === true) ? "Activo" : "Inactivo";
  }

  let label = $derived(getLabel(estado, tipo));
</script>

<span class="badge" style="background:{bg}">{label}</span>

<style>
  :host { display: inline-block; }
  .badge {
    color: white;
    font-size: 12px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    white-space: nowrap;
    display: inline-block;
  }
</style>
