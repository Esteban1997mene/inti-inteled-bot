import streamlit as st
from google import genai
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="INTI | Asistente Virtual de INTILED",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

/* Ocultar elementos de Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Fondo */
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(255, 196, 0, 0.08), transparent 25%),
        linear-gradient(180deg, #ffffff 0%, #f7f8fa 100%);
}

/* Contenedor principal */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Encabezado */
.inti-header {
    padding: 26px 30px;
    background: linear-gradient(135deg, #15171c, #262a32);
    border-radius: 24px;
    margin-bottom: 24px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.10);
}

.inti-brand {
    font-size: 42px;
    font-weight: 800;
    color: white;
    letter-spacing: -1px;
    margin: 0;
}

.inti-brand span {
    color: #ffc400;
}

.inti-subtitle {
    color: #d7d9df;
    font-size: 16px;
    margin-top: 3px;
}

.inti-status {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 12px;
    border-radius: 100px;
    background: rgba(40, 200, 120, 0.15);
    color: #73e2a7;
    font-size: 12px;
    font-weight: 600;
}

/* Secciones */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #6d727c;
    margin-bottom: 18px;
}

/* Botones */
.stButton > button {
    width: 100%;
    min-height: 62px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    background: white;
    font-weight: 600;
    transition: all .20s ease;
    box-shadow: 0 3px 10px rgba(0,0,0,.03);
}

.stButton > button:hover {
    border-color: #ffc400;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,.07);
}

/* Chat */
[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid #eeeeee;
    border-radius: 18px;
    padding: 15px 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,.035);
}

/* Input del chat */
[data-testid="stChatInput"] {
    border-radius: 18px;
}

/* Separador */
.divider {
    height: 1px;
    background: #e9e9e9;
    margin: 28px 0;
}

/* Footer */
.inti-footer {
    text-align: center;
    color: #8a8f98;
    font-size: 12px;
    padding-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GEMINI
# ============================================================

api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("No se encontró GEMINI_API_KEY en Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)


SYSTEM_PROMPT = """
Eres INTI, el asistente virtual institucional de INTILED.

INTILED es una empresa relacionada con soluciones de iluminación,
tecnología, eficiencia energética y proyectos energéticos.

Tu misión es atender de manera profesional, amable y natural
a clientes, empresas, entidades públicas y ciudadanos.

Puedes:

- orientar inicialmente sobre servicios de INTILED;
- atender consultas sobre iluminación y eficiencia energética;
- orientar sobre alumbrado público;
- conversar sobre energía solar y soluciones energéticas;
- identificar oportunidades comerciales;
- ayudar a estructurar inicialmente solicitudes de cotización;
- orientar sobre reuniones y visitas técnicas;
- orientar sobre PQR/PQRS.

REGLAS IMPORTANTES:

- Nunca inventes precios.
- Nunca inventes contratos.
- Nunca inventes clientes.
- Nunca inventes teléfonos o correos.
- Nunca inventes direcciones.
- Nunca inventes proyectos ejecutados.
- Nunca inventes especificaciones técnicas de productos.
- Si no tienes información oficial de INTILED, dilo claramente.
- No confirmes una cita si todavía no existe un módulo de agenda.
- No confirmes una PQR si todavía no ha sido registrada.
- Cuando detectes una oportunidad comercial, haz preguntas
  progresivas para comprender el proyecto.
- Mantén respuestas claras, profesionales y relativamente breves.
- Tu nombre siempre es INTI.
- No te presentes como Gemini.
"""


def preguntar_a_inti(pregunta, historial):

    conversacion = ""

    for mensaje in historial[-10:]:

        if mensaje["role"] == "user":
            conversacion += f"\nCliente: {mensaje['content']}"

        elif mensaje["role"] == "assistant":
            conversacion += f"\nINTI: {mensaje['content']}"

    prompt = f"""
{SYSTEM_PROMPT}

CONVERSACIÓN RECIENTE:
{conversacion}

NUEVO MENSAJE DEL CLIENTE:
{pregunta}

Responde como INTI.
"""

    respuesta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return respuesta.text


# ============================================================
# ESTADO
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
                "¡Hola! 👋 Soy **INTI**, el asistente virtual de "
                "**INTILED**.\n\n"
                "Estoy aquí para orientarte sobre nuestros servicios "
                "y ayudarte con tu solicitud. ¿En qué puedo ayudarte?"
        }
    ]


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown("""
<div class="inti-header">

    <div class="inti-brand">
        INT<span>I</span> 💡
    </div>

    <div class="inti-subtitle">
        Asistente Virtual Inteligente de INTILED
    </div>

    <div class="inti-status">
        ● INTI está en línea
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# ACCESOS RÁPIDOS
# ============================================================

st.markdown(
    '<div class="section-title">¿Cómo puedo ayudarte?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Selecciona una opción o conversa directamente con INTI.'
    '</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    btn_servicios = st.button(
        "💡  Servicios",
        use_container_width=True
    )


with c2:

    btn_cotizacion = st.button(
        "📄  Cotización",
        use_container_width=True
    )


with c3:

    btn_cita = st.button(
        "📅  Agendar cita",
        use_container_width=True
    )


with c4:

    btn_pqr = st.button(
        "📋  PQR / PQRS",
        use_container_width=True
    )


# ============================================================
# MENSAJES DE ACCESO RÁPIDO
# ============================================================

if btn_servicios:

    st.session_state.messages.append({
        "role": "assistant",
        "content":
            "💡 Claro. Puedo ayudarte a conocer las soluciones de "
            "**INTILED**.\n\n"
            "Cuéntame qué necesitas: iluminación, alumbrado público, "
            "eficiencia energética, energía solar u otro proyecto."
    })


if btn_cotizacion:

    st.session_state.messages.append({
        "role": "assistant",
        "content":
            "📄 Con gusto te ayudo con una **solicitud de cotización**.\n\n"
            "Para comenzar, cuéntame brevemente qué proyecto o solución "
            "necesitas cotizar."
    })


if btn_cita:

    st.session_state.messages.append({
        "role": "assistant",
        "content":
            "📅 Puedo ayudarte a preparar una solicitud de "
            "**reunión o visita técnica**.\n\n"
            "Cuéntame primero cuál es el motivo de la reunión."
    })


if btn_pqr:

    st.session_state.messages.append({
        "role": "assistant",
        "content":
            "📋 Puedo orientarte sobre una **PQR/PQRS**.\n\n"
            "Indícame si deseas presentar una petición, queja, "
            "reclamo o sugerencia."
    })


# ============================================================
# CHAT
# ============================================================

st.markdown(
    '<div class="divider"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">💬 Conversa con INTI</div>',
    unsafe_allow_html=True
)


for mensaje in st.session_state.messages:

    avatar = "💡" if mensaje["role"] == "assistant" else "👤"

    with st.chat_message(
        mensaje["role"],
        avatar=avatar
    ):

        st.markdown(
            mensaje["content"]
        )


# ============================================================
# ENTRADA DEL USUARIO
# ============================================================

pregunta = st.chat_input(
    "Escribe tu mensaje para INTI..."
)


if pregunta:

    historial_anterior = list(
        st.session_state.messages
    )

    st.session_state.messages.append({
        "role": "user",
        "content": pregunta
    })


    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(pregunta)


    with st.chat_message(
        "assistant",
        avatar="💡"
    ):

        with st.spinner(
            "INTI está analizando tu solicitud..."
        ):

            try:

                respuesta = preguntar_a_inti(
                    pregunta,
                    historial_anterior
                )

            except Exception as error:

                respuesta = (
                    "En este momento tuve un inconveniente al "
                    "procesar tu consulta. Por favor intenta "
                    "nuevamente en unos instantes."
                )

                st.caption(
                    f"Error técnico: {error}"
                )

        st.markdown(respuesta)


    st.session_state.messages.append({
        "role": "assistant",
        "content": respuesta
    })


# ============================================================
# INFORMACIÓN INSTITUCIONAL
# ============================================================

st.markdown(
    '<div class="divider"></div>',
    unsafe_allow_html=True
)


with st.expander(
    "🏢 Conoce más sobre INTILED"
):

    st.markdown("""
**INTI** es el asistente virtual de **INTILED**.

Estamos construyendo progresivamente una plataforma capaz de integrar:

- 💡 Portafolio de servicios
- 🤖 Atención inteligente
- 📄 Solicitudes de cotización
- 📅 Agendamiento de reuniones y visitas técnicas
- 📋 Gestión de PQR/PQRS
- 🌐 Información institucional
- 📚 Documentación técnica
- 👨‍💼 Derivación a asesores
""")


# ============================================================
# FOOTER
# ============================================================

año = datetime.now().year

st.markdown(
    f"""
    <div class="inti-footer">

        <strong>INTI</strong>
        · Asistente Virtual Inteligente de INTILED

        <br><br>

        © {año} INTILED · Todos los derechos reservados

        <br>

        Las recomendaciones de INTI no sustituyen
        la validación técnica o comercial de INTILED.

    </div>
    """,
    unsafe_allow_html=True
)
