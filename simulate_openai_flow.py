"""
Simulador del flujo completo de OpenAI
Este script simula paso a paso cómo OpenAI se conecta y usa tu servidor MCP
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def simulate_openai_agent():
    """Simula un agente de OpenAI usando tu servidor MCP"""
    
    print("🤖 SIMULANDO AGENTE DE OPENAI")
    print("="*60)
    
    # Simular que un usuario le dice algo al agente de OpenAI
    user_message = "Necesito que uses Claude para explicarme qué es la inteligencia artificial"
    
    print(f"👤 Usuario dice: '{user_message}'")
    print("\n🧠 OpenAI procesando...")
    print("   - Detecta que necesita usar Claude")
    print("   - Busca servidor MCP configurado")
    print("   - Se conecta a tu servidor...")
    
    # Paso 1: OpenAI verifica que el servidor esté disponible
    print("\n1️⃣ Verificando servidor MCP...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            server_info = response.json()
            print(f"   ✅ Conectado a: {server_info['name']}")
        else:
            print(f"   ❌ Error del servidor: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ No se puede conectar: {e}")
        return
    
    # Paso 2: OpenAI obtiene las herramientas disponibles
    print("\n2️⃣ Obteniendo herramientas disponibles...")
    try:
        response = requests.get(f"{BASE_URL}/mcp/v1/tools")
        if response.status_code == 200:
            tools = response.json()['tools']
            print(f"   ✅ Herramientas encontradas: {len(tools)}")
            for tool in tools:
                print(f"      🔧 {tool['name']}")
        else:
            print(f"   ❌ Error obteniendo herramientas: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Paso 3: OpenAI decide usar la herramienta call_claude
    print("\n3️⃣ OpenAI decide usar la herramienta 'call_claude'")
    print("   - Analiza el prompt del usuario")
    print("   - Prepara la llamada a Claude")
    
    # Paso 4: OpenAI llama a la herramienta
    print("\n4️⃣ Ejecutando llamada a Claude...")
    
    # Simular que OpenAI prepara el prompt para Claude
    claude_prompt = "Explica qué es la inteligencia artificial de manera clara y concisa"
    
    payload = {
        "name": "call_claude",
        "arguments": {
            "model": "claude-3-5-sonnet-20241022",
            "prompt": claude_prompt,
            "max_tokens": 300
        }
    }
    
    print(f"   📤 Enviando a Claude: '{claude_prompt}'")
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
            
            print(f"   ✅ Respuesta de Claude recibida en {response_time}s")
            print(f"   📥 Claude responde:")
            print(f"      {claude_response}")
            
            # Paso 5: OpenAI procesa la respuesta y la presenta al usuario
            print(f"\n5️⃣ OpenAI procesa la respuesta y responde al usuario:")
            print(f"   🤖 OpenAI dice: 'Basándome en la información de Claude, {claude_response[:100]}...'")
            
        else:
            print(f"   ❌ Error en la llamada: {response.status_code}")
            print(f"   📝 Detalles: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def simulate_different_scenarios():
    """Simula diferentes escenarios de uso"""
    
    scenarios = [
        {
            "user": "¿Cuál es la capital de Francia?",
            "claude_prompt": "¿Cuál es la capital de Francia? Responde de forma breve.",
            "max_tokens": 50
        },
        {
            "user": "Necesito ayuda con programación en Python",
            "claude_prompt": "Dame consejos básicos para programar en Python para un principiante",
            "max_tokens": 200
        },
        {
            "user": "Explica la teoría de la relatividad",
            "claude_prompt": "Explica la teoría de la relatividad de Einstein de manera simple y comprensible",
            "max_tokens": 300
        }
    ]
    
    print("\n🎭 SIMULANDO DIFERENTES ESCENARIOS")
    print("="*60)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📝 Escenario {i}:")
        print(f"   👤 Usuario: '{scenario['user']}'")
        
        payload = {
            "name": "call_claude",
            "arguments": {
                "model": "claude-3-5-sonnet-20241022",
                "prompt": scenario['claude_prompt'],
                "max_tokens": scenario['max_tokens']
            }
        }
        
        try:
            response = requests.post(f"{BASE_URL}/mcp/v1/call_tool", json=payload)
            if response.status_code == 200:
                result = response.json()
                claude_response = result['content'][0]['text']
                print(f"   🤖 Claude: {claude_response[:100]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("   " + "-"*40)

def main():
    """Función principal"""
    print("🚀 SIMULADOR COMPLETO DE OPENAI + MCP")
    print("   Este script simula exactamente cómo OpenAI usará tu servidor")
    print("\n⚠️  IMPORTANTE: Asegúrate de que tu servidor esté corriendo:")
    print("   python app.py")
    print("\n" + "="*60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=3)
        if response.status_code != 200:
            print("❌ El servidor no está corriendo")
            return
    except:
        print("❌ No se puede conectar al servidor")
        print("   Ejecuta primero: python app.py")
        return
    
    # Ejecutar simulaciones
    simulate_openai_agent()
    simulate_different_scenarios()
    
    print("\n" + "="*60)
    print("✅ SIMULACIÓN COMPLETADA")
    print("\n🎯 Lo que acabas de ver es exactamente lo que pasará cuando:")
    print("   1. Un usuario le diga algo a OpenAI")
    print("   2. OpenAI detecte que necesita usar Claude")
    print("   3. OpenAI se conecte a tu servidor en Railway")
    print("   4. Tu servidor llame a Claude")
    print("   5. La respuesta regrese al usuario")
    
    print("\n🚀 ¡Tu servidor está listo para desplegar en Railway!")

if __name__ == "__main__":
    main()
