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

AZUL_ACCENTO = "#1D70B8"
AZUL_CHAT_USER = "#EBF3FA"

OSCURO = "#0F172A"
OSCURO_2 = "#1E293B"

TEXTO = "#1E293B"
GRIS = "#64748B"

BORDE = "#E2E8F0"
FONDO = "#F8FAFC"
BLANCO = "#FFFFFF"


# ============================================================
# CSS MEJORADO
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   TIPOGRAFÍA Y NAVEGACIÓN GENERAL
========================================================= */

html, body, [class*="css"] {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-size: 16px;
    color: {TEXTO};
}}

p {{
    font-size: 16px;
    line-height: 1.6;
}}

.block-container {{
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}}

/* Ocultar elementos predeterminados de Streamlit */
#MainMenu, footer, header {{
    visibility: hidden;
}}


/* =========================================================
   SIDEBAR ELEGANTE
========================================================= */

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}}

[data-testid="stSidebar"] * {{
    color: #F8FAFC !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    background: rgba(255, 255, 255, 0.04);
    color: #E2E8F0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    min-height: 48px;
    font-size: 15px;
    font-weight: 500;
    text-align: left;
    transition: all 0.2s ease;
    margin-bottom: 4px;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: {NARANJA};
    border-color: {NARANJA};
    color: white !important;
    transform: translateX(4px);
    box-shadow: 0 4px 14px rgba(245, 102, 0, 0.35);
}}


/* =========================================================
   TARJETAS DE ACCESOS RÁPIDOS (BOTONES INICIALES)
========================================================= */

.stButton > button {{
    width: 100%;
    min-height: 64px;
    border-radius: 16px;
    border: 1px solid {BORDE};
    background: {BLANCO};
    color: {TEXTO};
    font-size: 15px;
    font-weight: 600;
    transition: all 0.25s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}}

.stButton > button:hover {{
    border-color: {NARANJA};
    color: {NARANJA};
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(245, 102, 0, 0.12);
}}


/* =========================================================
   ESTILIZADO DE MENSAJES DE CHAT
========================================================= */

/* Estilo general para burbujas de chat */
[data-testid="stChatMessage"] {{
    border-radius: 18px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border: 1px solid {BORDE};
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}}

/* Asistente: Fondo ligeramente anaranjado */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
    background-color: #FFF9F5;
    border-color: #FFE6D5;
}}

/* Usuario: Fondo azulino para contrastar */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background-color: {AZUL_CHAT_USER};
    border-color: #D0E1F9;
}}


/* =========================================================
   FORMULARIO Y ENTRADA DE TEXTO
========================================================= */

[data-testid="stForm"] {{
    background: {BLANCO};
    border: 1px solid {BORDE};
    border-radius: 20px;
    padding: 10px 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}}

.stTextInput input {{
    min-height: 48px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    background: #F8FAFC;
    font-size: 16px;
}}

.stTextInput input:focus {{
    border-color: {NARANJA};
    box-shadow: 0 0 0 3px rgba(245, 102, 0, 0.15);
}}

[data-testid="stFormSubmitButton"] button {{
    background: linear-gradient(135deg, {NARANJA}, #FF7A00);
    color: white !important;
    border: none;
    font-size: 20px;
    min-height: 48px;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(245, 102, 0, 0.3);
}}

[data-testid="stFormSubmitButton"] button:hover {{
    background: {NARANJA_OSCURO};
    transform: translateY(-1px);
}}

/* =========================================================
   TARJETAS LATERALES Y DE INFORMACIÓN
========================================================= */

.info-card {{
    background: {BLANCO};
    border: 1px solid {BORDE};
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}}

.contact-link {{
    color: {AZUL_ACCENTO};
    text-decoration: none;
    font-weight: 500;
}}

.contact-link:hover {{
    text-decoration: underline;
}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# VERIFICACIÓN DE ARCHIVOS
# ============================================================

logo_existe = Path(LOGO_PATH).exists()
avatar_existe = Path(INTI_AVATAR_PATH).exists()


# ============================================================
# API KEY
# ============================================================

api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("No se encontró GEMINI_API_KEY en Streamlit Secrets.")
    st.stop()


# ============================================================
# MENSAJE INICIAL
# ============================================================

MENSAJE_INICIAL = {
    "role": "assistant",
    "content": (
        "¡Hola! 👋 Soy **INTI**, el asistente virtual de **INTILED**.\n\n"
        "Estoy aquí para orientarte sobre nuestros servicios, proyectos y soluciones energéticas.\n\n"
        "**¿En qué puedo ayudarte hoy?**"
    )
}


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [MENSAJE_INICIAL.copy()]


# ============================================================
# PROCESAR MENSAJE (SIN MODIFICACIONES EN EL MOTOR IA)
# ============================================================

def procesar_mensaje(pregunta):
    if not pregunta:
        return

    pregunta = pregunta.strip()
    if not pregunta:
        return

    historial_anterior = list(st.session_state.messages)

    st.session_state.messages.append({
        "role": "user",
        "content": pregunta
    })

    try:
        respuesta = responder_inti(
            pregunta=pregunta,
            historial=historial_anterior,
            api_key=api_key
        )
    except Exception:
        respuesta = (
            "⚠️ En este momento tuve un inconveniente al procesar tu consulta. "
            "Por favor intenta nuevamente."
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": respuesta
    })


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    if logo_existe:
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown("# 🟠 INTILED")

    st.caption("Soluciones que iluminan el futuro")
    st.divider()

    st.markdown("#### 📌 Navegación")

    if st.button("💬   Chat con INTI", use_container_width=True, key="sidebar_chat"):
        pass

    if st.button("💡   Servicios", use_container_width=True, key="sidebar_servicios"):
        procesar_mensaje("Quiero conocer los servicios que ofrece INTILED.")
        st.rerun()

    if st.button("📄   Cotización", use_container_width=True, key="sidebar_cotizacion"):
        procesar_mensaje("Quiero solicitar una cotización para un proyecto.")
        st.rerun()

    if st.button("📅   Agendar cita", use_container_width=True, key="sidebar_cita"):
        procesar_mensaje("Quiero solicitar una reunión o visita técnica.")
        st.rerun()

    if st.button("🎧   PQR / PQRS", use_container_width=True, key="sidebar_pqr"):
        procesar_mensaje("Necesito orientación para presentar una PQR o PQRS.")
        st.rerun()

    if st.button("ⓘ   Acerca de INTILED", use_container_width=True, key="sidebar_acerca"):
        procesar_mensaje("Cuéntame sobre INTILED, su enfoque y sus servicios.")
        st.rerun()

    st.divider()
    st.caption("🌱 Comprometidos con un futuro más sostenible.")


# ============================================================
# ENCABEZADO PRINCIPAL
# ============================================================

header_avatar, header_texto, header_estado = st.columns([1, 5, 1.8], vertical_alignment="center")

with header_avatar:
    if avatar_existe:
        st.image(INTI_AVATAR_PATH, width=100)
    else:
        st.markdown("# 👷🏻‍♂️")

with header_texto:
    st.markdown("<h1 style='margin-bottom: 0px;'>INTI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top: 0px; color: #64748B;'>Asistente Virtual de INTILED</h3>", unsafe_allow_html=True)

with header_estado:
    st.success("● En línea")
    st.caption("Energía, eficiencia y sostenibilidad")

st.divider()


# ============================================================
# ACCESOS RÁPIDOS / TARJETAS INTERACTIVAS
# ============================================================

st.markdown("### ¿Cómo puedo ayudarte?")
st.caption("Selecciona una opción o escribe tu mensaje directamente.")

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    servicios = st.button("💡 Services\n\nConoce nuestras soluciones", use_container_width=True, key="servicios_superior")

with c2:
    cotizacion = st.button("📄 Cotización\n\nSolicita una propuesta", use_container_width=True, key="cotizacion_superior")

with c3:
    cita = st.button("📅 Agendar cita\n\nReúnete con nuestro equipo", use_container_width=True, key="cita_superior")

with c4:
    pqr = st.button("🎧 PQR / PQRS\n\nPeticiones, quejas o reclamos", use_container_width=True, key="pqr_superior")

# Acciones rápidas
if servicios:
    procesar_mensaje("Quiero conocer los servicios y soluciones que ofrece INTILED.")
    st.rerun()

if cotizacion:
    procesar_mensaje("Quiero solicitar una cotización para un proyecto.")
    st.rerun()

if cita:
    procesar_mensaje("Quiero agendar una reunión o visita técnica con el equipo de INTILED.")
    st.rerun()

if pqr:
    procesar_mensaje("Necesito orientación para presentar una PQR o PQRS.")
    st.rerun()

st.write("")


# ============================================================
# CUERPO PRINCIPAL
# ============================================================

chat_col, info_col = st.columns([3.2, 1.1], gap="large")


# ============================================================
# CHAT
# ============================================================

with chat_col:
    st.markdown("### 💬 Conversa con INTI")

    # MOSTRAR CONVERSACIÓN
    for mensaje in st.session_state.messages:
        if mensaje["role"] == "assistant":
            avatar = INTI_AVATAR_PATH if avatar_existe else "👷🏻‍♂️"
        else:
            avatar = "👤"

        with st.chat_message(mensaje["role"], avatar=avatar):
            st.markdown(mensaje["content"])

    # FORMULARIO ENTRADA
    st.write("")
    with st.form("formulario_inti", clear_on_submit=True):
        texto_col, boton_col = st.columns([8, 1], vertical_alignment="bottom")

        with texto_col:
            pregunta = st.text_input(
                "Mensaje",
                placeholder="Escribe tu mensaje para INTI...",
                label_visibility="collapsed"
            )

        with boton_col:
            enviar = st.form_submit_button("➤", use_container_width=True)

    if enviar and pregunta.strip():
        procesar_mensaje(pregunta)
        st.rerun()

    # NUEVA CONVERSACIÓN
    espacio, limpiar = st.columns([5, 2.5])
    with limpiar:
        if st.button("🗑️ Nueva conversación", use_container_width=True, key="nueva_conversacion"):
            st.session_state.messages = [MENSAJE_INICIAL.copy()]
            st.rerun()


# ============================================================
# PANEL DERECHO
# ============================================================

with info_col:
    # SOBRE INTI
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("#### Sobre INTI")
    st.write("Soy **INTI**, el asistente virtual inteligente de **INTILED S.A.S. BIC**.")
    st.caption("Diseñado para brindarte soporte técnico y comercial de forma rápida.")
    st.markdown("</div>", unsafe_allow_html=True)

    # CONTACTO INTERACTIVO
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("#### 📍 Contacto Directo")
    st.write("**INTILED S.A.S. BIC**")
    st.write("Calle 11 #36-46, La Castellana")
    st.caption("Pasto, Nariño, Colombia")
    st.markdown("---")
    st.markdown("📞 <a class='contact-link' href='tel:+576027337893'>+57 602 733 7893</a>", unsafe_allow_html=True)
    st.markdown("📱 <a class='contact-link' href='https://wa.me/573046702584'>+57 304 670 2584</a>", unsafe_allow_html=True)
    st.markdown("✉️ <a class='contact-link' href='mailto:comercial@intiled.com.co'>comercial@intiled.com.co</a>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # HORARIOS
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.markdown("#### 🕐 Horario de Atención")
    st.write("**Lunes a viernes:** 8:00 a. m. – 6:00 p. m.")
    st.write("**Sábados:** 8:00 a. m. – 12:00 p. m.")
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.divider()

f1, f2, f3, f4, f5 = st.columns(5)
with f1: st.caption("🍃 Eficiencia energética")
with f2: st.caption("☀️ Energía solar")
with f3: st.caption("⚙️ Infraestructura eléctrica")
with f4: st.caption("👥 Acompañamiento técnico")
with f5: st.caption("🌱 Sostenibilidad")

año = datetime.now().year
st.caption(f"© {año} INTILED S.A.S. BIC · INTI — Asistente Virtual Inteligente")
