import streamlit as st
from datetime import datetime

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
# COLORES CORPORATIVOS
# ============================================================

NARANJA = "#F56600"
NARANJA_CLARO = "#FFF1E7"
NARANJA_SUAVE = "#FFF7F2"

OSCURO = "#111820"
OSCURO_2 = "#1B2530"

TEXTO = "#17202A"
GRIS = "#667085"
BORDE = "#E7E9ED"
FONDO = "#F6F7F9"
BLANCO = "#FFFFFF"


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   GENERAL
========================================================= */

.stApp {{
    background:
        radial-gradient(
            circle at 85% 0%,
            rgba(245,102,0,0.08),
            transparent 28%
        ),
        #F6F7F9;
}}

.block-container {{
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}


/* =========================================================
   SIDEBAR
========================================================= */

[data-testid="stSidebar"] {{
    background:
        radial-gradient(
            circle at 50% 85%,
            rgba(245,102,0,0.24),
            transparent 35%
        ),
        linear-gradient(
            180deg,
            {OSCURO} 0%,
            {OSCURO_2} 100%
        );

    border-right: 1px solid rgba(255,255,255,0.05);
}}

[data-testid="stSidebar"] * {{
    color: white;
}}

[data-testid="stSidebar"] .block-container {{
    padding-top: 1.5rem;
}}

[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.10);
}}


/* Botones sidebar */

[data-testid="stSidebar"] .stButton > button {{
    background: transparent;
    color: white;
    border: 1px solid transparent;
    border-radius: 12px;

    min-height: 48px;

    text-align: left;

    font-weight: 500;

    transition: all 0.2s ease;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(245,102,0,0.15);
    border-color: rgba(245,102,0,0.30);
    color: white;

    transform: translateX(3px);
}}


/* =========================================================
   BOTONES GENERALES
========================================================= */

.stButton > button {{
    width: 100%;

    border-radius: 14px;

    border: 1px solid {BORDE};

    background: white;

    min-height: 52px;

    font-weight: 600;

    color: {TEXTO};

    transition: all 0.20s ease;

    box-shadow:
        0 4px 14px
        rgba(16,24,40,0.04);
}}

.stButton > button:hover {{
    border-color: {NARANJA};

    color: {NARANJA};

    transform: translateY(-2px);

    box-shadow:
        0 8px 24px
        rgba(16,24,40,0.08);
}}


/* =========================================================
   CHAT
========================================================= */

[data-testid="stChatMessage"] {{
    background: white;

    border:
        1px solid {BORDE};

    border-radius: 18px;

    padding: 16px 18px;

    margin-bottom: 12px;

    box-shadow:
        0 4px 18px
        rgba(16,24,40,0.035);
}}


/* =========================================================
   FORMULARIO MENSAJE
========================================================= */

[data-testid="stForm"] {{
    background: white;

    border:
        1px solid {BORDE};

    border-radius: 18px;

    padding: 12px 14px;

    box-shadow:
        0 8px 25px
        rgba(16,24,40,0.06);
}}

.stTextInput input {{
    border-radius: 14px;

    min-height: 48px;

    border:
        1px solid #E3E6EA;

    background:
        #FAFBFC;
}}

.stTextInput input:focus {{
    border-color: {NARANJA};

    box-shadow:
        0 0 0 2px
        rgba(245,102,0,0.10);
}}


/* =========================================================
   EXPANDER
========================================================= */

[data-testid="stExpander"] {{
    background: white;

    border:
        1px solid {BORDE};

    border-radius: 14px;

    overflow: hidden;
}}


/* =========================================================
   MÉTRICAS / ESTADO
========================================================= */

[data-testid="stMetric"] {{
    background: white;

    padding: 12px;

    border-radius: 14px;

    border:
        1px solid {BORDE};
}}


/* =========================================================
   DIVISORES
========================================================= */

hr {{
    border: none;

    border-top:
        1px solid #E7E9ED;

    margin-top: 1.2rem;

    margin-bottom: 1.2rem;
}}


/* =========================================================
   LINKS
========================================================= */

a {{
    color: {NARANJA};
}}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {{

    .block-container {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}

}}

</style>
""",
    unsafe_allow_html=True
)


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
# ESTADO DE SESIÓN
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",

            "content":
                "¡Hola! 👋 Soy **INTI**, el asistente virtual "
                "de **INTILED**.\n\n"
                "Estoy aquí para orientarte sobre nuestros "
                "servicios, proyectos y soluciones energéticas.\n\n"
                "**¿En qué puedo ayudarte hoy?**"
        }

    ]


# ============================================================
# FUNCIÓN PRINCIPAL DEL CHAT
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

    st.markdown(
        "# 🟠 INTILED"
    )

    st.caption(
        "Soluciones que iluminan el futuro"
    )

    st.divider()


    if st.button(
        "💬   Chat con INTI",
        use_container_width=True
    ):

        pass


    if st.button(
        "💡   Servicios",
        use_container_width=True
    ):

        procesar_mensaje(
            "Quiero conocer los servicios que ofrece INTILED."
        )

        st.rerun()


    if st.button(
        "📄   Cotización",
        use_container_width=True
    ):

        procesar_mensaje(
            "Quiero solicitar una cotización para un proyecto."
        )

        st.rerun()


    if st.button(
        "📅   Agendar cita",
        use_container_width=True
    ):

        procesar_mensaje(
            "Quiero solicitar una reunión o visita técnica."
        )

        st.rerun()


    if st.button(
        "🎧   PQR / PQRS",
        use_container_width=True
    ):

        procesar_mensaje(
            "Necesito orientación para presentar una PQR o PQRS."
        )

        st.rerun()


    if st.button(
        "ⓘ   Acerca de INTILED",
        use_container_width=True
    ):

        procesar_mensaje(
            "Cuéntame sobre INTILED."
        )

        st.rerun()


    st.divider()


    st.markdown(
        "### 👷🏻‍♂️ INTI"
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
        "🌱 **Comprometidos con un futuro más sostenible.**"
    )


# ============================================================
# ENCABEZADO
# ============================================================

header_logo, header_texto, header_estado = st.columns(
    [1, 5, 1.5],
    vertical_alignment="center"
)


with header_logo:

    st.markdown(
        "# 🟠"
    )


with header_texto:

    st.markdown(
        "# INTI"
    )

    st.markdown(
        "**Asistente Virtual de INTILED**"
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

c1, c2, c3, c4 = st.columns(4)


with c1:

    servicios = st.button(
        "💡  Servicios\n\nConoce nuestras soluciones",
        use_container_width=True,
        key="servicios_superior"
    )


with c2:

    cotizacion = st.button(
        "📄  Cotización\n\nSolicita una propuesta",
        use_container_width=True,
        key="cotizacion_superior"
    )


with c3:

    cita = st.button(
        "📅  Agendar cita\n\nReúnete con nuestro equipo",
        use_container_width=True,
        key="cita_superior"
    )


with c4:

    pqr = st.button(
        "🎧  PQR / PQRS\n\nPeticiones, quejas o reclamos",
        use_container_width=True,
        key="pqr_superior"
    )


# ============================================================
# ACCIONES RÁPIDAS
# ============================================================

if servicios:

    procesar_mensaje(
        "Quiero conocer los servicios y soluciones "
        "que ofrece INTILED."
    )

    st.rerun()


if cotizacion:

    procesar_mensaje(
        "Quiero solicitar una cotización para un proyecto."
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
    [3.2, 1],
    gap="large"
)


# ============================================================
# CHAT CENTRAL
# ============================================================

with chat_col:

    st.markdown(
        "### 💬 Conversa con INTI"
    )

    st.caption(
        "Pregúntame sobre nuestros servicios, "
        "soluciones energéticas o proyectos."
    )


    # --------------------------------------------------------
    # MENSAJES
    # --------------------------------------------------------

    for mensaje in st.session_state.messages:

        if mensaje["role"] == "assistant":

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
    # FORMULARIO DE MENSAJE
    # --------------------------------------------------------

    st.write("")

    with st.form(
        "formulario_inti",
        clear_on_submit=True
    ):

        texto_col, boton_col = st.columns(
            [7, 1],
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
            pregunta.strip()
        )

        st.rerun()


    # --------------------------------------------------------
    # NUEVA CONVERSACIÓN
    # --------------------------------------------------------

    vacio, limpiar = st.columns(
        [5, 2]
    )


    with limpiar:

        if st.button(
            "🗑️ Nueva conversación",
            use_container_width=True
        ):

            st.session_state.messages = [

                {
                    "role": "assistant",

                    "content":
                        "¡Hola! 👋 Soy **INTI**, "
                        "el asistente virtual de **INTILED**.\n\n"
                        "Estoy listo para ayudarte.\n\n"
                        "**¿Qué necesitas hoy?**"
                }

            ]

            st.rerun()


# ============================================================
# PANEL DERECHO
# ============================================================

with info_col:

    st.markdown(
        "### 👷🏻‍♂️ Sobre INTI"
    )

    st.write(
        "Soy **INTI**, el asistente virtual de "
        "**INTILED**."
    )

    st.caption(
        "Puedo orientarte sobre nuestros servicios, "
        "proyectos y soluciones energéticas."
    )


    st.divider()


    st.markdown(
        "### 📍 Contacto"
    )

    st.write(
        "**INTILED S.A.S. BIC**"
    )

    st.caption(
        "Calle 11 #36-46\n\n"
        "La Castellana\n\n"
        "Pasto, Nariño"
    )


    st.markdown(
        "📞 **+57 602 733 7893**"
    )

    st.markdown(
        "📱 **+57 304 670 2584**"
    )

    st.markdown(
        "✉️ **comercial@intiled.com.co**"
    )


    st.divider()


    st.markdown(
        "### 🕐 Horario"
    )

    st.caption(
        "Lunes a viernes\n\n"
        "8:00 a. m. – 6:00 p. m.\n\n"
        "Sábados\n\n"
        "8:00 a. m. – 12:00 p. m."
    )


    st.divider()


    st.markdown(
        "### ☀️ Soluciones que iluminan el futuro"
    )

    st.caption(
        "Eficiencia energética, energía solar, "
        "infraestructura eléctrica y sostenibilidad."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


f1, f2, f3, f4, f5 = st.columns(5)


with f1:
    st.caption("🍃 Eficiencia energética")

with f2:
    st.caption("☀️ Energía solar")

with f3:
    st.caption("⚙️ Infraestructura eléctrica")

with f4:
    st.caption("👥 Acompañamiento técnico")

with f5:
    st.caption("🌱 Sostenibilidad")


st.write("")

año = datetime.now().year

st.caption(
    f"© {año} INTILED S.A.S. BIC · "
    "INTI — Asistente Virtual Inteligente"
)
