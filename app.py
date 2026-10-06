import streamlit as st
from google import genai

st.set_page_config(
    page_title="Prueba Gemini - INTI",
    page_icon="🤖"
)

st.title("🧪 Prueba de conexión INTI ↔ Gemini")
st.write("Esta pantalla es temporal. Solo comprobaremos la conexión.")

# Verificar que Streamlit encuentre la clave
api_key = st.secrets.get("GEMINI_API_KEY", "")

if api_key:
    st.success("✅ GEMINI_API_KEY detectada correctamente.")
else:
    st.error("❌ Streamlit no encuentra GEMINI_API_KEY.")
    st.stop()

pregunta = st.text_input(
    "Escribe una pregunta:",
    value="Hola. Preséntate brevemente como INTI, asistente virtual de INTILED."
)

if st.button("🚀 Probar Gemini"):

    try:

        with st.spinner("Conectando con Gemini..."):

            client = genai.Client(
                api_key=api_key
            )

            respuesta = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=pregunta
            )

        st.success("✅ ¡Gemini respondió correctamente!")

        st.markdown("### 🤖 Respuesta")

        st.write(
            respuesta.text
        )

    except Exception as error:

        st.error("❌ Gemini no pudo responder.")

        st.markdown("### Error técnico")

        st.code(str(error))
