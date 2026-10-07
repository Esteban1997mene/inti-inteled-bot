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
# CSS
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   TIPOGRAFÍA GENERAL
========================================================= */

html,
body,
[class*="css"] {{
    font-size: 17px;
}}

p {{
    font-size: 17px;
    line-height: 1.65;
}}

li {{
    font-size: 17px;
    line-height: 1.6;
}}

.stMarkdown {{
    font-size: 17px;
}}


/* =========================================================
   APLICACIÓN
========================================================= */

.stApp {{
    background:
        radial-gradient(
            circle at 88% 0%,
            rgba(245, 102, 0, 0.10),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #FFFFFF 0%,
            #F7F8FA 25%,
            #F5F6F8 100%
        );
}}


.block-container {{
    max-width: 1500px;

    padding-top: 1.5rem;
    padding-bottom: 2rem;

    padding-left: 2rem;
    padding-right: 2rem;
}}


/* Ocultar elementos de Streamlit */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}


/* =========================================================
   TÍTULOS
========================================================= */

h1 {{
    color: {OSCURO};

    font-weight: 800;

    letter-spacing: -0.5px;
}}

h2 {{
    color: {OSCURO};

    font-weight: 750;
}}

h3 {{
    color: {OSCURO};

    font-weight: 700;
}}


/* =========================================================
   SIDEBAR
========================================================= */

[data-testid="stSidebar"] {{

    background:
        radial-gradient(
            circle at 50% 88%,
            rgba(245,102,0,0.35),
            transparent 32%
        ),
        linear-gradient(
            180deg,
            #111820 0%,
            #18222D 65%,
            #111820 100%
        );

    border-right:
        1px solid rgba(255,255,255,0.05);
}}


[data-testid="stSidebar"] * {{
    color: white;
}}


[data-testid="stSidebar"] .block-container {{
    padding-top: 1.4rem;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
}}


[data-testid="stSidebar"] p {{
    font-size: 16px;
}}


[data-testid="stSidebar"] hr {{

    border: none;

    border-top:
        1px solid rgba(255,255,255,0.12);
}}


/* =========================================================
   BOTONES SIDEBAR
========================================================= */

[data-testid="stSidebar"]
.stButton > button {{

    background: transparent;

    color: white;

    border:
        1px solid transparent;

    border-radius: 13px;

    min-height: 52px;

    font-size: 16px;

    font-weight: 600;

    text-align: left;

    transition:
        all 0.20s ease;
}}


[data-testid="stSidebar"]
.stButton > button:hover {{

    background:
        linear-gradient(
            90deg,
            {NARANJA},
            #FF7A00
        );

    border-color:
        {NARANJA};

    color: white;

    transform:
        translateX(3px);

    box-shadow:
        0 8px 22px
        rgba(245,102,0,0.22);
}}


/* =========================================================
   BOTONES GENERALES
========================================================= */

.stButton > button {{

    width: 100%;

    min-height: 58px;

    border-radius: 15px;

    border:
        1px solid {BORDE};

    background: white;

    color: {TEXTO};

    font-size: 16px;

    font-weight: 650;

    transition:
        all 0.20s ease;

    box-shadow:
        0 5px 18px
        rgba(16,24,40,0.045);
}}


.stButton > button:hover {{

    border-color:
        {NARANJA};

    color:
        {NARANJA};

    transform:
        translateY(-2px);

    box-shadow:
        0 10px 25px
        rgba(16,24,40,0.09);
}}


/* =========================================================
   CHAT
========================================================= */

[data-testid="stChatMessage"] {{

    background:
        rgba(255,255,255,0.96);

    border:
        1px solid {BORDE};

    border-radius:
        18px;

    padding:
        18px 20px;

    margin-bottom:
        14px;

    box-shadow:
        0 5px 20px
        rgba(16,24,40,0.04);
}}


[data-testid="stChatMessage"] p {{

    font-size:
        17px;

    line-height:
        1.68;
}}


/* =========================================================
   FORMULARIO DE MENSAJE
========================================================= */

[data-testid="stForm"] {{

    background:
        white;

    border:
        1px solid {BORDE};

    border-radius:
        19px;

    padding:
        14px;

    box-shadow:
        0 10px 30px
        rgba(16,24,40,0.07);
}}


.stTextInput input {{

    min-height:
        52px;

    border-radius:
        14px;

    border:
        1px solid #E1E5EA;

    background:
        #FAFBFC;

    font-size:
        17px;
}}


.stTextInput input:focus {{

    border-color:
        {NARANJA};

    box-shadow:
        0 0 0 3px
        rgba(245,102,0,0.10);
}}


/* Botón de enviar dentro del formulario */

[data-testid="stFormSubmitButton"]
button {{

    background:
        linear-gradient(
            135deg,
            {NARANJA},
            #FF7A00
        );

    color:
        white;

    border:
        none;

    font-size:
        22px;

    min-height:
        52px;

    box-shadow:
        0 7px 18px
        rgba(245,102,0,0.22);
}}


[data-testid="stFormSubmitButton"]
button:hover {{

    color:
        white;

    border:
        none;

    background:
        {NARANJA_OSCURO};

    transform:
        translateY(-1px);
}}


/* =========================================================
   EXPANDER
========================================================= */

[data-testid="stExpander"] {{

    background:
        white;

    border:
        1px solid {BORDE};

    border-radius:
        15px;

    overflow:
        hidden;
}}


/* =========================================================
   ALERTAS
========================================================= */

[data-testid="stAlert"] {{

    border-radius:
        14px;

    font-size:
        16px;
}}


/* =========================================================
   DIVISORES
========================================================= */

hr {{

    border:
        none;

    border-top:
        1px solid #E4E7EB;

    margin-top:
        1.3rem;

    margin-bottom:
        1.3rem;
}}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {{

    html,
    body,
    [class*="css"] {{
        font-size: 16px;
    }}


    .block-container {{

        padding-left:
            1rem;

        padding-right:
            1rem;

        padding-top:
            1rem;
    }}


    [data-testid="stChatMessage"] p {{

        font-size:
            16px;
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
        "# INTI"
    )

    st.markdown(
        "### Asistente Virtual de INTILED"
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

    [3.25, 1],

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
# PANEL DERECHO
# ============================================================

with info_col:


    # --------------------------------------------------------
    # SOBRE INTI
    # --------------------------------------------------------

    st.markdown(
        "### Sobre INTI"
    )


    if avatar_existe:

        st.image(
            INTI_AVATAR_PATH,
            width=125
        )


    st.write(
        "Soy **INTI**, el asistente virtual "
        "de **INTILED**."
    )


    st.caption(
        "Puedo orientarte sobre nuestros servicios, "
        "proyectos y soluciones energéticas."
    )


    st.divider()


    # --------------------------------------------------------
    # CONTACTO
    # --------------------------------------------------------

    st.markdown(
        "### 📍 Información de contacto"
    )


    st.write(
        "**INTILED S.A.S. BIC**"
    )


    st.write(
        "📍 Calle 11 #36-46, La Castellana"
    )


    st.caption(
        "Pasto, Nariño, Colombia"
    )


    st.write(
        "📞 **+57 602 733 7893**"
    )


    st.write(
        "📱 **+57 304 670 2584**"
    )


    st.write(
        "✉️ **comercial@intiled.com.co**"
    )


    st.divider()


    # --------------------------------------------------------
    # HORARIOS
    # --------------------------------------------------------

    st.markdown(
        "### 🕐 Horario de atención"
    )


    st.write(
        "**Lunes a viernes**"
    )

    st.caption(
        "8:00 a. m. – 6:00 p. m."
    )


    st.write(
        "**Sábados**"
    )

    st.caption(
        "8:00 a. m. – 12:00 p. m."
    )


    st.divider()


    # --------------------------------------------------------
    # SOLUCIONES
    # --------------------------------------------------------

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
