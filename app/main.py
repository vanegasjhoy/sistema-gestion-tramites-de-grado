from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ===== IMPORTAR ROUTERS =====
from app.routes.estudiante_routes import router as estudiante_router
from app.routes.documento_requerido_routes import router as documento_requerido_router
from app.routes.facultad_routes import router as facultad_router
from app.routes.programa_routes import router as programa_router
from app.routes.tramite_grado_routes import router as tramite_grado_router
from app.routes.tipo_grado_routes import router as tipo_grado_router
from app.routes.ceremonia_grado_routes import router as ceremonia_grado_router
from app.routes.asignacion_ceremonia_routes import router as asignacion_ceremonia_router
from app.routes.tipo_documento_routes import router as tipo_documento_router
from app.routes.entrega_documento_routes import router as entrega_documentos_router
from app.routes.tipo_paz_ysalvo_routes import router as tipo_paz_ysalvo_router
from app.routes.usuario_routes import router as usuario_router
from app.routes.reporte_routes import router as reporte_router

# ===== APP =====
from fastapi.security import HTTPBearer

security = HTTPBearer()

app = FastAPI(
    title="Sistema de Gestión de Trámites de Grado",
    description="API para gestión de trámites de grado universitario",
    version="1.0.0"
)

# ===== CORS (MUY IMPORTANTE PARA SVELTE) =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://tu-app.netlify.app"  # SVELTE
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== RUTA PRINCIPAL =====
@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente 🚀"}

# ===== ROUTERS =====
app.include_router(usuario_router)           # ← NUEVO (primero para que /login sea accesible)
app.include_router(estudiante_router)
app.include_router(documento_requerido_router)
app.include_router(facultad_router)
app.include_router(programa_router)
app.include_router(tramite_grado_router)
app.include_router(tipo_grado_router)
app.include_router(ceremonia_grado_router)
app.include_router(asignacion_ceremonia_router)
app.include_router(tipo_documento_router)
app.include_router(entrega_documentos_router)
app.include_router(tipo_paz_ysalvo_router)
app.include_router(reporte_router)

# ===== EJECUCIÓN =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)