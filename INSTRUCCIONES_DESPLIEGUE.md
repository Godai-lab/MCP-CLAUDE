# 📋 Instrucciones Rápidas de Despliegue

## 🎯 Pasos para desplegar en Railway

### 1. Preparar el código
✅ Ya está listo - ahora usa el SDK oficial de MCP

### 2. Subir a GitHub (si aún no lo has hecho)
```bash
git add .
git commit -m "Actualizado a SDK oficial de MCP"
git push origin main
```

### 3. Desplegar en Railway

1. **Ve a Railway**: https://railway.app
2. **New Project** → **Deploy from GitHub repo**
3. **Selecciona tu repositorio**: Claude-railway
4. Railway comenzará a desplegar automáticamente

### 4. Agregar variable de entorno en Railway

En tu proyecto de Railway:
1. Ve a la pestaña **"Variables"**
2. Click en **"New Variable"**
3. Agrega:
   - **Key**: `ANTHROPIC_API_KEY`
   - **Value**: Tu API key de Anthropic (empieza con `sk-ant-...`)
4. Guarda los cambios

### 5. Obtener tu URL

1. En Railway, ve a la pestaña **"Settings"**
2. En la sección **"Networking"**, encontrarás tu URL pública
3. Se verá algo como: `https://claude-railway-production.up.railway.app`
4. **¡Copia esta URL!**

## 🔗 Conectar con OpenAI

### En el formulario que te muestra OpenAI:

**🌐 URL:**
```
https://tu-dominio.up.railway.app
```
*(Pega aquí la URL que obtuviste de Railway)*

**🏷️ Label:**
```
claude_mcp
```

**📝 Description:** *(opcional)*
```
Servidor MCP para usar modelos de Claude
```

**🔐 Authentication:**
```
Por ahora déjalo sin token (o selecciona "Sin autenticación")
```

### ✅ Hacer click en "Connect"

¡Listo! Ahora tu agente de OpenAI podrá usar Claude.

## 🧪 Probar la conexión

### 1. Primero verifica que el servidor esté funcionando:
Abre en tu navegador:
```
https://tu-dominio.up.railway.app/
```

Deberías ver:
```json
{
  "name": "Claude MCP Server",
  "version": "1.0.0",
  "description": "Servidor MCP para conectar OpenAI con Claude",
  "status": "online"
}
```

### 2. Verifica las herramientas disponibles:
```
https://tu-dominio.up.railway.app/mcp/v1/tools
```

Deberías ver la herramienta `call_claude` listada.

### 3. Prueba desde OpenAI:
Dile al agente de OpenAI algo como:
```
"Usa Claude para responderme: ¿Cuál es la capital de Francia?"
```

El agente debería conectarse a tu servidor MCP y obtener la respuesta de Claude.

## 🎯 Ejemplo de uso

**Usuario a OpenAI:**
> "Necesito que uses Claude modelo sonnet para explicarme qué es la física cuántica"

**OpenAI internamente:**
1. Detecta que necesita usar el servidor MCP "claude_mcp"
2. Llama a tu servidor en Railway
3. Tu servidor llama a la API de Claude
4. Claude responde
5. OpenAI recibe y muestra la respuesta al usuario

## ⚠️ Notas importantes

- **ANTHROPIC_API_KEY**: Debe estar configurada en Railway para que funcione
- **Sin autenticación**: Por ahora está sin protección, solo para pruebas
- **Costos**: Cada llamada a Claude consume tokens de tu cuenta de Anthropic
- **Logs**: Puedes ver los logs en Railway para debug

## 🔧 Para desarrollo local

Si quieres probarlo localmente antes:

```bash
# 1. Crear archivo .env
echo "ANTHROPIC_API_KEY=tu-key-aqui" > .env

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar servidor
python app.py
```

El servidor correrá en `http://localhost:8080`

## 📞 Necesitas ayuda?

- **Logs de Railway**: Ve a la pestaña "Deployments" en Railway
- **Estado del servidor**: Accede a `https://tu-dominio.up.railway.app/`
- **Verificar API key**: Asegúrate de que esté bien configurada en Railway

---

**¡Todo está listo para desplegar! 🚀**

