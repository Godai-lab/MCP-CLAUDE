import requests
import json
import os
from typing import List, Dict
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Get port from environment variable (Railway sets this, defaults to 8080 for local dev)
PORT = int(os.environ.get("PORT", 8080))

# Initialize FastMCP server with host and port in constructor
mcp = FastMCP("claude", host="0.0.0.0", port=PORT)

# Get API key from environment
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

def call_claude_api(model: str, prompt: str, max_tokens: int = 1024) -> str:
    """Llama a la API de Claude con el modelo especificado"""
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": anthropic_api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
            },
        )

        if response.status_code != 200:
            error_data = response.json()
            raise Exception(f"Anthropic API error: {json.dumps(error_data)}")

        data = response.json()
        return data["content"][0]["text"]

    except Exception as e:
        raise Exception(f"Failed to call Claude: {str(e)}")

@mcp.tool()
def call_claude(model: str, prompt: str, max_tokens: int = 1024) -> str:
    """
    Llama a Claude con el modelo especificado y retorna la respuesta.

    Args:
        model: El modelo de Claude a utilizar (ej: claude-3-5-sonnet-20241022)
        prompt: El prompt a enviar al modelo
        max_tokens: Máximo número de tokens en la respuesta (opcional, default: 1024)

    Returns:
        Respuesta de Claude como string
    """
    try:
        if not anthropic_api_key:
            return "Error: ANTHROPIC_API_KEY no está configurada"
        
        result = call_claude_api(model, prompt, max_tokens)
        return result
        
    except Exception as e:
        return f"Error llamando a Claude: {str(e)}"

@mcp.tool()
def get_claude_models() -> str:
    """
    Obtiene la lista de modelos de Claude disponibles.

    Returns:
        JSON string con los modelos disponibles
    """
    models = [
        {
            "name": "claude-3-5-sonnet-20241022",
            "description": "Claude 3.5 Sonnet - Modelo más reciente y potente",
            "max_tokens": 8192,
            "recommended": True
        },
        {
            "name": "claude-3-5-haiku-20241022", 
            "description": "Claude 3.5 Haiku - Modelo rápido y eficiente",
            "max_tokens": 8192,
            "recommended": False
        },
        {
            "name": "claude-3-opus-20240229",
            "description": "Claude 3 Opus - Modelo anterior pero potente",
            "max_tokens": 4096,
            "recommended": False
        }
    ]
    
    return json.dumps(models, indent=2)

@mcp.resource("claude://models")
def get_available_models() -> str:
    """
    Recurso que lista todos los modelos de Claude disponibles.
    """
    try:
        content = "# Modelos de Claude Disponibles\n\n"
        content += "## Modelos Recomendados\n\n"
        content += "- **claude-3-5-sonnet-20241022**: Modelo más reciente y potente (recomendado)\n"
        content += "- **claude-3-5-haiku-20241022**: Modelo rápido y eficiente\n\n"
        content += "## Modelos Anteriores\n\n"
        content += "- **claude-3-opus-20240229**: Modelo anterior pero potente\n\n"
        content += "## Uso\n\n"
        content += "Usa `call_claude(model='nombre_del_modelo', prompt='tu_pregunta')` para llamar a cualquier modelo.\n"
        
        return content
        
    except Exception as e:
        return f"# Error\n\nError obteniendo modelos: {str(e)}"

@mcp.resource("claude://status")
def get_server_status() -> str:
    """
    Recurso que muestra el estado del servidor Claude MCP.
    """
    try:
        content = "# Estado del Servidor Claude MCP\n\n"
        content += f"**Servidor**: Claude MCP Server\n"
        content += f"**Puerto**: {PORT}\n"
        content += f"**API Key**: {'✅ Configurada' if anthropic_api_key else '❌ No configurada'}\n\n"
        content += "## Herramientas Disponibles\n\n"
        content += "- `call_claude`: Llama a cualquier modelo de Claude\n"
        content += "- `get_claude_models`: Obtiene lista de modelos disponibles\n\n"
        content += "## Recursos Disponibles\n\n"
        content += "- `claude://models`: Lista de modelos\n"
        content += "- `claude://status`: Estado del servidor\n\n"
        
        return content
        
    except Exception as e:
        return f"# Error\n\nError obteniendo estado: {str(e)}"

@mcp.prompt()
def generate_claude_prompt(question: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    """
    Genera un prompt optimizado para obtener la mejor respuesta de Claude.
    
    Args:
        question: La pregunta o tarea a realizar
        model: El modelo de Claude a usar (opcional)
    """
    return f"""Usa Claude para responder la siguiente pregunta de manera completa y útil:

**Pregunta**: {question}

**Instrucciones**:
1. Usa el modelo {model} para obtener la mejor respuesta
2. Proporciona una respuesta detallada y bien estructurada
3. Si es apropiado, incluye ejemplos o explicaciones paso a paso
4. Asegúrate de que la respuesta sea precisa y útil

**Comando sugerido**:
```
call_claude(model='{model}', prompt='{question}', max_tokens=1024)
```

Responde de manera clara y profesional."""

if __name__ == "__main__":
    # Initialize and run the server
    print(f"🚀 Iniciando Claude MCP Server en 0.0.0.0:{PORT}")
    print("📡 Usando FastMCP con transporte SSE")
    print("🔗 Compatible con OpenAI y Claude")
    
    if not anthropic_api_key:
        print("⚠️  ADVERTENCIA: ANTHROPIC_API_KEY no está configurada")
        print("   Configura la variable de entorno para que funcione correctamente")
    
    # Run with SSE transport (host and port already set in constructor)
    mcp.run(transport='sse')