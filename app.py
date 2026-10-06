import streamlit as st
import requests
from streamlit_lottie import st_lottie
from datetime import datetime

# Importamos el cerebro de INTI
from modules.inti_ai import responder_inti


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="INTI | Asistente Virtual INTILED",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. ESTILOS
# ============================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background: linear-gradient(
        135deg,
        #f5f7fa 0%,
        #eef2f7 100%
    );
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.inti-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.inti-subtitle {
    font-size: 18px;
    color: #5f6368;
    margin-top: 0;
}

.status-online {
    display: inline-block;
    background-color: #e8f5e9;
    color: #198754;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

.service-card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    min-height: 145px;
    border: 1px solid #eeeeee;

    transition:
        transform .2s ease,
        box-shadow .2s ease;
}

.service-card:hover {

    transform: translateY(-4px);

    box-shadow:
        0 8px 22px rgba(0,0,0,.08);
}

.stButton > button {

    width: 100%;

    border-radius: 12px;

    font-weight: 600;

    min-height: 45px;
}

[data-testid="stChatMessage"] {

    background:
        rgba(255,255,255,.75);

    border-radius: 16px;

    padding: 12px;

    margin-bottom: 10px;

    border:
        1px solid rgba(0,0,0,.04);
}

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

.inti-footer {

    text-align: center;

    color: #888;

    font-size: 13px;

    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. ANIMACIÓN DE INTI
# ============================================================

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

        pass

    return None


LOTTIE_INTI = (
    "https://assets10.lottiefiles.com/"
    "packages/lf20_mbe35mca.json"
)

animacion_inti = cargar_lottie(
    LOTTIE_INTI
)


# ============================================================
# 4. HISTORIAL DEL CHAT
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [

        {

            "role": "assistant",

            "content": (
                "¡Hola! 👋 Soy **INTI**, el asistente virtual "
                "de **INTILED**.\n\n"

                "Puedo orientarte sobre nuestros servicios, "
                "proyectos, energía, iluminación y atención "
                "al cliente.\n\n"

                "**¿Cómo puedo ayudarte hoy?**"
            )

        }

    ]


# ============================================================
# 5. FUNCIÓN PARA MENSAJES DE BOTONES
# ============================================================

def agregar_mensaje_rapido(texto):

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": texto

        }

    )


# ============================================================
# 6. ENCABEZADO
# ============================================================

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


# ============================================================
# 7. ACCIONES RÁPIDAS
# ============================================================

st.markdown(
    "### ¿Cómo puedo ayudarte?"
)


col1, col2, col3, col4 = st.columns(4)


# ------------------------------------------------------------
# SERVICIOS
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# CITAS
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# PQR
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# COTIZACIÓN
# ------------------------------------------------------------

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


# ============================================================
# 8. ACCIONES DE LOS BOTONES
# ============================================================

if servicios:

    agregar_mensaje_rapido(

        "💡 Puedo orientarte sobre las soluciones y servicios "
        "de **INTILED**. Pregúntame qué necesitas y te ayudaré "
        "a identificar la opción adecuada."

    )


if cita:

    agregar_mensaje_rapido(

        "📅 Puedo orientarte para solicitar una "
        "**reunión o visita técnica**.\n\n"
        "El módulo de registro automático de citas será "
        "nuestra próxima integración."

    )


if pqr:

    agregar_mensaje_rapido(

        "📋 Puedo orientarte sobre **PQR/PQRS**.\n\n"
        "Próximamente podrás radicar y consultar solicitudes "
        "directamente desde INTI."

    )


if cotizacion:

    agregar_mensaje_rapido(

        "💰 Claro. Cuéntame brevemente **qué necesitas cotizar** "
        "y te ayudaré a precisar la información inicial "
        "del proyecto."

    )


# ============================================================
# 9. CHAT
# ============================================================

st.markdown("---")

st.markdown(
    "### 💬 Habla con INTI"
)


# Mostrar conversación

for mensaje in st.session_state.messages:

    with st.chat_message(
        mensaje["role"]
    ):

        st.markdown(
            mensaje["content"]
        )


# ============================================================
# 10. ENTRADA DEL USUARIO
# ============================================================

pregunta = st.chat_input(

    "Escribe tu pregunta para INTI..."

)


if pregunta:

    # Guardamos el historial antes de añadir
    # la nueva pregunta

    historial_anterior = list(
        st.session_state.messages
    )


    # Guardamos pregunta

    st.session_state.messages.append(

        {

            "role": "user",

            "content": pregunta

        }

    )


    # Mostrar pregunta

    with st.chat_message("user"):

        st.markdown(
            pregunta
        )


    # ========================================================
    # CONEXIÓN CON GEMINI
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "INTI está pensando..."
        ):

            try:

                # Leer API KEY desde Streamlit Secrets

                api_key = st.secrets.get(

                    "GEMINI_API_KEY",

                    ""

                )


                # Consultar cerebro de INTI

                respuesta = responder_inti(

                    pregunta=pregunta,

                    historial=historial_anterior,

                    api_key=api_key

                )


            except Exception:

                respuesta = (

                    "⚠️ INTI tuvo un inconveniente al "
                    "procesar tu consulta.\n\n"

                    "Verifica la configuración de Gemini "
                    "e intenta nuevamente."

                )


            st.markdown(
                respuesta
            )


    # Guardar respuesta

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": respuesta

        }

    )


# ============================================================
# 11. INFORMACIÓN INSTITUCIONAL
# ============================================================

st.markdown("---")


with st.expander(
    "🏢 Acerca de INTILED"
):

    st.markdown(

        """

        **INTI** es el asistente virtual institucional
        de **INTILED**.

        El proyecto se está desarrollando progresivamente
        para integrar:

        - 🤖 Atención mediante inteligencia artificial
        - 🌐 Información institucional y página web
        - 💡 Servicios y proyectos
        - 📅 Agendamiento de citas
        - 📋 PQR / PQRS
        - 💰 Solicitudes de cotización
        - 👨‍💼 Contacto con asesores
        - 📊 Seguimiento de solicitudes

        """

    )


# ============================================================
# 12. PIE DE PÁGINA
# ============================================================

año = datetime.now().year


st.markdown(

    f"""

    <div class="inti-footer">

        <b>INTI</b>
        · Asistente Virtual INTILED

        <br>

        © {año} INTILED
        · Todos los derechos reservados

        <br><br>

        INTI puede cometer errores.
        La información técnica o comercial relevante
        debe ser validada por personal autorizado
        de INTILED.

    </div>

    """,

    unsafe_allow_html=True

)
