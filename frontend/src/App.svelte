<script>
  let mensaje = "Cargando...";

  async function obtenerMensaje() {
    const respuesta = await fetch("http://127.0.0.1:8000/mensaje");
    const data = await respuesta.json();
    mensaje = data.mensaje;
  }

  obtenerMensaje();
</script>

<main>
  <h1>Sistema de Gestión de Trámites de Grado</h1>
  <h2>{mensaje}</h2>
</main>