import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ─── Config ───────────────────────────────────────────────────────────────────
API_KEY = os.environ["PERPLEXITY_API_KEY"]
API_URL = "https://api.perplexity.ai/chat/completions"
MODEL   = "sonar"   # modelo con búsqueda web en tiempo real

fecha_hoy = datetime.now().strftime("%d de %B de %Y")
fecha_archivo = datetime.now().strftime("%Y-%m-%d")

# ─── Prompt del agente ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres un agente periodístico personal llamado \"El Diario de Santiago\".
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
- Noticias de las últimas 24-48 horas. Si no las hay, usa las más recientes de 7 días e indícalo
- Tono riguroso pero ágil. Asume conocimiento médico avanzado en cardiología
- Siempre incluye fuente completa y fecha de publicación
- Formato: Markdown limpio y optimizado para lectura en pantalla
- No rellenes con noticias irrelevantes; si una sección está vacía, dilo"""

USER_PROMPT = f"""Genera la edición completa de hoy, {fecha_hoy}, de El Diario de Santiago.

Sigue EXACTAMENTE esta estructura:

# 📰 El Diario de Santiago — {fecha_hoy}

> **Titular del día:** [Una frase que resume el tema más relevante de la jornada]

---

## 🫀 1. Cardiología y Arritmias
Fuentes: PubMed, JACC, Heart Rhythm, EP Europace, NEJM, ESC/HRS.
3 noticias o papers. Por cada ítem:
- Titular
- Resumen 3-4 líneas (qué se estudió, resultado, n muestral si aplica)
- 🏥 Implicación clínica práctica (1 línea)
- 🔗 DOI o enlace

---

## 📈 2. Economía y Mercados
Fuentes: Financial Times, El Economista, Expansión, Reuters, Bloomberg, El País Economía.
3 noticias del día. Por cada ítem:
- Titular
- Resumen 3 líneas (contexto macro, dato clave, implicación)
- 📊 Dato concreto: índice, porcentaje, precio
- Relevancia para inversor particular español

---

## 🚴 3. Deporte y Ciencia del Ejercicio
Fuentes: BJSM, Journal of Physiology, Sports Medicine.
2 noticias o estudios. Por cada ítem:
- Titular
- Resumen metodológico breve (tipo de estudio, muestra, intervención)
- 🏋️ Aplicación práctica para el entrenamiento
- 🔗 Enlace si disponible

---

## 📰 4. Prensa Nacional
Fuentes: El País, El Mundo, El Confidencial, La Provincia (Canarias).
3 noticias. Prioriza: sanidad, política económica, ciencia, Canarias.
Resumen de 2 líneas por ítem.

---

## 🔬 5. Paper del Día
El artículo más relevante de las últimas 48h en cualquiera de tus áreas.
- Título completo y autores
- Revista y factor de impacto aproximado
- Abstract resumido en 5 líneas (PICO si es ensayo clínico)
- Por qué es relevante para Santiago específicamente
- 🔗 DOI

---

## ⚙️ 6. Actualización GitHub
Revisa y reporta novedades en:
- https://github.com/Santiagomartingomero/agente-IA-INVERSION-
- https://github.com/Santiagomartingomero/agente-arritmias-literatura-
- https://github.com/Santiagomartingomero/plan-entrenamiento-mensual

Por repo: último commit (fecha + mensaje), issues abiertos, sugerencia de próximo paso.

---

## 🧠 7. Reflexión del Día
Una paradoja clínica, dato económico contraintuitivo o hallazgo deportivo sorprendente.
Máximo 4 líneas.

---
*Generado automáticamente por El Diario de Santiago · {fecha_hoy} · Las Palmas de Gran Canaria*
"""

# ─── Llamada a la API ─────────────────────────────────────────────────────────
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": USER_PROMPT}
    ],
    "max_tokens": 4000,
    "temperature": 0.2,
    "search_recency_filter": "day"
}

response = requests.post(API_URL, headers=headers, json=payload)
response.raise_for_status()

contenido = response.json()["choices"][0]["message"]["content"]

# ─── Guardar edición ──────────────────────────────────────────────────────────
os.makedirs("ediciones", exist_ok=True)
ruta = f"ediciones/{fecha_archivo}.md"

with open(ruta, "w", encoding="utf-8") as f:
    f.write(contenido)

print(f"✅ Edición guardada en {ruta}")
