import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Asistente Virtual ATMCE",
    page_icon="📡",
    layout="centered"
)

st.title("📡 Asistente Virtual ATMCE")
st.caption("Academia Militar de Comunicaciones y Electrónica — Apoyo Académico con IA")

api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("⚠️ Falta configurar `GEMINI_API_KEY` en los Secrets de Streamlit.")
    st.stop()

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = (
    "Eres el Asistente Virtual Académico de la Academia Militar de Comunicaciones y Electrónica (ATMCE). "
    "Tu objetivo es apoyar a cadetes, estudiantes e instructores en materias de telecomunicaciones, "
    "electrónica, redes, sistemas de radio, matemáticas aplicadas, física y estudio académico general. "
    "Responde siempre en español con tono respetuoso, disciplinado, claro, preciso y pedagógico. "
    "Cuando expliques ejercicios o conceptos técnicos, hazlo paso a paso y con ejemplos prácticos."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Bienvenido, cadete! Soy el Asistente Virtual de la ATMCE. ¿En qué tema de electrónica, comunicaciones o estudio te puedo apoyar hoy?"
        }
    ]

with st.sidebar:
    st.header("Opciones")
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversación reiniciada. ¿En qué puedo ayudarte ahora?"
            }
        ]
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu consulta académica aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Procesando consulta..."):
            try:
                contenido_historial = []
                for m in st.session_state.messages:
                    rol = "user" if m["role"] == "user" else "model"
                    contenido_historial.append(
                        types.Content(
                            role=rol,
                            parts=[types.Part.from_text(text=m["content"])]
                        )
                    )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contenido_historial,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4,
                    ),
                )
                respuesta_texto = response.text or "No se obtuvo respuesta del modelo."
            except Exception as e:
                respuesta_texto = f"Ocurrió un error al consultar Gemini: {e}"

            st.markdown(respuesta_texto)

    st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
