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
    """Endpoint de bienvenida"""
    return jsonify({
        "name": "Claude MCP Server",
        "version": "1.0.0",
        "description": "Servidor MCP híbrido para conectar OpenAI con Claude",
        "status": "online",
        "protocol": "HTTP + MCP compatible"
    })

@app.route("/mcp/v1/tools", methods=["GET"])
def list_tools():
    """Lista las herramientas disponibles - Formato OpenAI compatible"""
    tools = [
        {
            "name": "call_claude",
            "description": "Llama a Claude con el modelo especificado y retorna la respuesta",
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
        }
    ]
    
    # Headers para compatibilidad con OpenAI
    response = jsonify({"tools": tools})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route("/mcp/v1/call_tool", methods=["POST"])
def call_tool():
    """Ejecuta una herramienta - Formato OpenAI compatible"""
    try:
        data = request.json
        tool_name = data.get("name")
        tool_input = data.get("arguments", {})
        
        if tool_name == "call_claude":
            result = call_claude(
                model=tool_input["model"],
                prompt=tool_input["prompt"],
                max_tokens=tool_input.get("max_tokens", 1024),
            )
            
            return jsonify({
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            })
        else:
            return jsonify({
                "error": f"Herramienta desconocida: {tool_name}"
            }), 400
            
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