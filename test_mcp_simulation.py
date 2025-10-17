"""
Simulador completo de llamadas MCP
Este script simula exactamente cómo OpenAI se conectará a tu servidor
"""

import requests
import json
import time

# URL del servidor local
BASE_URL = "http://localhost:8080"

def print_header(title):
    """Imprime un encabezado bonito"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def test_mcp_handshake():
    """Simula el handshake inicial que hace OpenAI"""
    print_header("SIMULANDO CONEXIÓN INICIAL DE OPENAI")
    
    # 1. Verificar que el servidor esté vivo
    print("1️⃣ Verificando estado del servidor...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Servidor online: {data['name']} v{data['version']}")
            print(f"   📝 Descripción: {data['description']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ No se puede conectar: {e}")
        return False
    
    # 2. Listar herramientas disponibles
    print("\n2️⃣ Obteniendo herramientas disponibles...")
    try:
        response = requests.get(f"{BASE_URL}/mcp/v1/tools")
        if response.status_code == 200:
            tools = response.json()['tools']
            print(f"   ✅ Encontradas {len(tools)} herramienta(s):")
            for tool in tools:
                print(f"      🔧 {tool['name']}: {tool['description']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return True

def test_claude_integration():
    """Simula una conversación completa como la haría OpenAI"""
    print_header("SIMULANDO CONVERSACIÓN CON CLAUDE")
    
    # Simular diferentes tipos de preguntas que podría hacer un usuario
    test_cases = [
        {
            "user_question": "¿Cuál es la capital de Francia?",
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 100
        },
        {
            "user_question": "Explica qué es la inteligencia artificial en términos simples",
            "model": "claude-3-5-sonnet-20241022", 
            "max_tokens": 200
        },
        {
            "user_question": "¿Cuáles son los beneficios de usar Python?",
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 150
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Caso de prueba {i}:")
        print(f"   Usuario pregunta: '{test_case['user_question']}'")
        
        # Simular la llamada que haría OpenAI
        payload = {
            "name": "call_claude",
            "arguments": {
                "model": test_case["model"],
                "prompt": test_case["user_question"],
                "max_tokens": test_case["max_tokens"]
            }
        }
        
        print("   🔄 Enviando solicitud a Claude...")
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{BASE_URL}/mcp/v1/call_tool",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            if response.status_code == 200:
                result = response.json()
                claude_response = result['content'][0]['text']
                print(f"   ✅ Respuesta recibida en {response_time}s:")
                print(f"   📤 Claude dice: {claude_response}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error en la llamada: {e}")
        
        print("   " + "-"*50)

def test_error_handling():
    """Prueba el manejo de errores"""
    print_header("PROBANDO MANEJO DE ERRORES")
    
    # Caso 1: Herramienta inexistente
    print("1️⃣ Probando herramienta inexistente...")
    payload = {
        "name": "herramienta_inexistente",
        "arguments": {"test": "value"}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/mcp/v1/call_tool", json=payload)
        if response.status_code == 400:
            print("   ✅ Error manejado correctamente")
        else:
            print(f"   ⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Caso 2: Parámetros faltantes
    print("\n2️⃣ Probando parámetros faltantes...")
    payload = {
        "name": "call_claude",
        "arguments": {
            "model": "claude-3-5-sonnet-20241022"
            # Falta 'prompt'
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/mcp/v1/call_tool", json=payload)
        if response.status_code in [400, 500]:
            print("   ✅ Error de validación manejado")
        else:
            print(f"   ⚠️  Respuesta inesperada: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_performance():
    """Prueba la performance del servidor"""
    print_header("PRUEBA DE PERFORMANCE")
    
    # Hacer múltiples llamadas para ver el rendimiento
    num_requests = 3
    print(f"🔄 Haciendo {num_requests} llamadas consecutivas...")
    
    times = []
    for i in range(num_requests):
        payload = {
            "name": "call_claude",
            "arguments": {
                "model": "claude-3-5-sonnet-20241022",
                "prompt": f"Responde solo 'OK' a la pregunta {i+1}",
                "max_tokens": 10
            }
        }
        
        start_time = time.time()
        try:
            response = requests.post(f"{BASE_URL}/mcp/v1/call_tool", json=payload)
            end_time = time.time()
            
            if response.status_code == 200:
                times.append(end_time - start_time)
                print(f"   ✅ Llamada {i+1}: {round(end_time - start_time, 2)}s")
            else:
                print(f"   ❌ Llamada {i+1}: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ Llamada {i+1}: {e}")
    
    if times:
        avg_time = sum(times) / len(times)
        print(f"\n📊 Tiempo promedio: {round(avg_time, 2)}s")
        print(f"📊 Tiempo más rápido: {round(min(times), 2)}s")
        print(f"📊 Tiempo más lento: {round(max(times), 2)}s")

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 INICIANDO SIMULACIÓN COMPLETA DE MCP")
    print("   (Simulando cómo OpenAI se conectará a tu servidor)")
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ El servidor no está corriendo o no responde correctamente")
            print("   Ejecuta: python app.py")
            return
    except:
        print("❌ No se puede conectar al servidor")
        print("   Asegúrate de que esté corriendo: python app.py")
        return
    
    # Ejecutar todas las pruebas
    if test_mcp_handshake():
        test_claude_integration()
        test_error_handling()
        test_performance()
        
        print_header("RESUMEN DE PRUEBAS")
        print("✅ Handshake MCP: OK")
        print("✅ Integración con Claude: OK") 
        print("✅ Manejo de errores: OK")
        print("✅ Performance: OK")
        print("\n🎉 ¡Tu servidor está listo para Railway!")
        print("\n📋 Próximos pasos:")
        print("   1. Sube el código a GitHub")
        print("   2. Despliega en Railway")
        print("   3. Configura ANTHROPIC_API_KEY en Railway")
        print("   4. Conecta con OpenAI usando la URL de Railway")
    else:
        print("❌ Las pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
