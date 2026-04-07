import asyncio
import sys
from pathlib import Path
# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from b1sl.b1sl import AsyncB1Client, B1Environment
from b1sl.b1sl.logging_utils import setup_logging

async def main():
    # 0. Inicializar logs estructurados
    setup_logging()
    
    # 1. Carga de configuración desde .env
    env = B1Environment.load()
    config = env.config
    
    print(f"✅ Conectando a {config.base_url} (DB: {config.company_db})...")
    
    # 2. Uso de AsyncB1Client como context manager asíncrono
    async with AsyncB1Client(config) as b1:
        
        # 3. Llamadas concurrentes de ejemplo (Peticiones asíncronas)
        item_codes = ["A0001", "A0002", "A0003"]
        
        # Lanzamos todas las peticiones al mismo tiempo
        print(f"🚀 Enviando {len(item_codes)} peticiones concurrentes a SAP...")
        tasks = [b1.items.get(code) for code in item_codes]
        
        # Esperamos a que todas terminen
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 4. Mostrar resultados
        for idx, res in enumerate(results):
            if isinstance(res, Exception):
                print(f"  ❌ Error en petición {idx+1}: {res}")
            else:
                print(f"  ✨ Item {idx+1} recuperado: {res.item_name} ({res.item_code})")

if __name__ == "__main__":
    # Ejecutamos el bucle de eventos
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
