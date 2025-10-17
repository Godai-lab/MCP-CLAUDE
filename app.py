import json
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Configuración
app = Flask(__name__)
CORS(app)
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

def call_claude(model: str, prompt: str, max_tokens: int = 1024) -> str:
    """Llama a Claude con el modelo especificado"""
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

# Endpoints HTTP para OpenAI
@app.route("/", methods=["GET"])
def home():
    """Endpoint de bienvenida con información de herramientas"""
    return jsonify({
        "name": "Claude MCP Server",
        "version": "1.0.0",
        "description": "Servidor MCP híbrido para conectar OpenAI con Claude",
        "status": "online",
        "protocol": "HTTP + MCP compatible",
        "tools": [
            {
                "name": "call_claude",
                "description": "Llama a Claude con el modelo especificado y retorna la respuesta",
                "endpoint": "/call_claude",
                "method": "POST",
                "parameters": {
                    "model": "string (ej: claude-3-5-sonnet-20241022)",
                    "prompt": "string (pregunta para Claude)",
                    "max_tokens": "number (opcional, default: 1024)"
                },
                "example": {
                    "url": "POST https://mcp-claude-production.up.railway.app/call_claude",
                    "body": {
                        "model": "claude-3-5-sonnet-20241022",
                        "prompt": "¿Cuál es la capital de Francia?",
                        "max_tokens": 100
                    }
                }
            }
        ],
        "endpoints": {
            "discover_tools": "GET /mcp/v1/tools",
            "call_claude": "POST /call_claude",
            "resources": "GET /mcp/v1/resources",
            "prompts": "GET /mcp/v1/prompts"
        },
        "usage": {
            "step1": "GET /mcp/v1/tools - Descubrir herramientas disponibles",
            "step2": "POST /call_claude - Ejecutar herramienta call_claude",
            "step3": "Formato: {model, prompt, max_tokens?}",
            "note": "Para nuevas herramientas: POST /{nombre_herramienta}"
        },
        "important": {
            "primary_endpoint": "POST /call_claude",
            "format": "Direct JSON with {model, prompt, max_tokens?}",
            "no_wrapper": "No need for 'name' or 'arguments' wrapper"
        }
    })

@app.route("/mcp/v1/tools", methods=["GET"])
def list_tools():
    """Lista las herramientas disponibles - Formato OpenAI compatible"""
    tools = [
        {
            "name": "call_claude",
            "description": "Llama a Claude con el modelo especificado y retorna la respuesta",
            "endpoint": "/call_claude",
            "method": "POST",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "El modelo de Claude a utilizar (ej: claude-3-5-sonnet-20241022)",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "El prompt a enviar al modelo",
                    },
                    "max_tokens": {
                        "type": "number",
                        "description": "Máximo número de tokens en la respuesta (opcional, default: 1024)",
                        "default": 1024
                    },
                },
                "required": ["model", "prompt"],
            },
            "usage": {
                "url": "POST /call_claude",
                "format": "Direct JSON: {model, prompt, max_tokens?}",
                "note": "No wrapper needed - send parameters directly"
            }
        }
    ]
    
    # Headers para compatibilidad con OpenAI
    response = jsonify({"tools": tools})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route("/call_claude", methods=["POST"])
def call_claude_endpoint():
    """Endpoint específico para call_claude - Formato simplificado"""
    try:
        data = request.json
        
        # Validar parámetros requeridos
        if "model" not in data:
            return jsonify({"error": "Parámetro 'model' es requerido"}), 400
        if "prompt" not in data:
            return jsonify({"error": "Parámetro 'prompt' es requerido"}), 400
        
        result = call_claude(
            model=data["model"],
            prompt=data["prompt"],
            max_tokens=data.get("max_tokens", 1024),
        )
        
        return jsonify({
            "content": [
                {
                    "type": "text",
                    "text": result
                }
            ]
        })
            
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/mcp/v1/resources", methods=["GET"])
def list_resources():
    """Lista los recursos disponibles"""
    return jsonify({
        "resources": []
    })

@app.route("/mcp/v1/prompts", methods=["GET"])
def list_prompts():
    """Lista los prompts disponibles"""
    return jsonify({
        "prompts": []
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print("🚀 Claude MCP Server Híbrido iniciado")
    print("📡 Endpoints HTTP disponibles para OpenAI:")
    print(f"  - GET  /")
    print(f"  - GET  /mcp/v1/tools")
    print(f"  - POST /mcp/v1/call_tool")
    print(f"  - GET  /mcp/v1/resources")
    print(f"  - GET  /mcp/v1/prompts")
    print("🔗 Compatible con OpenAI y clientes MCP")
    app.run(host="0.0.0.0", port=port, debug=False)