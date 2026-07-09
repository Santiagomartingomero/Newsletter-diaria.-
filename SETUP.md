# ⚙️ Configuración del Agente Automático

## Paso único: añadir tu API Key como GitHub Secret

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** → **Secrets and variables** → **Actions**
3. Pulsa **New repository secret**
4. Nombre: `PERPLEXITY_API_KEY`
5. Valor: tu API key de Perplexity (empieza por `pplx-...`)
6. Guarda

¡Listo! El agente se ejecutará automáticamente **de lunes a viernes a las 7:00 WEST**.

## Ejecución manual

Si quieres generar la newsletter fuera del horario automático:
1. Ve a **Actions** en tu repo
2. Selecciona **📰 Generar Newsletter Diaria**
3. Pulsa **Run workflow**

## Dónde encontrar cada edición

Cada edición se guarda en `ediciones/YYYY-MM-DD.md` y es accesible
directamente desde GitHub.

## Modelo utilizado

- **Perplexity `sonar`**: modelo con búsqueda web en tiempo real,
  ideal para noticias de las últimas 24-48 horas.
- Coste estimado: ~$0.02-0.05 por edición diaria.

## Obtener tu API Key de Perplexity

https://www.perplexity.ai/settings/api
