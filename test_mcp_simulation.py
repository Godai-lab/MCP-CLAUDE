import requests
import json
import time

# URL del servidor local
BASE_URL = "http://localhost:8080"

def test_server_status():
    """Prueba que el servidor esté funcionando"""
    print("🔍 Probando estado del servidor FastMCP...")
    try:
        # FastMCP no expone endpoints HTTP directos, solo SSE
        # Vamos a probar la conectividad básica
        response = requests.get(f"{BASE_URL}/", timeout=3)
        # FastMCP devuelve 404 para endpoints HTTP (esto es normal)
        if response.status_code == 404:
            print("✅ Servidor FastMCP funcionando (404 es normal para FastMCP)")
            return True
        else:
            print(f"✅ Servidor respondiendo con código: {response.status_code}")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("   Asegúrate de que esté corriendo: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_fastmcp_info():
    """Muestra información sobre el servidor FastMCP"""
    print("\n📡 Información del servidor FastMCP:")
    print("   - Framework: FastMCP (SDK oficial)")
    print("   - Transporte: SSE (Server-Sent Events)")
    print("   - Protocolo: MCP nativo")
    print("   - Compatible con: OpenAI, Claude, Cursor")
    print("   - Herramientas: call_claude, get_claude_models")
    print("   - Recursos: claude://models, claude://status")
    print("\n💡 IMPORTANTE:")
    print("   - FastMCP NO expone endpoints HTTP REST")
    print("   - Usa transporte SSE para comunicación MCP")
    print("   - Los errores 404 son NORMALES para FastMCP")
    print("   - OpenAI se conecta usando el protocolo MCP nativo")

def test_claude_function():
    """Prueba la función call_claude directamente"""
    print("\n🧪 Probando función call_claude directamente...")
    
    # Importar la función directamente del módulo
    try:
        from app import call_claude_api
        
        result = call_claude_api(
            model="claude-3-5-sonnet-20241022",
            prompt="Responde solo 'OK' para confirmar que funciona",
            max_tokens=10
        )
        print(f"✅ Claude responde: {result}")
        return True
    except Exception as e:
        print(f"❌ Error en llamada directa: {e}")
        return False

def test_different_questions():
    """Prueba diferentes preguntas a Claude"""
    print("\n🎭 Probando diferentes preguntas...")
    
    questions = [
        "¿Cuál es la capital de Francia?",
        "Explica qué es la inteligencia artificial en una frase",
        "¿Cuáles son los beneficios de Python?"
    ]
    
    try:
        from app import call_claude_api
        
        for i, question in enumerate(questions, 1):
            print(f"\n📝 Pregunta {i}: {question}")
            
            result = call_claude_api(
                model="claude-3-5-sonnet-20241022",
                prompt=question,
                max_tokens=100
            )
            print(f"   🤖 Claude: {result[:100]}...")
            
    except Exception as e:
        print(f"❌ Error en preguntas: {e}")

def test_models_list():
    """Prueba la función get_claude_models"""
    print("\n🔧 Probando lista de modelos...")
    
    try:
        from app import get_claude_models
        
        models_json = get_claude_models()
        models = json.loads(models_json)
        
        print(f"✅ Modelos encontrados: {len(models)}")
        for model in models:
            recommended = "⭐" if model.get("recommended") else "  "
            print(f"   {recommended} {model['name']}: {model['description']}")
        
        return True
    except Exception as e:
        print(f"❌ Error obteniendo modelos: {e}")
        return False

def test_resources():
    """Prueba los recursos del servidor"""
    print("\n📚 Probando recursos del servidor...")
    
    try:
        from app import get_available_models, get_server_status
        
        print("🔍 Probando recurso claude://models:")
        models_content = get_available_models()
        print(f"   ✅ Contenido: {len(models_content)} caracteres")
        
        print("🔍 Probando recurso claude://status:")
        status_content = get_server_status()
        print(f"   ✅ Contenido: {len(status_content)} caracteres")
        
        return True
    except Exception as e:
        print(f"❌ Error en recursos: {e}")
        return False

def test_prompts():
    """Prueba los prompts del servidor"""
    print("\n💬 Probando prompts del servidor...")
    
    try:
        from app import generate_claude_prompt
        
        prompt = generate_claude_prompt(
            question="¿Qué es la inteligencia artificial?",
            model="claude-3-5-sonnet-20241022"
        )
        
        print(f"✅ Prompt generado: {len(prompt)} caracteres")
        print(f"   📝 Contenido: {prompt[:200]}...")
        
        return True
    except Exception as e:
        print(f"❌ Error en prompts: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DEL SERVIDOR FASTMCP")
    print("   (Servidor MCP nativo con transporte SSE)")
    print("\n" + "="*60)
    
    # Verificar que el servidor esté corriendo
    if not test_server_status():
        print("\n❌ El servidor no está corriendo")
        print("   Ejecuta: python app.py")
        return
    
    # Mostrar información del servidor
    test_fastmcp_info()
    
    # Ejecutar todas las pruebas
    tests_passed = 0
    total_tests = 5
    
    print("\n" + "="*60)
    print("🧪 EJECUTANDO PRUEBAS...")
    print("="*60)
    
    if test_claude_function():
        tests_passed += 1
    
    if test_models_list():
        tests_passed += 1
    
    if test_resources():
        tests_passed += 1
    
    if test_prompts():
        tests_passed += 1
    
    test_different_questions()
    
    print("\n" + "="*60)
    print(f"📊 Resultados: {tests_passed}/{total_tests} pruebas pasaron")
    
    if tests_passed == total_tests:
        print("🎉 ¡El servidor FastMCP funciona perfectamente!")
        print("📡 Listo para conectar con OpenAI y Claude")
        print("\n🚀 Próximos pasos:")
        print("   1. Sube los cambios a GitHub")
        print("   2. Railway se redesplegará automáticamente")
        print("   3. Conecta con OpenAI usando la URL de Railway")
        print("\n💡 Nota: FastMCP usa transporte SSE, no HTTP REST")
        print("   Es compatible con clientes MCP nativos como OpenAI")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\n🔧 Posibles soluciones:")
        print("   - Verifica que ANTHROPIC_API_KEY esté configurada")
        print("   - Asegúrate de que el servidor esté corriendo")
        print("   - Revisa la conexión a internet")

if __name__ == "__main__":
    main()