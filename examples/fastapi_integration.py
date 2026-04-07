import sys
from pathlib import Path
# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent))

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from b1sl.b1sl import AsyncB1Client, B1Environment
from b1sl.b1sl.base_adapter import ObservabilityConfig, HookContext

# 1. Configuración Global (desde .env)
# Utiliza B1Environment para cargar las variables del sistema (como en Item.py)
env = B1Environment.load()
config = env.config

# 1.5. Configuración de Observabilidad (Opcional)
# Registramos un hook para monitorear el performance en los logs.
def monitor_performance(ctx: HookContext):
    if ctx.duration_ms > 500:
        print(f"⚠️ Alerta de Performance: {ctx.http_method} {ctx.endpoint} tardó {ctx.duration_ms:.1f}ms")

obs = ObservabilityConfig(
    hooks={"on_response": [monitor_performance]},
    context_extras={"service": "fastapi-demo"}
)

# 2. Contenedor del Cliente en el estado de la App
# Esto permite que el cliente viva durante todo el ciclo de vida del proceso.
class AppState:
    b1: AsyncB1Client = None

state = AppState()

# 3. Lifespan de FastAPI
# Aquí gestionamos el Login al arrancar y el Logout al cerrar.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # --- Startup ---
    print("Iniciando conexión con SAP B1...")
    async with AsyncB1Client(config, observability=obs) as b1:
        state.b1 = b1
        yield  # Aquí es donde la app atiende peticiones
    # --- Shutdown ---
    # El bloque 'async with' ejecutará automáticamente el logout al salir.
    print("Conexión con SAP B1 cerrada correctamente.")

app = FastAPI(lifespan=lifespan)

# 4. Dependencia para inyectar el cliente en los Endpoints
async def get_b1() -> AsyncB1Client:
    if not state.b1:
        raise HTTPException(status_code=503, detail="SAP B1 Client not initialized")
    return state.b1

# 5. Endpoint de ejemplo
@app.get("/items/{item_code}")
async def get_item(item_code: str, b1: AsyncB1Client = Depends(get_b1)):
    """
    Ejemplo de consulta asíncrona. 
    Múltiples peticiones pueden entrar aquí y no se bloquearán entre sí.
    """
    try:
        item = await b1.items.get(item_code)
        return item
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Item {item_code} not found: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
