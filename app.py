import streamlit as st
import requests
from streamlit_lottie import st_lottie
from datetime import datetime

# ============================================================
# INTI - ASISTENTE VIRTUAL DE INTILED
# Archivo principal de la aplicación
# Versión inicial: 0.1
# ============================================================


# ------------------------------------------------------------
# 1. CONFIGURACIÓN GENERAL
# ------------------------------------------------------------

st.set_page_config(
    page_title="INTI | Asistente Virtual INTILED",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ------------------------------------------------------------
# 2. ESTILOS GENERALES
# ------------------------------------------------------------

st.markdown("""
<style>

/* Ocultar elementos predeterminados de Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Fondo general */
.stApp {
    background: linear-gradient(
        135deg,
        #f5f7fa 0%,
        #eef2f7 100%
    );
}

/* Contenedor principal */
.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Título principal */
.inti-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

/* Subtítulo */
.inti-subtitle {
    font-size: 18px;
    color: #5f6368;
    margin-top: 0px;
}

/* Estado del bot */
.status-online {
    display: inline-block;
    background-color: #e8f5e9;
    color: #198754;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

/* Tarjetas */
.inti-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;

    box-shadow:
        0 4px 15px rgba(0,0,0,0.05);

    border:
        1px solid rgba(0,0,0,0.04);
}

/* Tarjetas de servicios */
.service-card {
    background: white;

    padding: 18px;

    border-radius: 16px;

    text-align: center;

    min-height: 145px;

    border:
        1px solid #eeeeee;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.service-card:hover {

    transform: translateY(-4px);

    box-shadow:
        0 8px 22px rgba(0,0,0,0.08);
}

/* Botones Streamlit */
.stButton > button {

    width: 100%;

    border-radius: 12px;

    font-weight: 600;

    min-height: 45px;

    transition: all 0.2s ease;
}

/* Caja del chat */
[data-testid="stChatMessage"] {

    background: rgba(255,255,255,0.75);

    border-radius: 16px;

    padding: 12px;

    margin-bottom: 10px;

    border:
        1px solid rgba(0,0,0,0.04);
}

/* Chat input */
[data-testid="stChatInput"] {

    border-radius: 15px;
}

/* Línea divisoria */
.inti-divider {

    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #d9d9d9,
            transparent
        );

    margin: 20px 0;
}

/* Pie */
.inti-footer {

    text-align: center;

    color: #888;

    font-size: 13px;

    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# 3. CARGA DE ANIMACIÓN LOTTIE
# ------------------------------------------------------------

@st.cache_data
def cargar_lottie(url):

    try:

        respuesta = requests.get(
            url,
            timeout=5
        )

        if respuesta.status_code == 200:
            return respuesta.json()

    except requests.RequestException:
        return None

    return None


LOTTIE_INTI = (
    "https://assets10.lottiefiles.com/"
    "packages/lf20_mbe35mca.json"
)

animacion_inti = cargar_lottie(
    LOTTIE_INTI
)


# ------------------------------------------------------------
# 4. FUNCIONES TEMPORALES
# ------------------------------------------------------------

def respuesta_temporal(pregunta):
    """
    Esta función será reemplazada posteriormente
    por el verdadero cerebro de IA de INTI.
    """

    pregunta_lower = pregunta.lower()

    if "hola" in pregunta_lower:

        return (
            "¡Hola! 👋 Soy **INTI**, el asistente virtual "
            "de **INTILED**.\n\n"
            "Estoy aquí para ayudarte con nuestros servicios, "
            "proyectos, solicitudes, visitas técnicas y atención "
            "al cliente."
        )

    if "solar" in pregunta_lower:

        return (
            "☀️ **Energía solar**\n\n"
            "INTILED desarrolla soluciones relacionadas con "
            "energía solar e iluminación eficiente.\n\n"
            "En las próximas versiones podré consultar "
            "directamente el portafolio y los proyectos "
            "institucionales para darte información más precisa."
        )

    if "cotiza" in pregunta_lower:

        return (
            "💰 Claro. Puedo ayudarte a iniciar una "
            "**solicitud de cotización**.\n\n"
            "Próximamente este módulo recopilará automáticamente "
            "la información de tu proyecto y la enviará al "
            "equipo comercial de INTILED."
        )

    if (
        "cita" in pregunta_lower
        or "visita" in pregunta_lower
    ):

        return (
            "📅 Puedo ayudarte a solicitar una "
            "**visita o reunión con INTILED**.\n\n"
            "Estamos preparando el módulo de agendamiento para "
            "consultar disponibilidad y registrar la cita."
        )

    if (
        "pqr" in pregunta_lower
        or "queja" in pregunta_lower
        or "reclamo" in pregunta_lower
    ):

        return (
            "📋 INTI contará con un módulo especializado para "
            "**PQR/PQRS**, donde podrás radicar y posteriormente "
            "consultar el estado de tu solicitud."
        )

    return (
        "Entiendo tu consulta. 💡\n\n"
        "Actualmente estoy en mi primera etapa de desarrollo. "
        "Muy pronto utilizaré inteligencia artificial para "
        "comprender preguntas abiertas y consultar automáticamente "
        "la información institucional de **INTILED**.\n\n"
        "Mientras tanto puedes preguntarme sobre **iluminación, "
        "energía solar, cotizaciones, visitas técnicas o PQR**."
    )


# ------------------------------------------------------------
# 5. INICIALIZAR VARIABLES DE SESIÓN
# ------------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",

            "content":
                "¡Hola! 👋 Soy **INTI**, el asistente virtual "
                "de **INTILED**.\n\n"
                "Estoy aquí para orientarte y ayudarte a conectar "
                "con nuestros servicios.\n\n"
                "**¿Qué necesitas hoy?**"
        }

    ]


# ------------------------------------------------------------
# 6. ENCABEZADO
# ------------------------------------------------------------

col_robot, col_header = st.columns(
    [1, 4],
    vertical_alignment="center"
)


with col_robot:

    if animacion_inti:

        st_lottie(
            animacion_inti,
            height=130,
            key="inti_robot"
        )

    else:

        st.markdown(
            """
            <div style="
                font-size:70px;
                text-align:center;
            ">
            💡
            </div>
            """,
            unsafe_allow_html=True
        )


with col_header:

    st.markdown(
        """
        <div class="inti-title">
            INTI
        </div>

        <div class="inti-subtitle">
            Asistente Virtual Inteligente de INTILED
        </div>

        <br>

        <span class="status-online">
            ● En línea
        </span>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="inti-divider"></div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# 7. ACCIONES RÁPIDAS
# ------------------------------------------------------------

st.markdown(
    "### ¿Cómo puedo ayudarte?"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        """
        <div class="service-card">

        <div style="font-size:35px">
        💡
        </div>

        <b>Servicios</b>

        <br>

        <small>
        Conoce las soluciones de INTILED
        </small>

        </div>
        """,
        unsafe_allow_html=True
    )

    servicios = st.button(
        "Consultar servicios",
        key="btn_servicios"
    )


with col2:

    st.markdown(
        """
        <div class="service-card">

        <div style="font-size:35px">
        📅
        </div>

        <b>Agendar cita</b>

        <br>

        <small>
        Solicita atención comercial o técnica
        </small>

        </div>
        """,
        unsafe_allow_html=True
    )

    cita = st.button(
        "Agendar",
        key="btn_cita"
    )


with col3:

    st.markdown(
        """
        <div class="service-card">

        <div style="font-size:35px">
        📋
        </div>

        <b>PQR / PQRS</b>

        <br>

        <small>
        Radica o consulta una solicitud
        </small>

        </div>
        """,
        unsafe_allow_html=True
    )

    pqr = st.button(
        "Ir a PQR",
        key="btn_pqr"
    )


with col4:

    st.markdown(
        """
        <div class="service-card">

        <div style="font-size:35px">
        💰
        </div>

        <b>Cotización</b>

        <br>

        <small>
        Cuéntanos sobre tu proyecto
        </small>

        </div>
        """,
        unsafe_allow_html=True
    )

    cotizacion = st.button(
        "Solicitar cotización",
        key="btn_cotizacion"
    )


# ------------------------------------------------------------
# 8. RESPUESTAS DE BOTONES RÁPIDOS
# ------------------------------------------------------------

if servicios:

    st.session_state.messages.append(
        {
            "role": "assistant",

            "content":
                "💡 **Servicios de INTILED**\n\n"
                "Puedo orientarte inicialmente sobre:\n\n"
                "- Iluminación eficiente\n"
                "- Alumbrado público\n"
                "- Soluciones LED\n"
                "- Energía solar\n"
                "- Estudios y proyectos técnicos\n\n"
                "Más adelante consultaré automáticamente "
                "el portafolio oficial de la empresa."
        }
    )


if cita:

    st.session_state.messages.append(
        {
            "role": "assistant",

            "content":
                "📅 **Agendamiento**\n\n"
                "Muy pronto podré consultar la disponibilidad "
                "del equipo de INTILED y ayudarte a programar "
                "una reunión o visita técnica."
        }
    )


if pqr:

    st.session_state.messages.append(
        {
            "role": "assistant",

            "content":
                "📋 **PQR / PQRS**\n\n"
                "El siguiente módulo que construiremos permitirá "
                "radicar peticiones, quejas, reclamos y "
                "sugerencias, además de consultar su estado."
        }
    )


if cotizacion:

    st.session_state.messages.append(
        {
            "role": "assistant",

            "content":
                "💰 **Solicitud de cotización**\n\n"
                "Cuéntame brevemente qué proyecto necesitas "
                "cotizar y posteriormente podré recopilar "
                "automáticamente los datos necesarios."
        }
    )


# ------------------------------------------------------------
# 9. CHAT
# ------------------------------------------------------------

st.markdown("---")

st.markdown(
    "### 💬 Habla con INTI"
)


for mensaje in st.session_state.messages:

    with st.chat_message(
        mensaje["role"]
    ):

        st.markdown(
            mensaje["content"]
        )


# ------------------------------------------------------------
# 10. ENTRADA DEL USUARIO
# ------------------------------------------------------------

pregunta = st.chat_input(
    "Escribe tu pregunta..."
)


if pregunta:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": pregunta
        }
    )

    with st.chat_message("user"):

        st.markdown(
            pregunta
        )


    with st.chat_message("assistant"):

        with st.spinner(
            "INTI está pensando..."
        ):

            respuesta = respuesta_temporal(
                pregunta
            )

            st.markdown(
                respuesta
            )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": respuesta
        }
    )


# ------------------------------------------------------------
# 11. INFORMACIÓN INSTITUCIONAL
# ------------------------------------------------------------

st.markdown("---")


with st.expander(
    "🏢 Acerca de INTILED"
):

    st.markdown(
        """
        **INTILED**

        INTI está siendo desarrollado como el asistente
        virtual institucional para facilitar la comunicación
        entre clientes, ciudadanos y la empresa.

        ### Próximas capacidades

        🤖 Inteligencia artificial

        🌐 Consulta de información institucional

        💡 Información de servicios y proyectos

        📅 Agendamiento de citas

        📋 PQR / PQRS

        💰 Solicitudes de cotización

        👨‍💼 Contacto con asesores

        📊 Seguimiento de solicitudes
        """
    )


# ------------------------------------------------------------
# 12. PIE DE PÁGINA
# ------------------------------------------------------------

año = datetime.now().year


st.markdown(
    f"""
    <div class="inti-footer">

    <b>INTI</b> · Asistente Virtual INTILED

    <br>

    © {año} INTILED · Todos los derechos reservados

    <br><br>

    INTI puede cometer errores.
    La información técnica o comercial relevante
    deberá ser validada por personal autorizado.

    </div>
    """,
    unsafe_allow_html=True
)
