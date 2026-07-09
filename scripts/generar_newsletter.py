import os
import requests
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────
GROQ_API_KEY   = os.environ["GROQ_API_KEY"]
TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]

GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
TAVILY_URL = "https://api.tavily.com/search"
MODEL      = "llama-3.3-70b-versatile"

fecha_hoy     = datetime.now().strftime("%d de %B de %Y")
fecha_archivo = datetime.now().strftime("%Y-%m-%d")

# ─── Búsquedas con Tavily ─────────────────────────────────────────────────────
def buscar(query, max_results=5):
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "include_answer": False,
        "days": 2
    }
    r = requests.post(TAVILY_URL, json=payload)
    r.raise_for_status()
    resultados = r.json().get("results", [])
    return "\n\n".join(
        f"- [{item['title']}]({item['url']})\n  {item.get('content', '')[:300]}"
        for item in resultados
    )

print("🔍 Buscando noticias del día...")

noticias = {
    "cardiologia": buscar("arritmias electrofisiologia cardiologia noticias estudio 2026"),
    "economia":    buscar("mercados financieros economia España noticias hoy 2026"),
    "deporte":     buscar("ciencia ejercicio deporte evidencia estudio 2026"),
    "prensa":      buscar("noticias España hoy El País El Mundo Canarias 2026"),
    "paper":       buscar("cardiology arrhythmia electrophysiology new study published 2026"),
}

print("✅ Búsquedas completadas. Generando newsletter...")

# ─── Prompt ───────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres un agente periodístico personal llamado "El Diario de Santiago".
Tu misión es generar cada mañana un periódico digital de consulta diaria,
personalizado, riguroso y accionable, para un cardiólogo electrofisiólogo
en formación, apasionado del deporte basado en evidencia y activo inversor particular.

PERFIL DEL LECTOR:
- Cardiólogo en formación en arritmias y electrofisiología clínica
- Fellow en Las Palmas de Gran Canaria, España
- Interés activo en inversión (value investing, mercados, macro)
- Deportista: ciclismo, fuerza, cardio basado en evidencia científica
- Perfil técnico-científico: valora metodología, no solo titulares

REGLAS GENERALES:
- Resúmenes en español, términos técnicos en inglés cuando sea estándar clínico
- Usa SOLO la información de las búsquedas proporcionadas; no inventes noticias
- Tono riguroso pero ágil. Asume conocimiento médico avanzado en cardiología
- Siempre incluye fuente completa y fecha de publicación
- Formato: Markdown limpio y optimizado para lectura en pantalla
- Si una búsqueda no tiene resultados relevantes, indícalo explícitamente"""

USER_PROMPT = f"""Genera la edición completa de hoy, {fecha_hoy}, de El Diario de Santiago.
Basa cada sección EXCLUSIVAMENTE en los resultados de búsqueda que te proporciono.

=== RESULTADOS DE BÚSQUEDA ===

[CARDIOLOGÍA Y ARRITMIAS]
{noticias['cardiologia']}

[ECONOMÍA Y MERCADOS]
{noticias['economia']}

[DEPORTE Y CIENCIA]
{noticias['deporte']}

[PRENSA NACIONAL]
{noticias['prensa']}

[PAPER DEL DÍA]
{noticias['paper']}

=== ESTRUCTURA REQUERIDA ===

# 📰 El Diario de Santiago — {fecha_hoy}

> **Titular del día:** [Una frase que resume el tema más relevante]

---

## 🫀 1. Cardiología y Arritmias
3 ítems. Por cada uno:
- **Titular**
- Resumen 3-4 líneas (qué se estudió, resultado, n muestral si aplica)
- 🏥 Implicación clínica práctica (1 línea)
- 🔗 Enlace o DOI

---

## 📈 2. Economía y Mercados
3 ítems. Por cada uno:
- **Titular**
- Resumen 3 líneas (contexto macro, dato clave, implicación)
- 📊 Dato concreto: índice, porcentaje, precio
- Relevancia para inversor particular español

---

## 🚴 3. Deporte y Ciencia del Ejercicio
2 ítems. Por cada uno:
- **Titular**
- Resumen metodológico breve
- 🏋️ Aplicación práctica para el entrenamiento
- 🔗 Enlace

---

## 📰 4. Prensa Nacional
3 ítems. Prioriza: sanidad, política económica, ciencia, Canarias.
- **Titular** — Fuente — Fecha
- Resumen 2 líneas

---

## 🔬 5. Paper del Día
- Título completo y autores
- Revista y factor de impacto aproximado
- Abstract resumido en 5 líneas (PICO si aplica)
- Por qué es relevante para Santiago
- 🔗 DOI o enlace

---

## ⚙️ 6. Actualización GitHub
Repositorios a revisar:
- https://github.com/Santiagomartingomero/agente-IA-INVERSION-
- https://github.com/Santiagomartingomero/agente-arritmias-literatura-
- https://github.com/Santiagomartingomero/plan-entrenamiento-mensual

Indica: último commit conocido, issues abiertos si los hay, sugerencia de próximo paso.

---

## 🧠 7. Reflexión del Día
Una paradoja clínica, dato económico contraintuitivo o hallazgo deportivo sorprendente.
Máximo 4 líneas.

---
*Generado automáticamente por El Diario de Santiago · {fecha_hoy} · Las Palmas de Gran Canaria*
"""

# ─── Llamada a Groq ───────────────────────────────────────────────────────────
response = requests.post(
    GROQ_URL,
    headers={
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": USER_PROMPT}
        ],
        "temperature": 0.2,
        "max_tokens": 4096
    }
)
response.raise_for_status()

contenido = response.json()["choices"][0]["message"]["content"]

# ─── Guardar edición ──────────────────────────────────────────────────────────
os.makedirs("ediciones", exist_ok=True)
ruta = f"ediciones/{fecha_archivo}.md"

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print(f"✅ Edición guardada en {ruta}")
