import asyncio

from b1sl.b1sl import HookContext, ObservabilityConfig


# 1. Definir un Hook de ejemplo (Pilar de Telemetría)
async def my_metrics_hook(ctx: HookContext):
    """
    Simula el envío de métricas a un sistema externo (Datadog, Sentry, etc.).
    Recibe un HookContext inmutable con todos los detalles de la petición.
    En este caso es una función asíncrona para mayor flexibilidad.
    """
    # Usamos prints manuales dentro del hook para ver qué está pasando
    print(f"\n   [HOOK TRIGGERED] event=on_response | req_id={ctx.req_id}")
    print(f"   → Latencia: {ctx.duration_ms:.2f}ms")
    print(f"   → Endpoint: {ctx.http_method} {ctx.endpoint}")
    print(f"   → Extra de Contexto: {ctx.extra.get('workflow_id')}")

async def run_example():
    # 2. Configurar el objeto de Observabilidad
    obs_config = ObservabilityConfig(
        hooks={"on_response": [my_metrics_hook]},
        context_extras={
            "workflow_id": "WF-ASYNC-777",
            "environment": "demo-async"
        },
        slow_request_threshold_ms=10.0 # Umbral bajo para forzar logs de 'Slow'
    )

    # 3. Inicializar el cliente
    # Importar dentro de la función para mayor claridad en el ejemplo
    import sys
    from pathlib import Path
    # Add project roots to sys.path for standalone script execution
    sys.path.append(str(Path(__file__).parent.parent / "src"))
    sys.path.append(str(Path(__file__).parent))

    import httpx
    import respx
    from utils import AsyncExampleRunner

    from b1sl.b1sl import AsyncB1Client, B1Environment

    env = B1Environment.load()
    client = AsyncB1Client(config=env.config, version="v2", observability=obs_config)
    runner = AsyncExampleRunner("Advanced Async Observability Demo", observability=obs_config)
    runner.client = client

    # --- CONFIGURAR MOCK USANDO RESPX ---
    # Respx intercepta todas las peticiones a httpx sin importar cuándo se crea el cliente
    respx_mock = respx.mock(base_url=client._adapter.raw_base_url, assert_all_called=False)
    respx_mock.start()

    # Mock para Login
    respx_mock.post("/Login").mock(return_value=httpx.Response(
        200,
        json={"SessionId": "MOCK-SESSION-ID", "SessionTimeout": 30}
    ))

    # Mock para Items
    async def items_side_effect(request):
        await asyncio.sleep(0.05) # Simular latencia de 50ms
        return httpx.Response(200, json={"value": []})

    respx_mock.get("/Items").mock(side_effect=items_side_effect)

    # Mock para Logout
    respx_mock.post("/Logout").mock(return_value=httpx.Response(200))

    async with runner.client as b1:
        runner.header("SAP B1 Observability (Async Enterprise Pattern)")
        runner.info("Ejecutando petición asíncrona a 'Items' (MOCK)...")

        # Al ejecutar esto, se disparará automáticamente el hook 'on_response'
        try:
            # En el cliente asíncrono, los servicios también son asíncronos
            items = await b1.items.list()
            runner.success("Petición asíncrona completada con éxito.")
            runner.result("Registros recuperados", len(items))
        except Exception as e:
            runner.error("Error durante la petición asíncrona", e)

        runner.info("Demo de Observabilidad Asíncrona finalizada.")
        respx_mock.stop()
        print("\nNota: Revisa la consola para ver los logs estructurados inyectados por el SDK.")

if __name__ == "__main__":
    try:
        asyncio.run(run_example())
    except KeyboardInterrupt:
        pass
