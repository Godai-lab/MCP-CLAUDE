import os
from dotenv import load_dotenv
from app import call_claude

load_dotenv()

def test_claude_direct():
    """Prueba directa de la función call_claude"""
    print("🧪 Probando llamada directa a Claude...")
    
    try:
        result = call_claude(
            model="claude-3-5-sonnet-20241022",
            prompt="Responde solo 'OK' para confirmar que funciona",
            max_tokens=10
        )
        print(f"✅ Claude responde: {result}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_claude_direct():
        print("\n🎉 ¡El servidor MCP funciona correctamente!")
        print("📡 Claude puede responder a través del servidor MCP")
    else:
        print("\n❌ Hay un problema con la configuración")