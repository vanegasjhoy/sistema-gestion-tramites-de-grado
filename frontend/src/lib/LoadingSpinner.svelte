<svelte:options customElement="loading-spinner" />

<script>
  let { mensaje = "Cargando...", color = "#0d6efd" } = $props();
</script>

<div class="contenedor">
  <div class="spinner" style="border-top-color:{color}"></div>
  <p class="texto">{mensaje}</p>
</div>

<style>
  :host { display: block; }
  .contenedor {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 40px;
    gap: 16px;
  }
  .spinner {
    width: 36px;
    height: 36px;
    border: 3px solid #e2e8f0;
    border-top-color: #0d6efd;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .texto {
    color: #64748b;
    font-size: 15px;
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
  }
</style>
