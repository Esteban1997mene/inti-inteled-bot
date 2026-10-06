import streamlit as st
import requests
from streamlit_lottie import st_lottie

# -----------------------------------------------------------------------------
# 1. Configuración de la página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="INTI - Chatbot INTELED",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ocultar estilos por defecto de Streamlit para una integración limpia vía iframe
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #FAFAFA;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. Carga de animaciones Lottie (Avatar INTI)
# -----------------------------------------------------------------------------
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

# URL de animación Lottie (puedes reemplazarla por la URL JSON que elijas de LottieFiles)
LOTTIE_URL = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
inti_animation = load_lottieurl(LOTTIE_URL)


# -----------------------------------------------------------------------------
# 3. Encabezado e Interfaz Principal de INTI
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1, 3])

with col1:
    if inti_animation:
        st_lottie(inti_animation, height=100, key="inti_avatar")
    else:
        st.markdown("<h1 style='text-align: center;'>💡</h1>", unsafe_allow_html=True)

with col2:
    st.markdown("## **INTI** | Asistente INTELED 🤖")
    st.caption("Soluciones en Iluminación y Eficiencia Energética")

st.markdown("---")


# -----------------------------------------------------------------------------
# 4. Estado de Sesión / Historial de Chat
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "¡Hola! Soy **INTI**, tu asistente virtual de **INTELED**. ¿En qué puedo ayudarte hoy?"
        }
    ]

# Renderizar mensajes anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------------------------------------------------------
# 5. Botones de Navegación Rápida
# -----------------------------------------------------------------------------
st.write("**Opciones rápidas:**")
btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

selected_option = None

if btn_col1.button("💰 Cotizar"):
    selected_option = "Cotización"
if btn_col2.button("📅 Agendar"):
    selected_option = "Visita Técnica"
if btn_col3.button("📋 PQRS"):
    selected_option = "PQRS"
if btn_col4.button("❓ Ayuda"):
    selected_option = "Atención al Cliente"


# -----------------------------------------------------------------------------
# 6. Procesamiento de Mensajes y Lógica de Flujo
# -----------------------------------------------------------------------------
user_input = st.chat_input("Escribe tu consulta aquí...")

prompt = selected_option if selected_option else user_input

if prompt:
    # Agregar mensaje del usuario al chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()
    bot_response = ""

    # Flujo: Cotizaciones
    if "cotiz" in prompt_lower:
        bot_response = (
            "### 💰 **Solicitud de Cotización**\n"
            "Para ayudarte con una cotización precisa, indícame por favor:\n"
            "* **Nombre o Empresa**\n"
            "* **Tipo de proyecto** (Iluminación comercial, industrial, pública, etc.)\n"
            "* **Unidades o área aproximada (m²)**\n\n"
            "*Un asesor del equipo comercial se pondrá en contacto contigo a la brevedad.*"
        )

    # Flujo: Agendamiento de Visitas
    elif "agendar" in prompt_lower or "visit" in prompt_lower:
        bot_response = (
            "### 📅 **Programación de Visita Técnica**\n"
            "Con gusto coordinamos una inspección o visita técnica.\n"
            "Por favor proporciona los siguientes datos:\n"
            "1. **Dirección / Ciudad del proyecto**\n"
            "2. **Día y horario de preferencia** (Lunes a Viernes)\n"
            "3. **Teléfono de contacto**"
        )

    # Flujo: PQRS
    elif "pqrs" in prompt_lower or "queja" in prompt_lower or "reclamo" in prompt_lower:
        bot_response = (
            "### 📋 **Módulo de PQRS**\n"
            "Lamentamos si has tenido un inconveniente. Registraré tu caso formalmente.\n\n"
            "Por favor ayúdame con:\n"
            "* **Nombre completo / NIT**\n"
            "* **Número de factura o proyecto**\n"
            "* **Descripción detallada del requerimiento o reclamación**"
        )

    # Flujo: Atención al Cliente / Información General
    elif "ayuda" in prompt_lower or "atención" in prompt_lower or "contacto" in prompt_lower:
        bot_response = (
            "### 💡 **Atención al Cliente INTELED**\n"
            "Puedo ayudarte a resolver tus dudas sobre:\n"
            "- Portafolio de productos y luminarias LED\n"
            "- Estado de proyectos en ejecución\n"
            "- Asesoría en proyectos de eficiencia energética\n\n"
            "Escribe tu duda detallada o selecciona una opción del menú superior."
        )

    # Respuesta General
    else:
        bot_response = (
            f"Gracias por comunicarte con **INTELED**. He recibido tu mensaje: *\"{prompt}\"*.\n\n"
            "¿Te gustaría que te ayude a **cotizar**, **agendar una visita** o **registrar una solicitud (PQRS)**?"
        )

    # Mostrar respuesta de INTI y guardarla en el historial
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
