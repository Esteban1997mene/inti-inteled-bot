import streamlit as st
from datetime import datetime

from modules.inti_ai import responder_inti


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="INTI | Asistente Virtual INTILED",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

/* Ocultar elementos innecesarios de Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Ancho general */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Fondo */
.stApp {
    background: #f7f8fa;
}

/* Botones */
.stButton > button {
    width: 100%;
    min-height: 55px;
    border-radius: 14px;
    border: 1px solid #e3e6ea;
    background-color: white;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    border-color: #f5b800;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.07);
    transform: translateY(-2px);
}

/* Caja de texto */
.stTextInput input {
    border-radius: 12px;
}

/* Mensajes */
[data-testid="stChatMessage"] {
    background-color: white;
    border: 1px solid #e9eaed;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 10px;
}

/* Formularios */
[data-testid="stForm"] {
    background-color: white;
    border: 1px solid #e4e6e9;
    border-radius: 18px;
    padding: 18px;
}

/* Quitar espacio excesivo */
hr {
    margin-top: 25px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# API KEY
# ============================================================

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    ""
)

if not api_key:

    st.error(
        "No se encontró GEMINI_API_KEY en Streamlit Secrets."
    )

    st.stop()


# ============================================================
# HISTORIAL
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",
            "content":
                "¡Hola! 👋 Soy **INTI**, el asistente virtual "
                "de **INTILED**.\n\n"
                "Estoy aquí para orientarte y ayudarte con tu "
                "solicitud.\n\n"
                "**¿En qué puedo ayudarte hoy?**"
        }

    ]


# ============================================================
# FUNCIÓN PARA PROCESAR MENSAJES
# ============================================================

def procesar_mensaje(pregunta):

    if not pregunta:
        return

    historial_anterior = list(
        st.session_state.messages
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    try:

        respuesta = responder_inti(
            pregunta=pregunta,
            historial=historial_anterior,
            api_key=api_key
        )

    except Exception as error:

        respuesta = (
            "⚠️ En este momento tuve un inconveniente "
            "al procesar tu consulta. "
            "Por favor intenta nuevamente."
        )

        st.session_state["ultimo_error"] = str(error)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": respuesta
        }
    )


# ============================================================
# CABECERA
# ============================================================

col_logo, col_titulo, col_estado = st.columns(
    [1, 6, 2],
    vertical_alignment="center"
)

with col_logo:

    st.markdown("# 💡")


with col_titulo:

    st.title("INTI")

    st.caption(
        "Asistente Virtual Inteligente de INTILED"
    )


with col_estado:

    st.success("● En línea")


st.write(
    "**Atención inteligente para iluminación, energía, "
    "proyectos y servicios de INTILED.**"
)

st.divider()


# ============================================================
# BIENVENIDA
# ============================================================

st.subheader(
    "👋 Hola, soy INTI"
)

st.write(
    "Selecciona una opción o cuéntame directamente "
    "qué necesitas."
)


# ============================================================
# ACCESOS RÁPIDOS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    servicios = st.button(
        "💡\n\nServicios",
        use_container_width=True
    )


with c2:

    cotizacion = st.button(
        "💰\n\nCotización",
        use_container_width=True
    )


with c3:

    cita = st.button(
        "📅\n\nAgendar cita",
        use_container_width=True
    )


with c4:

    pqr = st.button(
        "📋\n\nPQR / PQRS",
        use_container_width=True
    )


# ============================================================
# ACCIONES
# ============================================================

if servicios:

    procesar_mensaje(
        "Quiero conocer los servicios que ofrece INTILED."
    )

    st.rerun()


if cotizacion:

    procesar_mensaje(
        "Quiero solicitar una cotización para un proyecto."
    )

    st.rerun()


if cita:

    procesar_mensaje(
        "Quiero solicitar una reunión o visita técnica."
    )

    st.rerun()


if pqr:

    procesar_mensaje(
        "Necesito orientación para presentar una PQR o PQRS."
    )

    st.rerun()


# ============================================================
# CONVERSACIÓN
# ============================================================

st.divider()

st.subheader(
    "💬 Conversa con INTI"
)


for mensaje in st.session_state.messages:

    if mensaje["role"] == "assistant":

        avatar = "💡"

    else:

        avatar = "👤"


    with st.chat_message(
        mensaje["role"],
        avatar=avatar
    ):

        st.markdown(
            mensaje["content"]
        )


# ============================================================
# CAMPO PARA ESCRIBIR
# ============================================================

st.write("")

with st.form(
    "formulario_inti",
    clear_on_submit=True
):

    col_texto, col_enviar = st.columns(
        [6, 1],
        vertical_alignment="bottom"
    )


    with col_texto:

        pregunta = st.text_input(
            "Mensaje",
            placeholder="Escribe tu mensaje para INTI...",
            label_visibility="collapsed"
        )


    with col_enviar:

        enviar = st.form_submit_button(
            "Enviar ➜",
            use_container_width=True
        )


if enviar and pregunta:

    procesar_mensaje(
        pregunta
    )

    st.rerun()


# ============================================================
# LIMPIAR CONVERSACIÓN
# ============================================================

col_vacio, col_limpiar = st.columns(
    [5, 2]
)


with col_limpiar:

    if st.button(
        "🗑️ Nueva conversación",
        use_container_width=True
    ):

        st.session_state.messages = [

            {
                "role": "assistant",
                "content":
                    "¡Hola! 👋 Soy **INTI**, el asistente "
                    "virtual de **INTILED**.\n\n"
                    "**¿Cómo puedo ayudarte?**"
            }

        ]

        st.rerun()


# ============================================================
# INFORMACIÓN
# ============================================================

st.divider()


with st.expander(
    "🏢 Acerca de INTILED e INTI"
):

    st.write(
        "INTI es el asistente virtual institucional de INTILED."
    )

    st.write(
        "Actualmente estamos desarrollando sus capacidades "
        "para integrar información institucional, servicios, "
        "cotizaciones, citas, PQR/PQRS y atención comercial."
    )


# ============================================================
# PIE DE PÁGINA
# ============================================================

año = datetime.now().year

st.divider()

st.caption(
    f"INTI · Asistente Virtual Inteligente de INTILED · "
    f"© {año} INTILED"
)

st.caption(
    "La información técnica o comercial relevante debe ser "
    "validada por personal autorizado de INTILED."
)
