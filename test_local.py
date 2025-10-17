"""
Script de prueba local para el servidor MCP
Ejecuta esto para probar que el servidor funciona correctamente
"""

import requests
import json

# URL del servidor (cambiar si usas Railway)
BASE_URL = "http://localhost:8080"

def test_server_status():
    """Prueba que el servidor esté funcionando"""
    print("🔍 Probando estado del servidor...")
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Status: {response.status_code}")
    print(f"📝 Respuesta: {json.dumps(response.json(), indent=2)}\n")

def test_list_tools():
    """Prueba que las herramientas estén disponibles"""
    print("🔍 Listando herramientas disponibles...")
    response = requests.get(f"{BASE_URL}/mcp/v1/tools")
    print(f"✅ Status: {response.status_code}")
    print(f"📝 Herramientas: {json.dumps(response.json(), indent=2)}\n")

def test_call_claude():
    """Prueba llamar a Claude"""
    print("🔍 Probando llamada a Claude...")
    payload = {
        "name": "call_claude",
        "arguments": {
            "model": "claude-3-5-sonnet-20241022",
            "prompt": "¿Cuál es la capital de Francia? Responde en una frase corta.",
            "max_tokens": 100
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/mcp/v1/call_tool",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"📝 Respuesta de Claude:")
        print(f"   {result['content'][0]['text']}\n")
    else:
        print(f"❌ Error: {response.text}\n")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del servidor MCP\n")
    print("=" * 60)
    
    try:
        test_server_status()
        test_list_tools()
        test_call_claude()
        
        print("=" * 60)
        print("✅ ¡Todas las pruebas completadas!")
        print("\n💡 Tu servidor está listo para conectarse con OpenAI")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   ¿Está el servidor corriendo? Ejecuta: python app.py")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

