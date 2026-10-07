import streamlit as st
from datetime import datetime
from pathlib import Path

from modules.inti_ai import responder_inti


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="INTI | Asistente Virtual INTILED",
    page_icon="🟠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# RUTAS
# ============================================================

LOGO_PATH = "assets/logo_intiled.png"
INTI_AVATAR_PATH = "assets/inti_avatar.png"


# ============================================================
# COLORES CORPORATIVOS
# ============================================================

NARANJA = "#F56600"
NARANJA_OSCURO = "#D94F00"
NARANJA_CLARO = "#FFF1E7"

OSCURO = "#111820"
OSCURO_2 = "#1B2530"

TEXTO = "#17202A"
GRIS = "#667085"

BORDE = "#E5E7EB"
FONDO = "#F6F7F9"
BLANCO = "#FFFFFF"


# ============================================================
# CSS REFORZADO (!important PARA FORZAR ESTILOS EN STREAMLIT)
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   TIPOGRAFÍA GENERAL
========================================================= */

html, body, [class*="css"] {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    font-size: 16px !important;
    color: {TEXTO} !important;
}}

p, li, .stMarkdown {{
    font-size: 16px !important;
    line-height: 1.6 !important;
}}

.block-container {{
    max-width: 1400px !important;
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}

/* Ocultar elementos predeterminados de Streamlit */
#MainMenu, footer, header {{
    visibility: hidden !important;
}}


/* =========================================================
   TÍTULOS
========================================================= */

h1 {{
    color: {OSCURO} !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}}

h2 {{
    color: {OSCURO} !important;
    font-weight: 750 !important;
}}

h3 {{
    color: {OSCURO} !important;
    font-weight: 700 !important;
}}


/* =========================================================
   SIDEBAR ELEGANTE
========================================================= */

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}}

[data-testid="stSidebar"] * {{
    color: #F8FAFC !important;
}}

[data-testid="stSidebar"] .block-container {{
    padding-top: 1.5rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
}}

[data-testid="stSidebar"] p {{
    font-size: 15px !important;
}}

[data-testid="stSidebar"] hr {{
    border: none !important;
    border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255, 255, 255, 0.05) !important;
    color: #E2E8F0 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    text-align: left !important;
    transition: all 0.25s ease !important;
    margin-bottom: 4px !important;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: {NARANJA} !important;
    border-color: {NARANJA} !important;
    color: #FFFFFF !important;
    transform: translateX(4px) !important;
    box-shadow: 0 4px 14px rgba(245, 102, 0, 0.35) !important;
}}


/* =========================================================
   BOTONES GENERALES / ACCESOS RÁPIDOS
========================================================= */

.stButton > button {{
    width: 100% !important;
    min-height: 64px !important;
    border-radius: 14px !important;
    border: 1px solid {BORDE} !important;
    background: #FFFFFF !important;
    color: {TEXTO} !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03) !important;
}}

.stButton > button:hover {{
    border-color: {NARANJA} !important;
    color: {NARANJA} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(245, 102, 0, 0.15) !important;
}}


/* =========================================================
   DIFERENCIACIÓN VISUAL EN LAS BURBUJAS DE CHAT
========================================================= */

[data-testid="stChatMessage"] {{
    border-radius: 16px !important;
    padding: 16px 20px !important;
    margin-bottom: 12px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
}}

/* Chat del Asistente (Fondo Naranja Suave) */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
    background-color: #FFF6F0 !important;
    border-color: #FFD2B8 !important;
}}

/* Chat del Usuario (Fondo Azul Grisáceo) */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background-color: #F0F5FA !important;
    border-color: #CBD5E1 !important;
}}


/* =========================================================
   INPUT Y FORMULARIO DE MENSAJE
========================================================= */

[data-testid="stForm"] {{
    background: #FFFFFF !important;
    border: 1px solid {BORDE} !important;
    border-radius: 18px !important;
    padding: 10px 12px !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05) !important;
}}

.stTextInput input {{
    min-height: 48px !important;
    border-radius: 12px !important;
    border: 1px solid #E2E8F0 !important;
    background: #F8FAFC !important;
    font-size: 16px !important;
}}

.stTextInput input:focus {{
    border-color: {NARANJA} !important;
    box-shadow: 0 0 0 3px rgba(245, 102, 0, 0.15) !important;
}}

[data-testid="stFormSubmitButton"] button {{
    background: linear-gradient(135deg, {NARANJA}, #FF7A00) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-size: 20px !important;
    min-height: 48px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(245, 102, 0, 0.3) !important;
}}

[data-testid="stFormSubmitButton"] button:hover {{
    background: {NARANJA_OSCURO} !important;
    transform: translateY(-1px) !important;
}}


/* =========================================================
   TARJETAS DEL PANEL DERECHO
========================================================= */

.info-card-box {{
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
}}

.contact-link-item {{
    color: #1D70B8 !important;
    text-decoration: none !important;
    font-weight: 600 !important;
}}

.contact-link-item:hover {{
    text-decoration: underline !important;
}}

/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {{
    html, body, [class*="css"] {{
        font-size: 15px !important;
    }}

    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }}

    [data-testid="stChatMessage"] p {{
        font-size: 15px !important;
    }}
}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# VERIFICACIÓN DE ARCHIVOS
# ============================================================

logo_existe = Path(
    LOGO_PATH
).exists()

avatar_existe = Path(
    INTI_AVATAR_PATH
).exists()


# ============================================================
# API KEY
# ============================================================

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    ""
)


if not api_key:

    st.error(
        "No se encontró GEMINI_API_KEY "
        "en Streamlit Secrets."
    )

    st.stop()


# ============================================================
# MENSAJE INICIAL
# ============================================================

MENSAJE_INICIAL = {

    "role": "assistant",

    "content":
        "¡Hola! 👋 Soy **INTI**, el asistente virtual "
        "de **INTILED**.\n\n"
        "Estoy aquí para orientarte sobre nuestros servicios, "
        "proyectos y soluciones energéticas.\n\n"
        "**¿En qué puedo ayudarte hoy?**"
}


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        MENSAJE_INICIAL.copy()
    ]


# ============================================================
# PROCESAR MENSAJE
# ============================================================

def procesar_mensaje(pregunta):

    if not pregunta:
        return

    pregunta = pregunta.strip()

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

    except Exception:

        respuesta = (
            "⚠️ En este momento tuve un inconveniente "
            "al procesar tu consulta. "
            "Por favor intenta nuevamente."
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": respuesta
        }
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    if logo_existe:

        st.image(
            LOGO_PATH,
            use_container_width=True
        )

    else:

        st.markdown(
            "# 🟠 INTILED"
        )

    st.caption(
        "Soluciones que iluminan el futuro"
    )

    st.divider()

    # --------------------------------------------------------
    # NAVEGACIÓN
    # --------------------------------------------------------

    st.markdown("#### 📌 Navegación")

    if st.button(
        "💬   Chat con INTI",
        use_container_width=True,
        key="sidebar_chat"
    ):

        pass

    if st.button(
        "💡   Servicios",
        use_container_width=True,
        key="sidebar_servicios"
    ):

        procesar_mensaje(
            "Quiero conocer los servicios "
            "que ofrece INTILED."
        )

        st.rerun()

    if st.button(
        "📄   Cotización",
        use_container_width=True,
        key="sidebar_cotizacion"
    ):

        procesar_mensaje(
            "Quiero solicitar una cotización "
            "para un proyecto."
        )

        st.rerun()

    if st.button(
        "📅   Agendar cita",
        use_container_width=True,
        key="sidebar_cita"
    ):

        procesar_mensaje(
            "Quiero solicitar una reunión "
            "o visita técnica."
        )

        st.rerun()

    if st.button(
        "🎧   PQR / PQRS",
        use_container_width=True,
        key="sidebar_pqr"
    ):

        procesar_mensaje(
            "Necesito orientación para presentar "
            "una PQR o PQRS."
        )

        st.rerun()

    if st.button(
        "ⓘ   Acerca de INTILED",
        use_container_width=True,
        key="sidebar_acerca"
    ):

        procesar_mensaje(
            "Cuéntame sobre INTILED, "
            "su enfoque y sus servicios."
        )

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # PERSONAJE INTI
    # --------------------------------------------------------

    if avatar_existe:

        st.image(
            INTI_AVATAR_PATH,
            use_container_width=True
        )

    st.markdown(
        "## INTI"
    )

    st.write(
        "**Tu aliado en soluciones energéticas.**"
    )

    st.caption(
        "Eficiencia energética · Energía solar · "
        "Infraestructura eléctrica"
    )

    st.divider()

    st.markdown(
        "🌱 **Comprometidos con un futuro "
        "más sostenible.**"
    )


# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================

header_avatar, header_texto, header_estado = st.columns(

    [1, 5, 1.5],

    vertical_alignment="center"

)


with header_avatar:

    if avatar_existe:

        st.image(
            INTI_AVATAR_PATH,
            width=115
        )

    else:

        st.markdown(
            "# 👷🏻‍♂️"
        )


with header_texto:

    st.markdown(
        "<h1 style='margin-bottom: 0px;'>INTI</h1>", 
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='margin-top: 0px; color: #475569;'>Asistente Virtual de INTILED</h3>", 
        unsafe_allow_html=True
    )

    st.caption(
        "Energía, eficiencia y sostenibilidad "
        "para un mejor mañana."
    )


with header_estado:

    st.success(
        "● En línea"
    )

    st.caption(
        "Listo para ayudarte"
    )


st.divider()


# ============================================================
# ACCESOS RÁPIDOS
# ============================================================

st.markdown(
    "### ¿Cómo puedo ayudarte?"
)

st.caption(
    "Selecciona una opción o conversa directamente con INTI."
)


c1, c2, c3, c4 = st.columns(
    4,
    gap="medium"
)


with c1:

    servicios = st.button(

        "💡 Servicios\n\n"
        "Conoce nuestras soluciones",

        use_container_width=True,

        key="servicios_superior"
    )


with c2:

    cotizacion = st.button(

        "📄 Cotización\n\n"
        "Solicita una propuesta",

        use_container_width=True,

        key="cotizacion_superior"
    )


with c3:

    cita = st.button(

        "📅 Agendar cita\n\n"
        "Reúnete con nuestro equipo",

        use_container_width=True,

        key="cita_superior"
    )


with c4:

    pqr = st.button(

        "🎧 PQR / PQRS\n\n"
        "Peticiones, quejas o reclamos",

        use_container_width=True,

        key="pqr_superior"
    )


# ============================================================
# ACCIONES RÁPIDAS
# ============================================================

if servicios:

    procesar_mensaje(
        "Quiero conocer los servicios "
        "y soluciones que ofrece INTILED."
    )

    st.rerun()


if cotizacion:

    procesar_mensaje(
        "Quiero solicitar una cotización "
        "para un proyecto."
    )

    st.rerun()


if cita:

    procesar_mensaje(
        "Quiero agendar una reunión o visita técnica "
        "con el equipo de INTILED."
    )

    st.rerun()


if pqr:

    procesar_mensaje(
        "Necesito orientación para presentar "
        "una PQR o PQRS."
    )

    st.rerun()


st.write("")


# ============================================================
# CUERPO PRINCIPAL
# ============================================================

chat_col, info_col = st.columns(

    [3.25, 1.1],

    gap="large"

)


# ============================================================
# CHAT
# ============================================================

with chat_col:

    st.markdown(
        "## 💬 Conversa con INTI"
    )

    st.caption(
        "Pregúntame sobre nuestros servicios, "
        "soluciones energéticas o proyectos."
    )

    st.write("")

    # --------------------------------------------------------
    # MOSTRAR CONVERSACIÓN
    # --------------------------------------------------------

    for mensaje in st.session_state.messages:

        if mensaje["role"] == "assistant":

            if avatar_existe:

                avatar = INTI_AVATAR_PATH

            else:

                avatar = "👷🏻‍♂️"

        else:

            avatar = "👤"

        with st.chat_message(

            mensaje["role"],

            avatar=avatar

        ):

            st.markdown(
                mensaje["content"]
            )

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    st.write("")

    with st.form(

        "formulario_inti",

        clear_on_submit=True

    ):

        texto_col, boton_col = st.columns(

            [8, 1],

            vertical_alignment="bottom"

        )

        with texto_col:

            pregunta = st.text_input(

                "Mensaje",

                placeholder=(
                    "Escribe tu mensaje para INTI..."
                ),

                label_visibility="collapsed"

            )

        with boton_col:

            enviar = st.form_submit_button(

                "➤",

                use_container_width=True

            )

    if enviar and pregunta.strip():

        procesar_mensaje(
            pregunta
        )

        st.rerun()

    # --------------------------------------------------------
    # NUEVA CONVERSACIÓN
    # --------------------------------------------------------

    espacio, limpiar = st.columns(
        [5, 2]
    )

    with limpiar:

        if st.button(

            "🗑️ Nueva conversación",

            use_container_width=True,

            key="nueva_conversacion"

        ):

            st.session_state.messages = [
                MENSAJE_INICIAL.copy()
            ]

            st.rerun()


# ============================================================
# PANEL DERECHO (ESTILIZADO EN TARJETAS BLANCAS)
# ============================================================

with info_col:

    # --------------------------------------------------------
    # SOBRE INTI
    # --------------------------------------------------------

    st.markdown("<div class='info-card-box'>", unsafe_allow_html=True)
    
    st.markdown("### Sobre INTI")

    if avatar_existe:

        st.image(
            INTI_AVATAR_PATH,
            width=105
        )

    st.write(
        "Soy **INTI**, el asistente virtual de **INTILED**."
    )

    st.caption(
        "Puedo orientarte sobre nuestros servicios, "
        "proyectos y soluciones energéticas."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # CONTACTO DIRECTO
    # --------------------------------------------------------

    st.markdown("<div class='info-card-box'>", unsafe_allow_html=True)

    st.markdown("### 📍 Contacto Directo")

    st.write("**INTILED S.A.S. BIC**")

    st.write("📍 Calle 11 #36-46, La Castellana")

    st.caption("Pasto, Nariño, Colombia")

    st.markdown("<hr style='border:none; border-top:1px solid #E2E8F0; margin:10px 0;'>", unsafe_allow_html=True)

    st.markdown("📞 <a class='contact-link-item' href='tel:+576027337893'>+57 602 733 7893</a>", unsafe_allow_html=True)

    st.markdown("📱 <a class='contact-link-item' href='https://wa.me/573046702584'>+57 304 670 2584</a>", unsafe_allow_html=True)

    st.markdown("✉️ <a class='contact-link-item' href='mailto:comercial@intiled.com.co'>comercial@intiled.com.co</a>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # HORARIOS
    # --------------------------------------------------------

    st.markdown("<div class='info-card-box'>", unsafe_allow_html=True)

    st.markdown("### 🕐 Horario de Atención")

    st.write("**Lunes a viernes:** 8:00 a. m. – 6:00 p. m.")

    st.write("**Sábados:** 8:00 a. m. – 12:00 p. m.")

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SOLUCIONES
    # --------------------------------------------------------

    st.markdown("<div class='info-card-box'>", unsafe_allow_html=True)

    st.markdown("### ☀️ Soluciones")

    st.caption("Eficiencia energética, energía solar, infraestructura eléctrica y sostenibilidad.")

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.divider()

f1, f2, f3, f4, f5 = st.columns(
    5
)

with f1:

    st.caption(
        "🍃 Eficiencia energética"
    )

with f2:

    st.caption(
        "☀️ Energía solar"
    )

with f3:

    st.caption(
        "⚙️ Infraestructura eléctrica"
    )

with f4:

    st.caption(
        "👥 Acompañamiento técnico"
    )

with f5:

    st.caption(
        "🌱 Sostenibilidad"
    )

st.write("")

año = datetime.now().year

st.caption(
    f"© {año} INTILED S.A.S. BIC · "
    "INTI — Asistente Virtual Inteligente"
)
