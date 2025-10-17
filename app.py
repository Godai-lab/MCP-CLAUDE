import asyncio
import json
import os
import requests
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

load_dotenv()

# Configuración
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Crear servidor MCP
server = Server("claude-mcp-server")

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

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Lista las herramientas disponibles"""
    return [
        Tool(
            name="call_claude",
            description="Llama a Claude con el modelo especificado y retorna la respuesta",
            inputSchema={
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
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ejecuta una herramienta"""
    if name == "call_claude":
        result = call_claude(
            model=arguments["model"],
            prompt=arguments["prompt"],
            max_tokens=arguments.get("max_tokens", 1024),
        )
        return [TextContent(type="text", text=result)]
    else:
        raise Exception(f"Unknown tool: {name}")

async def main():
    """Función principal"""
    print("🚀 Claude MCP Server iniciado")
    print("📡 Usando SDK oficial de MCP")
    
    # Ejecutar servidor MCP
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())