# ⚙️ Configuración del Agente Automático

## APIs necesarias (ambas gratuitas, sin tarjeta)

| API | Para qué | Dónde crearla | Nombre del secret |
|-----|----------|---------------|-------------------|
| Groq | Generar el texto (LLaMA 3.3 70B) | [console.groq.com/keys](https://console.groq.com/keys) | `GROQ_API_KEY` |
| Tavily | Buscar noticias en tiempo real | [app.tavily.com](https://app.tavily.com) | `TAVILY_API_KEY` |

## Añadir los secrets a GitHub

1. Ve a **Settings → Secrets and variables → Actions**
2. Crea dos secrets:
   - Nombre: `GROQ_API_KEY` → tu key de Groq (empieza por `gsk_...`)
   - Nombre: `TAVILY_API_KEY` → tu key de Tavily (empieza por `tvly-...`)

## Ejecución automática

El agente se ejecuta **de lunes a viernes a las 7:00 WEST** automáticamente.

## Ejecución manual

1. Ve a **Actions** → **📰 Generar Newsletter Diaria**
2. Pulsa **Run workflow**

## Dónde leer cada edición

Cada edición se guarda en `ediciones/YYYY-MM-DD.md`.

## Coste

**€0,00** — ambas APIs tienen tier gratuito más que suficiente para 1 newsletter diaria.
