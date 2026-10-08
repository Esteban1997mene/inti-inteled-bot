import streamlit as st
from datetime import datetime
from pathlib import Path

from modules.inti_ai import responder_inti


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="INTI | Asistente Virtual INTILED",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# ARCHIVOS
# ============================================================

LOGO = "assets/logo_intiled.png"
AVATAR = "assets/inti_avatar.png"

logo_ok = Path(LOGO).exists()
avatar_ok = Path(AVATAR).exists()


# ============================================================
# COLORES
# ============================================================

ORANGE = "#FF6500"
ORANGE_2 = "#FF8A00"
DARK = "#090E13"
DARK_2 = "#111923"
TEXT = "#101828"
MUTED = "#667085"
BORDER = "#E7E9EE"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   GLOBAL
========================================================= */

html {{
    scroll-behavior: smooth;
}}

html,
body,
[class*="css"] {{
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 85% 0%,
            rgba(255,101,0,.12),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #FFFFFF 0%,
            #F8F9FB 52%,
            #F4F6F8 100%
        );

    color: {TEXT};
}}

.block-container {{
    max-width: 1380px;

    padding-top: 1.3rem;
    padding-bottom: 3rem;

    padding-left: 2.2rem;
    padding-right: 2.2rem;
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}


/* =========================================================
   TIPOGRAFÍA
========================================================= */

h1 {{
    font-size: 3rem !important;
    font-weight: 820 !important;
    letter-spacing: -1.7px !important;
    color: {DARK} !important;
}}

h2 {{
    font-size: 2rem !important;
    font-weight: 780 !important;
    letter-spacing: -.7px !important;
    color: {DARK} !important;
}}

h3 {{
    font-size: 1.3rem !important;
    font-weight: 720 !important;
    color: {DARK} !important;
}}

p {{
    font-size: 17px;
    line-height: 1.7;
}}


/* =========================================================
   SIDEBAR
========================================================= */

[data-testid="stSidebar"] {{

    background:
        radial-gradient(
            circle at 50% 95%,
            rgba(255,101,0,.25),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #090E13 0%,
            #111923 58%,
            #090E13 100%
        );

    border-right:
        1px solid rgba(255,255,255,.06);
}}

[data-testid="stSidebar"] * {{
    color: #FFFFFF;
}}

[data-testid="stSidebar"] p {{
    font-size: 15px;
}}

[data-testid="stSidebar"] hr {{
    border: none;

    border-top:
        1px solid rgba(255,255,255,.10);
}}

[data-testid="stSidebar"] .stButton > button {{

    background: transparent;

    border:
        1px solid transparent;

    border-radius:
        14px;

    color:
        rgba(255,255,255,.88);

    min-height:
        50px;

    font-size:
        15px;

    font-weight:
        600;

    text-align:
        left;

    transition:
        all .22s ease;
}}

[data-testid="stSidebar"] .stButton > button:hover {{

    background:
        linear-gradient(
            90deg,
            {ORANGE},
            {ORANGE_2}
        );

    color:
        #FFFFFF;

    transform:
        translateX(4px);

    box-shadow:
        0 8px 28px rgba(255,101,0,.22);
}}


/* =========================================================
   BOTONES
========================================================= */

.stButton > button {{

    border-radius:
        17px;

    border:
        1px solid {BORDER};

    background:
        rgba(255,255,255,.92);

    min-height:
        64px;

    color:
        {TEXT};

    font-size:
        16px;

    font-weight:
        650;

    transition:
        all .22s ease;

    box-shadow:
        0 7px 25px rgba(16,24,40,.05);
}}

.stButton > button:hover {{

    border-color:
        rgba(255,101,0,.65);

    color:
        {ORANGE};

    transform:
        translateY(-3px);

    box-shadow:
        0 15px 35px rgba(16,24,40,.10),
        0 4px 15px rgba(255,101,0,.08);
}}


/* =========================================================
   CHAT
========================================================= */

[data-testid="stChatMessage"] {{

    background:
        rgba(255,255,255,.94);

    border:
        1px solid rgba(226,230,235,.95);

    border-radius:
        22px;

    padding:
        18px 22px;

    margin-bottom:
        14px;

    box-shadow:
        0 7px 25px rgba(16,24,40,.045);
}}

[data-testid="stChatMessage"] p {{

    font-size:
        17px;

    line-height:
        1.72;

    color:
        {TEXT};
}}

[data-testid="stChatMessage"] strong {{
    color:
        {DARK};
}}


/* =========================================================
   FORMULARIO CHAT
========================================================= */

[data-testid="stForm"] {{

    background:
        rgba(255,255,255,.96);

    border:
        1px solid rgba(224,228,234,.95);

    border-radius:
        22px;

    padding:
        12px 14px;

    box-shadow:
        0 18px 50px rgba(16,24,40,.09),
        0 3px 12px rgba(255,101,0,.05);
}}

.stTextInput input {{

    min-height:
        58px;

    border:
        1px solid #E6E9ED !important;

    border-radius:
        16px;

    background:
        #F7F8FA;

    color:
        {TEXT};

    font-size:
        17px;

    padding-left:
        18px;
}}

.stTextInput input::placeholder {{

    color:
        #8B95A1;
}}

.stTextInput input:focus {{

    background:
        #FFFFFF;

    border-color:
        {ORANGE} !important;

    box-shadow:
        0 0 0 3px rgba(255,101,0,.10) !important;
}}


/* =========================================================
   BOTÓN ENVIAR
========================================================= */

[data-testid="stFormSubmitButton"] button {{

    min-height:
        58px;

    border-radius:
        16px;

    border:
        none;

    background:
        linear-gradient(
            135deg,
            {ORANGE},
            {ORANGE_2}
        );

    color:
        #FFFFFF;

    font-size:
        23px;

    box-shadow:
        0 9px 25px rgba(255,101,0,.27);
}}

[data-testid="stFormSubmitButton"] button:hover {{

    color:
        #FFFFFF;

    border:
        none;

    background:
        linear-gradient(
            135deg,
            #ED5D00,
            {ORANGE}
        );
}}


/* =========================================================
   STATUS
========================================================= */

[data-testid="stAlert"] {{
    border-radius:
        16px;
}}


/* =========================================================
   DIVISORES
========================================================= */

hr {{

    border:
        none;

    border-top:
        1px solid #E7E9ED;

    margin:
        1.4rem 0;
}}


/* =========================================================
   SCROLLBAR
========================================================= */

::-webkit-scrollbar {{
    width:
        7px;
}}

::-webkit-scrollbar-track {{
    background:
        transparent;
}}

::-webkit-scrollbar-thumb {{
    background:
        #D5D8DD;

    border-radius:
        20px;
}}

::-webkit-scrollbar-thumb:hover {{
    background:
        {ORANGE};
}}


/* =========================================================
   MÓVIL — INTI MOBILE EXPERIENCE
========================================================= */

@media (max-width: 900px) {{

    /* -----------------------------------------------------
       FONDO
    ----------------------------------------------------- */

    .stApp {{

        background:
            radial-gradient(
                circle at 105% 0%,
                rgba(255,101,0,.35),
                transparent 27%
            ),
            radial-gradient(
                circle at -10% 60%,
                rgba(255,101,0,.10),
                transparent 25%
            ),
            linear-gradient(
                180deg,
                #080B0F 0%,
                #0B1016 48%,
                #070A0D 100%
            ) !important;

        color:
            #FFFFFF !important;
    }}


    /* -----------------------------------------------------
       CONTENEDOR
    ----------------------------------------------------- */

    .block-container {{

        padding-top:
            .6rem !important;

        padding-left:
            1rem !important;

        padding-right:
            1rem !important;

        padding-bottom:
            2.5rem !important;

        max-width:
            100% !important;
    }}


    /* -----------------------------------------------------
       TEXTO
    ----------------------------------------------------- */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {{

        color:
            #FFFFFF !important;
    }}

    h1 {{

        font-size:
            2.15rem !important;

        line-height:
            1.08 !important;

        letter-spacing:
            -1px !important;
    }}

    h2 {{

        font-size:
            1.65rem !important;
    }}

    h3 {{

        font-size:
            1.2rem !important;
    }}

    .stMarkdown p {{

        color:
            #E8EAED !important;

        font-size:
            16px !important;

        line-height:
            1.65 !important;
    }}

    .stMarkdown strong {{

        color:
            #FFFFFF !important;
    }}


    /* -----------------------------------------------------
       CAPTIONS
    ----------------------------------------------------- */

    [data-testid="stCaptionContainer"] p {{

        color:
            #A8B0BA !important;

        font-size:
            13px !important;

        line-height:
            1.5 !important;
    }}


    /* -----------------------------------------------------
       CHAT
    ----------------------------------------------------- */

    [data-testid="stChatMessage"] {{

        background:
            linear-gradient(
                145deg,
                rgba(25,32,40,.98),
                rgba(14,20,27,.98)
            ) !important;

        border:
            1px solid rgba(255,255,255,.09) !important;

        border-radius:
            21px !important;

        padding:
            17px !important;

        margin-bottom:
            12px !important;

        box-shadow:
            0 15px 35px rgba(0,0,0,.25) !important;
    }}

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em,
    [data-testid="stChatMessage"] li {{

        color:
            #F7F8FA !important;
    }}

    [data-testid="stChatMessage"] p {{

        font-size:
            16px !important;

        line-height:
            1.7 !important;
    }}


    /* -----------------------------------------------------
       AVATARES
    ----------------------------------------------------- */

    [data-testid="stChatMessageAvatarAssistant"],
    [data-testid="stChatMessageAvatarUser"] {{

        border-radius:
            50% !important;

        overflow:
            hidden !important;
    }}


    /* -----------------------------------------------------
       FORMULARIO
    ----------------------------------------------------- */

    [data-testid="stForm"] {{

        background:
            rgba(15,21,28,.97) !important;

        border:
            1px solid rgba(255,255,255,.10) !important;

        border-radius:
            20px !important;

        padding:
            10px !important;

        box-shadow:
            0 18px 45px rgba(0,0,0,.35) !important;
    }}


    /* -----------------------------------------------------
       INPUT
    ----------------------------------------------------- */

    .stTextInput input {{

        background:
            #171D24 !important;

        color:
            #FFFFFF !important;

        border:
            1px solid rgba(255,255,255,.12) !important;

        min-height:
            52px !important;

        border-radius:
            14px !important;

        font-size:
            16px !important;

        padding:
            0 15px !important;
    }}

    .stTextInput input::placeholder {{

        color:
            #89939E !important;
    }}

    .stTextInput input:focus {{

        border-color:
            {ORANGE} !important;

        box-shadow:
            0 0 0 3px rgba(255,101,0,.12) !important;
    }}


    /* -----------------------------------------------------
       ENVIAR
    ----------------------------------------------------- */

    [data-testid="stFormSubmitButton"] button {{

        min-height:
            52px !important;

        border-radius:
            14px !important;

        background:
            linear-gradient(
                135deg,
                {ORANGE},
                {ORANGE_2}
            ) !important;

        color:
            #FFFFFF !important;

        border:
            none !important;

        font-size:
            22px !important;

        box-shadow:
            0 10px 25px rgba(255,101,0,.28) !important;
    }}


    /* -----------------------------------------------------
       BOTONES
    ----------------------------------------------------- */

    .stButton > button {{

        background:
            linear-gradient(
                145deg,
                #151C24,
                #10161D
            ) !important;

        color:
            #F8FAFC !important;

        border:
            1px solid rgba(255,255,255,.09) !important;

        border-radius:
            17px !important;

        min-height:
            58px !important;

        font-size:
            14px !important;

        box-shadow:
            0 10px 25px rgba(0,0,0,.20) !important;
    }}

    .stButton > button:hover {{

        border-color:
            {ORANGE} !important;

        color:
            {ORANGE_2} !important;
    }}


    /* -----------------------------------------------------
       ALERTAS
    ----------------------------------------------------- */

    [data-testid="stAlert"] {{

        background:
            rgba(17,28,23,.96) !important;

        border:
            1px solid rgba(71,190,110,.20) !important;
    }}

    [data-testid="stAlert"] * {{

        color:
            #FFFFFF !important;
    }}


    /* -----------------------------------------------------
       DIVISORES
    ----------------------------------------------------- */

    hr {{

        border-top:
            1px solid rgba(255,255,255,.10) !important;
    }}


    /* -----------------------------------------------------
       IMÁGENES
    ----------------------------------------------------- */

    [data-testid="stImage"] img {{

        border-radius:
            18px;
    }}


    /* -----------------------------------------------------
       SIDEBAR
    ----------------------------------------------------- */

    [data-testid="stSidebar"] {{

        background:
            linear-gradient(
                180deg,
                #090E13,
                #111923
            ) !important;
    }}


    /* -----------------------------------------------------
       SCROLLBAR
    ----------------------------------------------------- */

    ::-webkit-scrollbar {{

        width:
            4px;
    }}

    ::-webkit-scrollbar-thumb {{

        background:
            {ORANGE};
    }}

}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# API
# ============================================================

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    "",
)

if not api_key:

    st.error(
        "INTI no puede iniciar porque falta la configuración "
        "del servicio de inteligencia artificial."
    )

    st.stop()


# ============================================================
# MENSAJE INICIAL
# ============================================================

MENSAJE_INICIAL = {

    "role": "assistant",

    "content": (
        "¡Hola! 👋 Soy **INTI**, tu asistente virtual de "
        "**INTILED**.\n\n"
        "Puedo ayudarte a explorar soluciones de "
        "**eficiencia energética, energía solar e "
        "infraestructura eléctrica**, orientarte sobre "
        "nuestros servicios o iniciar una solicitud con "
        "nuestro equipo.\n\n"
        "**¿Qué proyecto o necesidad tienes en mente?**"
    ),
}


# ============================================================
# ESTADO
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


    historial = list(
        st.session_state.messages
    )


    st.session_state.messages.append(
        {
            "role": "user",
            "content": pregunta,
        }
    )


    try:

        respuesta = responder_inti(

            pregunta=pregunta,

            historial=historial,

            api_key=api_key,

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
            "content": respuesta,
        }
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:


    if logo_ok:

        st.image(
            LOGO,
            use_container_width=True,
        )

    else:

        st.markdown(
            "# INTILED"
        )


    st.caption(
        "ENERGÍA · TECNOLOGÍA · FUTURO"
    )


    st.divider()


    st.caption(
        "NAVEGACIÓN"
    )


    if st.button(
        "◉  Hablar con INTI",
        use_container_width=True,
        key="side_chat",
    ):

        pass


    if st.button(
        "⚡  Soluciones",
        use_container_width=True,
        key="side_services",
    ):

        procesar_mensaje(
            "Quiero explorar las soluciones "
            "y servicios de INTILED."
        )

        st.rerun()


    if st.button(
        "◫  Estimar proyecto",
        use_container_width=True,
        key="side_quote",
    ):

        procesar_mensaje(
            "Quiero realizar un ejercicio teórico "
            "de estimación para mi proyecto."
        )

        st.rerun()


    if st.button(
        "◷  Agendar reunión",
        use_container_width=True,
        key="side_meeting",
    ):

        procesar_mensaje(
            "Quiero solicitar una reunión "
            "con el equipo de INTILED."
        )

        st.rerun()


    if st.button(
        "◎  PQR / PQRS",
        use_container_width=True,
        key="side_pqrs",
    ):

        procesar_mensaje(
            "Quiero realizar una PQR o PQRS."
        )

        st.rerun()


    st.divider()


    st.caption(
        "TU ASISTENTE"
    )


    if avatar_ok:

        st.image(
            AVATAR,
            width=145,
        )


    st.markdown(
        "### INTI"
    )


    st.write(
        "**Inteligencia que conecta tus ideas "
        "con soluciones energéticas.**"
    )


    st.caption(
        "Disponible para orientarte en tus proyectos "
        "y conectarte con INTILED."
    )


    st.divider()


    st.caption(
        "● SISTEMA OPERATIVO"
    )

    st.write(
        "🟢 **INTI en línea**"
    )


# ============================================================
# BARRA SUPERIOR
# ============================================================

top_avatar, top_name, top_status = st.columns(
    [0.7, 5, 1.4],
    vertical_alignment="center",
)


with top_avatar:

    if avatar_ok:

        st.image(
            AVATAR,
            width=70,
        )

    else:

        st.markdown(
            "### ⚡"
        )


with top_name:

    st.markdown(
        "### INTI"
    )

    st.caption(
        "INTILED Intelligence · Asistente energético"
    )


with top_status:

    st.success(
        "● EN LÍNEA"
    )


# ============================================================
# HERO
# ============================================================

st.write("")


hero_text, hero_visual = st.columns(
    [3.2, 1],
    gap="large",
    vertical_alignment="center",
)


with hero_text:

    st.caption(
        "INTILED · INTELLIGENT ENERGY EXPERIENCE"
    )


    st.markdown(
        "# Energía inteligente.  \n"
        "Decisiones más brillantes."
    )


    st.markdown(
        "Conversa con **INTI**, explora soluciones "
        "energéticas y convierte una necesidad en "
        "el próximo proyecto de INTILED."
    )


with hero_visual:

    if avatar_ok:

        st.image(
            AVATAR,
            use_container_width=True,
        )


# ============================================================
# ACCIONES RÁPIDAS
# ============================================================

st.write("")

st.markdown(
    "### ¿Qué quieres hacer?"
)

st.caption(
    "Elige una ruta o simplemente cuéntale a INTI "
    "lo que necesitas."
)


a1, a2, a3, a4 = st.columns(
    4,
    gap="medium",
)


with a1:

    accion_servicios = st.button(
        "⚡ EXPLORAR SOLUCIONES",
        use_container_width=True,
        key="action_services",
    )


with a2:

    accion_solar = st.button(
        "☀️ ENERGÍA SOLAR",
        use_container_width=True,
        key="action_solar",
    )


with a3:

    accion_estimar = st.button(
        "📊 ESTIMAR PROYECTO",
        use_container_width=True,
        key="action_quote",
    )


with a4:

    accion_reunion = st.button(
        "◷ HABLAR CON EL EQUIPO",
        use_container_width=True,
        key="action_meeting",
    )


if accion_servicios:

    procesar_mensaje(
        "Quiero explorar las soluciones "
        "que ofrece INTILED."
    )

    st.rerun()


if accion_solar:

    procesar_mensaje(
        "Estoy interesado en energía solar. "
        "Quiero conocer qué soluciones puede "
        "ofrecer INTILED."
    )

    st.rerun()


if accion_estimar:

    procesar_mensaje(
        "Quiero realizar un ejercicio teórico "
        "de estimación para mi proyecto. "
        "Entiendo que no corresponde a una "
        "cotización oficial de INTILED."
    )

    st.rerun()


if accion_reunion:

    procesar_mensaje(
        "Quiero solicitar una reunión "
        "con el equipo de INTILED."
    )

    st.rerun()


# ============================================================
# CHAT
# ============================================================

st.write("")
st.write("")


chat_title, reset_col = st.columns(
    [5, 1.4],
    vertical_alignment="center",
)


with chat_title:

    st.markdown(
        "## 💬 Conversa con INTI"
    )

    st.caption(
        "Describe tu necesidad como lo harías "
        "con un asesor."
    )


with reset_col:

    if st.button(
        "↻ Nuevo chat",
        use_container_width=True,
        key="reset_chat",
    ):

        st.session_state.messages = [
            MENSAJE_INICIAL.copy()
        ]

        st.rerun()


st.write("")


# ============================================================
# MENSAJES
# ============================================================

for mensaje in st.session_state.messages:

    role = mensaje.get(
        "role",
        "assistant",
    )

    content = mensaje.get(
        "content",
        "",
    )


    if role == "assistant":

        avatar = (
            AVATAR
            if avatar_ok
            else "⚡"
        )

    else:

        avatar = "👤"


    with st.chat_message(
        role,
        avatar=avatar,
    ):

        if role == "assistant":

            st.caption(
                "INTI · INTILED"
            )


        st.markdown(
            content
        )


# ============================================================
# CAMPO DE MENSAJE
# ============================================================

st.write("")


with st.form(
    "inti_message_form",
    clear_on_submit=True,
):

    pregunta = st.text_input(
        "Mensaje",
        placeholder=(
            "Pregúntale algo a INTI..."
        ),
        label_visibility="collapsed",
    )


    enviar = st.form_submit_button(
        "➜  Enviar",
        use_container_width=True,
    )


if enviar and pregunta.strip():

    procesar_mensaje(
        pregunta
    )

    st.rerun()


st.caption(
    "INTI ofrece orientación inicial. Las decisiones "
    "técnicas, comerciales y contractuales son validadas "
    "por el equipo de INTILED."
)


# ============================================================
# ECOSISTEMA
# ============================================================

st.write("")
st.divider()


st.caption(
    "EXPLORA EL ECOSISTEMA INTILED"
)


d1, d2, d3 = st.columns(
    3,
    gap="medium",
)


with d1:

    if st.button(
        "🍃 EFICIENCIA ENERGÉTICA",
        use_container_width=True,
        key="discover_efficiency",
    ):

        procesar_mensaje(
            "Quiero conocer las soluciones de "
            "eficiencia energética de INTILED."
        )

        st.rerun()


with d2:

    if st.button(
        "☀️ GENERACIÓN SOLAR",
        use_container_width=True,
        key="discover_solar",
    ):

        procesar_mensaje(
            "Quiero conocer las soluciones "
            "de generación solar de INTILED."
        )

        st.rerun()


with d3:

    if st.button(
        "⚙️ INFRAESTRUCTURA ELÉCTRICA",
        use_container_width=True,
        key="discover_electric",
    ):

        procesar_mensaje(
            "Quiero conocer las soluciones "
            "de infraestructura eléctrica "
            "de INTILED."
        )

        st.rerun()


# ============================================================
# CONTACTO
# ============================================================

st.write("")
st.divider()


contacto, horario, identidad = st.columns(
    [1.4, 1, 1.2],
    gap="large",
)


with contacto:

    st.markdown(
        "### INTILED S.A.S. BIC"
    )

    st.write(
        "📍 Calle 11 #36-46, La Castellana  \n"
        "Pasto, Nariño, Colombia"
    )

    st.write(
        "✉️ comercial@intiled.com.co"
    )


with horario:

    st.markdown(
        "### Atención"
    )

    st.write(
        "**Lunes a viernes**  \n"
        "8:00 a. m. – 6:00 p. m."
    )

    st.write(
        "**Sábados**  \n"
        "8:00 a. m. – 12:00 p. m."
    )


with identidad:

    st.markdown(
        "### Energía con propósito"
    )

    st.write(
        "Tecnología, eficiencia y sostenibilidad "
        "para transformar proyectos en soluciones."
    )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.divider()


year = datetime.now().year


st.caption(
    f"© {year} INTILED S.A.S. BIC · "
    "INTI — Intelligent Energy Experience ⚡"
)
