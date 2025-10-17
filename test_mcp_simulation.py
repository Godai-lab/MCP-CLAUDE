import requests
import json
import time

# URL del servidor local
BASE_URL = "http://localhost:8080"

def test_server_status():
    """Prueba que el servidor esté funcionando"""
    print("🔍 Probando estado del servidor híbrido...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Servidor online: {data['name']} v{data['version']}")
            print(f"📝 Descripción: {data['description']}")
            print(f"🔗 Protocolo: {data['protocol']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No se puede conectar: {e}")
        return False

def test_list_tools():
    """Prueba que las herramientas estén disponibles"""
    print("\n🔍 Probando listado de herramientas...")
    try:
        response = requests.get(f"{BASE_URL}/mcp/v1/tools")
        if response.status_code == 200:
            tools = response.json()['tools']
            print(f"✅ Herramientas encontradas: {len(tools)}")
            for tool in tools:
                print(f"   🔧 {tool['name']}: {tool['description']}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_call_claude():
    """Prueba llamar a Claude a través del servidor híbrido"""
    print("\n🔍 Probando llamada a Claude...")
    
    payload = {
        "name": "call_claude",
        "arguments": {
            "model": "claude-3-5-sonnet-20241022",
            "prompt": "Responde solo 'OK' para confirmar que funciona",
            "max_tokens": 10
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/v1/call_tool",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            claude_response = result['content'][0]['text']
            print(f"✅ Claude responde: {claude_response}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_different_questions():
    """Prueba diferentes preguntas a Claude"""
    print("\n🎭 Probando diferentes preguntas...")
    
    questions = [
        "¿Cuál es la capital de Francia?",
        "Explica qué es la inteligencia artificial en una frase",
        "¿Cuáles son los beneficios de Python?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Pregunta {i}: {question}")
        
        payload = {
            "name": "call_claude",
            "arguments": {
                "model": "claude-3-5-sonnet-20241022",
                "prompt": question,
                "max_tokens": 100
            }
        }
        
        try:
            response = requests.post(f"{BASE_URL}/mcp/v1/call_tool", json=payload)
            if response.status_code == 200:
                result = response.json()
                claude_response = result['content'][0]['text']
                print(f"   🤖 Claude: {claude_response}")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DEL SERVIDOR HÍBRIDO")
    print("   (Servidor HTTP + MCP compatible con OpenAI)")
    print("\n" + "="*60)
    
    # Verificar que el servidor esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/", timeout=3)
        if response.status_code != 200:
            print("❌ El servidor no está corriendo o no responde correctamente")
            print("   Ejecuta: python app.py")
            return
    except:
        print("❌ No se puede conectar al servidor")
        print("   Asegúrate de que esté corriendo: python app.py")
        return
    
    # Ejecutar todas las pruebas
    tests_passed = 0
    total_tests = 3
    
    if test_server_status():
        tests_passed += 1
    
    if test_list_tools():
        tests_passed += 1
    
    if test_call_claude():
        tests_passed += 1
    
    test_different_questions()
    
    print("\n" + "="*60)
    print(f"📊 Resultados: {tests_passed}/{total_tests} pruebas pasaron")
    
    if tests_passed == total_tests:
        print("🎉 ¡El servidor híbrido funciona perfectamente!")
        print("📡 Listo para conectar con OpenAI")
        print("\n🚀 Próximos pasos:")
        print("   1. Sube los cambios a GitHub")
        print("   2. Railway se redesplegará automáticamente")
        print("   3. Conecta con OpenAI usando la URL de Railway")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()