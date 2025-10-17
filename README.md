# Claude MCP Server para OpenAI

Servidor MCP (Model Context Protocol) que permite a agentes de OpenAI llamar a modelos de Claude.

## 🚀 Despliegue en Railway

### Paso 1: Preparar el repositorio
1. Sube este código a un repositorio de GitHub
2. Asegúrate de que todos los archivos estén incluidos

### Paso 2: Desplegar en Railway
1. Ve a [Railway.app](https://railway.app)
2. Crea un nuevo proyecto desde tu repositorio GitHub
3. Railway detectará automáticamente el `Procfile` y el `runtime.txt`

### Paso 3: Configurar variables de entorno
En Railway, ve a la pestaña "Variables" y agrega:
- `ANTHROPIC_API_KEY`: Tu API key de Anthropic

### Paso 4: Obtener la URL
Una vez desplegado, Railway te proporcionará una URL como:
```
https://tu-proyecto.up.railway.app
```

## 🔌 Conectar con OpenAI

### En el formulario de OpenAI:

**URL:**
```
https://tu-proyecto.up.railway.app
```

**Label:**
```
claude_mcp_server
```

**Description:** (opcional)
```
Servidor MCP para llamar a modelos de Claude
```

**Authentication:**
- Por ahora: Selecciona "Sin autenticación" o deja el token vacío
- Para producción: Implementaremos autenticación posteriormente

## 📡 Endpoints disponibles

- `GET /` - Estado del servidor
- `GET /mcp/v1/tools` - Lista las herramientas disponibles
- `POST /mcp/v1/call_tool` - Ejecuta una herramienta
- `GET /mcp/v1/resources` - Lista los recursos
- `GET /mcp/v1/prompts` - Lista los prompts

## 🛠️ Herramienta disponible

### `call_claude`

Llama a un modelo de Claude con un prompt específico.

**Parámetros:**
- `model` (string, requerido): El modelo de Claude (ej: "claude-3-5-sonnet-20241022")
- `prompt` (string, requerido): El prompt a enviar
- `max_tokens` (number, opcional): Máximo de tokens (default: 1024)

**Ejemplo de uso desde OpenAI:**
El agente de OpenAI puede decir:
"Usa Claude para responder: ¿Qué es la inteligencia artificial?"

Y automáticamente se conectará a este servidor MCP para obtener la respuesta de Claude.

## 🧪 Prueba local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variable de entorno
cp .env.example .env
# Edita .env y agrega tu ANTHROPIC_API_KEY

# Ejecutar servidor
python app.py
```

El servidor estará disponible en `http://localhost:8080`

## 📝 Notas

- El servidor está configurado sin autenticación para pruebas
- Para producción, se debe implementar autenticación con API keys
- Asegúrate de que tu API key de Anthropic tenga saldo suficiente

