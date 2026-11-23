import os
import gradio as gr
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = (
    "Eres un asistente virtual académico de apoyo para cadetes y estudiantes "
    "de la Academia Militar de Comunicaciones y Electrónica (ATMCE). "
    "Responde de forma clara, respetuosa y útil."
)

def responder(message, history):
    if not api_key:
        return "Error: falta configurar la variable de entorno GEMINI_API_KEY."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
            config={
                "system_instruction": SYSTEM_PROMPT,
            },
        )
        return response.text or "No se recibió respuesta del modelo."
    except Exception as e:
        return f"Ocurrió un error al consultar Gemini: {e}"

demo = gr.ChatInterface(
    fn=responder,
    title="Asistente Virtual ATMCE",
    description="Asistente académico con Google Gemini para cadetes y estudiantes.",
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)