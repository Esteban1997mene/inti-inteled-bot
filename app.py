import streamlit as st
from datetime import datetime
from pathlib import Path
from modules.inti_ai import responder_inti


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="INTI | INTILED",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO = "assets/logo_intiled.png"
AVATAR = "assets/inti_avatar.png"

logo_ok = Path(LOGO).exists()
avatar_ok = Path(AVATAR).exists()


# ============================================================
# PALETA
# ============================================================

ORANGE = "#FF6500"
ORANGE_2 = "#FF8A00"
DARK = "#0B1016"
DARK_2 = "#111923"
TEXT = "#101828"
MUTED = "#667085"
BORDER = "#E7E9EE"


# ============================================================
# CSS — INTI EXPERIENCE V2
# ============================================================

st.markdown(
    f"""
<style>

/* ---------------------------------------------------------
   RESET / GLOBAL
--------------------------------------------------------- */

html {{
    scroll-behavior: smooth;
}}

html, body, [class*="css"] {{
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
            circle at 82% 0%,
            rgba(255,101,0,.13),
            transparent 26%
        ),
        radial-gradient(
            circle at 18% 70%,
            rgba(255,138,0,.055),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #FFFFFF 0%,
            #F8F9FB 48%,
            #F4F6F8 100%
        );
    color: {TEXT};
}}

.block-container {{
    max-width: 1380px;
    padding-top: 1.5rem;
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


/* ---------------------------------------------------------
   TIPOGRAFÍA
--------------------------------------------------------- */

h1 {{
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: -1.7px !important;
    color: {DARK} !important;
}}

h2 {{
    font-size: 2rem !important;
    font-weight: 780 !important;
    letter-spacing: -.8px !important;
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

small {{
    color: {MUTED};
}}


/* ---------------------------------------------------------
   SIDEBAR
--------------------------------------------------------- */

[data-testid="stSidebar"] {{
    background:
        radial-gradient(
            circle at 50% 95%,
            rgba(255,101,0,.28),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #090E13 0%,
            #111923 58%,
            #0A1016 100%
        );

    border-right: 1px solid rgba(255,255,255,.06);
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.25rem;
}}

[data-testid="stSidebar"] * {{
    color: #FFFFFF;
}}

[data-testid="stSidebar"] p {{
    font-size: 15px;
}}

[data-testid="stSidebar"] hr {{
    border: none;
    border-top: 1px solid rgba(255,255,255,.09);
}}

[data-testid="stSidebar"] .stButton > button {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 14px;
    color: rgba(255,255,255,.84);
    min-height: 50px;
    font-size: 15px;
    font-weight: 600;
    text-align: left;
    transition: all .22s ease;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background:
        linear-gradient(
            90deg,
            rgba(255,101,0,.95),
            rgba(255,138,0,.85)
        );
    border-color: rgba(255,255,255,.08);
    color: white;
    transform: translateX(4px);
    box-shadow: 0 8px 28px rgba(255,101,0,.22);
}}


/* ---------------------------------------------------------
   BOTONES GENERALES
--------------------------------------------------------- */

.stButton > button {{
    border-radius: 17px;
    border: 1px solid {BORDER};
    background: rgba(255,255,255,.88);
    min-height: 64px;
    color: {TEXT};
    font-size: 16px;
    font-weight: 650;
    transition: all .22s ease;
    box-shadow:
        0 7px 25px rgba(16,24,40,.045);
}}

.stButton > button:hover {{
    border-color: rgba(255,101,0,.65);
    color: {ORANGE};
    transform: translateY(-3px);
    box-shadow:
        0 15px 35px rgba(16,24,40,.10),
        0 4px 15px rgba(255,101,0,.07);
}}


/* ---------------------------------------------------------
   CHAT MESSAGES
--------------------------------------------------------- */

[data-testid="stChatMessage"] {{
    background: rgba(255,255,255,.91);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(226,230,235,.95);
    border-radius: 22px;
    padding: 18px 22px;
    margin-bottom: 14px;

    box-shadow:
        0 7px 25px rgba(16,24,40,.045);

    transition:
        transform .18s ease,
        box-shadow .18s ease;
}}

[data-testid="stChatMessage"]:hover {{
    transform: translateY(-1px);

    box-shadow:
        0 12px 35px rgba(16,24,40,.07);
}}

[data-testid="stChatMessage"] p {{
    font-size: 17px;
    line-height: 1.72;
}}


/* Avatar */

[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {{
    border-radius: 50%;
    overflow: hidden;
}}


/* ---------------------------------------------------------
   FORMULARIO CHAT
--------------------------------------------------------- */

[data-testid="stForm"] {{
    background:
        rgba(255,255,255,.94);

    backdrop-filter:
        blur(20px);

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
    min-height: 58px;
    border: none !important;
    border-radius: 16px;
    background: #F7F8FA;
    font-size: 17px;
    padding-left: 18px;
}}

.stTextInput input:focus {{
    background: #FFFFFF;
    box-shadow:
        0 0 0 2px rgba(255,101,0,.13) !important;
}}


/* ---------------------------------------------------------
   BOTÓN ENVIAR
--------------------------------------------------------- */

[data-testid="stFormSubmitButton"] button {{
    min-height: 58px;

    border-radius: 16px;

    border: none;

    background:
        linear-gradient(
            135deg,
            {ORANGE},
            {ORANGE_2}
        );

    color: white;

    font-size: 24px;

    box-shadow:
        0 9px 25px rgba(255,101,0,.27);
}}

[data-testid="stFormSubmitButton"] button:hover {{
    color: white;

    background:
        linear-gradient(
            135deg,
            #ED5D00,
            {ORANGE}
        );

    transform:
        translateY(-2px);

    box-shadow:
        0 13px 30px rgba(255,101,0,.34);
}}


/* ---------------------------------------------------------
   ALERTAS / STATUS
--------------------------------------------------------- */

[data-testid="stAlert"] {{
    border-radius: 16px;
    border: none;
}}


/* ---------------------------------------------------------
   EXPANDER
--------------------------------------------------------- */

[data-testid="stExpander"] {{
    background: rgba(255,255,255,.80);
    border: 1px solid {BORDER};
    border-radius: 16px;
    overflow: hidden;
}}


/* ---------------------------------------------------------
   DIVIDER
--------------------------------------------------------- */

hr {{
    border: none;
    border-top: 1px solid #E7E9ED;
    margin: 1.4rem 0;
}}


/* ---------------------------------------------------------
   SCROLLBAR
--------------------------------------------------------- */

::-webkit-scrollbar {{
    width: 8px;
}}

::-webkit-scrollbar-track {{
    background: transparent;
}}

::-webkit-scrollbar-thumb {{
    background: #D5D8DD;
    border-radius: 20px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {ORANGE};
}}


/* ---------------------------------------------------------
   MOBILE
--------------------------------------------------------- */

@media (max-width: 900px) {{

    .block-container {{
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: .8rem;
    }}

    h1 {{
        font-size: 2.15rem !important;
    }}

    h2 {{
        font-size: 1.6rem !important;
    }}

    p {{
        font-size: 16px;
    }}

    [data-testid="stChatMessage"] p {{
        font-size: 16px;
    }}

}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# GEMINI
# ============================================================

api_key = st.secrets.get("GEMINI_API_KEY", "")

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
        "¡Hola! 👋 Soy **INTI**, tu asistente virtual de **INTILED**.\n\n"
        "Puedo ayudarte a explorar soluciones de **eficiencia energética, "
        "energía solar e infraestructura eléctrica**, orientarte sobre "
        "nuestros servicios o iniciar una solicitud con nuestro equipo.\n\n"
        "**¿Qué proyecto o necesidad tienes en mente?**"
    ),
}


if "messages" not in st.session_state:
    st.session_state.messages = [MENSAJE_INICIAL.copy()]


# ============================================================
# FUNCIÓN PARA ENVIAR MENSAJES
# ============================================================

def procesar_mensaje(pregunta):

    if not pregunta:
        return

    pregunta = pregunta.strip()

    if not pregunta:
        return

    historial = list(st.session_state.messages)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": pregunta,
        }
    )

    respuesta = responder_inti(
        pregunta=pregunta,
        historial=historial,
        api_key=api_key,
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
        st.markdown("# INTILED")

    st.caption(
        "ENERGÍA · TECNOLOGÍA · FUTURO"
    )

    st.divider()

    st.caption("NAVEGACIÓN")

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
            "Quiero explorar las soluciones y servicios de INTILED."
        )
        st.rerun()

    if st.button(
        "◫  Solicitar cotización",
        use_container_width=True,
        key="side_quote",
    ):
        procesar_mensaje(
            "Quiero solicitar una cotización para mi proyecto."
        )
        st.rerun()

    if st.button(
        "◷  Agendar reunión",
        use_container_width=True,
        key="side_meeting",
    ):
        procesar_mensaje(
            "Quiero solicitar una reunión con el equipo de INTILED."
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

    st.caption("TU ASISTENTE")

    if avatar_ok:
        st.image(
            AVATAR,
            width=145,
        )

    st.markdown("### INTI")

    st.write(
        "**Inteligencia que conecta tus ideas "
        "con soluciones energéticas.**"
    )

    st.caption(
        "Disponible para orientarte en tus proyectos "
        "y conectarte con INTILED."
    )

    st.divider()

    st.caption("● SISTEMA OPERATIVO")
    st.write("🟢 **INTI en línea**")


# ============================================================
# TOP BAR
# ============================================================

top_logo, top_name, top_status = st.columns(
    [0.65, 6, 1.4],
    vertical_alignment="center",
)

with top_logo:

    if avatar_ok:
        st.image(
            AVATAR,
            width=72,
        )
    else:
        st.markdown("### ⚡")


with top_name:

    st.markdown("### INTI")

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
    [2.8, 1],
    gap="large",
    vertical_alignment="center",
)


with hero_text:

    st.caption(
        "INTILED · INTELLIGENT ENERGY EXPERIENCE"
    )

    st.markdown(
        "# Energía inteligente.\n"
        "Decisiones más brillantes."
    )

    st.markdown(
        "Conversa con **INTI**, explora soluciones energéticas "
        "y convierte una idea en el próximo proyecto de INTILED."
    )


with hero_visual:

    if avatar_ok:
        st.image(
            AVATAR,
            use_container_width=True,
        )


# ============================================================
# ACCIONES PRINCIPALES
# ============================================================

st.write("")

st.markdown(
    "### ¿Qué quieres hacer?"
)

st.caption(
    "Elige una ruta o simplemente cuéntale a INTI lo que necesitas."
)


a1, a2, a3, a4 = st.columns(
    4,
    gap="medium",
)


with a1:

    accion_servicios = st.button(
        "⚡  EXPLORAR SOLUCIONES\n\n"
        "Descubre cómo puede ayudarte INTILED",
        use_container_width=True,
        key="action_services",
    )


with a2:

    accion_solar = st.button(
        "☀️  ENERGÍA SOLAR\n\n"
        "Explora soluciones fotovoltaicas",
        use_container_width=True,
        key="action_solar",
    )


with a3:

    accion_cotizar = st.button(
        "◫  COTIZAR PROYECTO\n\n"
        "Cuéntanos qué necesitas",
        use_container_width=True,
        key="action_quote",
    )


with a4:

    accion_reunion = st.button(
        "◷  HABLAR CON EL EQUIPO\n\n"
        "Solicita una reunión",
        use_container_width=True,
        key="action_meeting",
    )


if accion_servicios:
    procesar_mensaje(
        "Quiero explorar las soluciones que ofrece INTILED. "
        "Ayúdame a identificar cuál podría servirme."
    )
    st.rerun()


if accion_solar:
    procesar_mensaje(
        "Estoy interesado en energía solar. "
        "Quiero conocer qué soluciones puede ofrecer INTILED."
    )
    st.rerun()


if accion_cotizar:
    procesar_mensaje(
        "Tengo un proyecto y quiero solicitar una cotización."
    )
    st.rerun()


if accion_reunion:
    procesar_mensaje(
        "Quiero solicitar una reunión con el equipo de INTILED."
    )
    st.rerun()


# ============================================================
# CHAT
# ============================================================

st.write("")
st.write("")

chat_title, reset_col = st.columns(
    [6, 1.3],
    vertical_alignment="center",
)


with chat_title:

    st.markdown(
        "## Conversa con INTI"
    )

    st.caption(
        "Describe tu necesidad como lo harías con un asesor."
    )


with reset_col:

    if st.button(
        "↻  Nuevo chat",
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

    role = mensaje.get("role", "assistant")
    content = mensaje.get("content", "")

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
            st.caption("INTI · INTILED")

        st.markdown(content)


# ============================================================
# INPUT PREMIUM
# ============================================================

st.write("")

with st.form(
    "inti_message_form",
    clear_on_submit=True,
):

    input_col, send_col = st.columns(
        [10, 1],
        vertical_alignment="bottom",
    )

    with input_col:

        pregunta = st.text_input(
            "Mensaje",
            placeholder=(
                "Cuéntale a INTI qué necesitas..."
            ),
            label_visibility="collapsed",
        )

    with send_col:

        enviar = st.form_submit_button(
            "➜",
            use_container_width=True,
        )


if enviar and pregunta.strip():

    procesar_mensaje(
        pregunta
    )

    st.rerun()


st.caption(
    "INTI puede orientarte y ayudarte a iniciar solicitudes. "
    "Las decisiones técnicas, comerciales y contractuales "
    "son validadas por el equipo de INTILED."
)


# ============================================================
# DISCOVERY STRIP
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
        "🍃 EFICIENCIA ENERGÉTICA\n\n"
        "Optimiza el uso de la energía",
        use_container_width=True,
        key="discover_efficiency",
    ):

        procesar_mensaje(
            "Quiero conocer las soluciones de eficiencia "
            "energética de INTILED."
        )

        st.rerun()


with d2:

    if st.button(
        "☀️ GENERACIÓN SOLAR\n\n"
        "Transforma el sol en energía",
        use_container_width=True,
        key="discover_solar",
    ):

        procesar_mensaje(
            "Quiero conocer las soluciones de generación "
            "solar de INTILED."
        )

        st.rerun()


with d3:

    if st.button(
        "⚙️ INFRAESTRUCTURA ELÉCTRICA\n\n"
        "Soluciones para proyectos eléctricos",
        use_container_width=True,
        key="discover_electric",
    ):

        procesar_mensaje(
            "Quiero conocer las soluciones de infraestructura "
            "eléctrica de INTILED."
        )

        st.rerun()


# ============================================================
# CONTACTO — MINIMAL
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

footer_left, footer_right = st.columns(
    [4, 2],
)


with footer_left:

    st.caption(
        f"© {year} INTILED S.A.S. BIC · "
        "Todos los derechos reservados."
    )


with footer_right:

    st.caption(
        "INTI · Intelligent Energy Experience ⚡"
    )
