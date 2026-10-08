import streamlit as st
from datetime import datetime
from pathlib import Path

from modules.inti_ai import responder_inti
from modules.quotations import (
    calcular_sistema_fotovoltaico,
    generar_resumen_para_chat,
)
from modules.quotation_pdf import (
    generar_pdf_fotovoltaico,
    nombre_archivo_pdf,
)


# ============================================================
# CONFIGURACIÓN
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
TEXT = "#101828"
MUTED = "#667085"
BORDER = "#E7E9EE"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
<style>

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


/* SIDEBAR */

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
    border-top: 1px solid rgba(255,255,255,.10);
}}

[data-testid="stSidebar"] .stButton > button {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 14px;
    color: rgba(255,255,255,.88);
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
            {ORANGE},
            {ORANGE_2}
        );
    color: #FFFFFF;
    transform: translateX(4px);
    box-shadow: 0 8px 28px rgba(255,101,0,.22);
}}


/* BOTONES */

.stButton > button {{
    border-radius: 17px;
    border: 1px solid {BORDER};
    background: rgba(255,255,255,.94);
    min-height: 58px;
    color: {TEXT};
    font-size: 15px;
    font-weight: 650;
    transition: all .22s ease;
    box-shadow: 0 7px 25px rgba(16,24,40,.05);
}}

.stButton > button:hover {{
    border-color: rgba(255,101,0,.65);
    color: {ORANGE};
    transform: translateY(-2px);
    box-shadow:
        0 15px 35px rgba(16,24,40,.10),
        0 4px 15px rgba(255,101,0,.08);
}}


/* CHAT */

[data-testid="stChatMessage"] {{
    background: rgba(255,255,255,.95);
    border: 1px solid rgba(226,230,235,.95);
    border-radius: 22px;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 7px 25px rgba(16,24,40,.045);
}}

[data-testid="stChatMessage"] p {{
    font-size: 16px;
    line-height: 1.72;
    color: {TEXT};
}}


/* FORM */

[data-testid="stForm"] {{
    background: rgba(255,255,255,.96);
    border: 1px solid rgba(224,228,234,.95);
    border-radius: 22px;
    padding: 14px;
    box-shadow:
        0 18px 50px rgba(16,24,40,.09),
        0 3px 12px rgba(255,101,0,.05);
}}

.stTextInput input {{
    min-height: 55px;
    border: 1px solid #E6E9ED !important;
    border-radius: 15px;
    background: #F7F8FA;
    color: {TEXT};
    font-size: 16px;
    padding-left: 17px;
}}

.stTextInput input:focus {{
    background: #FFFFFF;
    border-color: {ORANGE} !important;
    box-shadow: 0 0 0 3px rgba(255,101,0,.10) !important;
}}

[data-testid="stFormSubmitButton"] button {{
    min-height: 55px;
    border-radius: 15px;
    border: none;
    background:
        linear-gradient(
            135deg,
            {ORANGE},
            {ORANGE_2}
        );
    color: #FFFFFF;
    font-size: 16px;
    box-shadow: 0 9px 25px rgba(255,101,0,.27);
}}

[data-testid="stFormSubmitButton"] button:hover {{
    color: #FFFFFF;
    border: none;
}}


/* MÉTRICAS */

[data-testid="stMetric"] {{
    background: rgba(255,255,255,.96);
    border: 1px solid #E7E9EE;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(16,24,40,.05);
}}

[data-testid="stMetricLabel"] {{
    font-weight: 650;
}}

[data-testid="stMetricValue"] {{
    color: {ORANGE};
}}


/* DOWNLOAD */

.stDownloadButton > button {{
    width: 100%;
    min-height: 58px;
    border: none;
    border-radius: 16px;
    background:
        linear-gradient(
            135deg,
            {ORANGE},
            {ORANGE_2}
        );
    color: white;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(255,101,0,.22);
}}

.stDownloadButton > button:hover {{
    color: white;
    border: none;
}}


/* MÓVIL */

@media (max-width: 900px) {{

    .stApp {{
        background:
            radial-gradient(
                circle at 105% 0%,
                rgba(255,101,0,.35),
                transparent 27%
            ),
            linear-gradient(
                180deg,
                #080B0F 0%,
                #0B1016 48%,
                #070A0D 100%
            ) !important;

        color: #FFFFFF !important;
    }}

    .block-container {{
        padding-top: .7rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 100% !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: #FFFFFF !important;
    }}

    h1 {{
        font-size: 2.1rem !important;
        line-height: 1.1 !important;
    }}

    h2 {{
        font-size: 1.6rem !important;
    }}

    .stMarkdown p {{
        color: #E8EAED !important;
        font-size: 16px !important;
    }}

    .stMarkdown strong {{
        color: #FFFFFF !important;
    }}

    [data-testid="stCaptionContainer"] p {{
        color: #A8B0BA !important;
    }}

    [data-testid="stChatMessage"] {{
        background:
            linear-gradient(
                145deg,
                rgba(25,32,40,.98),
                rgba(14,20,27,.98)
            ) !important;

        border:
            1px solid rgba(255,255,255,.09) !important;

        border-radius: 20px !important;
        padding: 16px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,.25) !important;
    }}

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] li {{
        color: #F7F8FA !important;
    }}

    [data-testid="stForm"] {{
        background: rgba(15,21,28,.97) !important;
        border: 1px solid rgba(255,255,255,.10) !important;
        border-radius: 20px !important;
        padding: 10px !important;
    }}

    .stTextInput input {{
        background: #171D24 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,.12) !important;
    }}

    .stTextInput input::placeholder {{
        color: #89939E !important;
    }}

    .stButton > button {{
        background:
            linear-gradient(
                145deg,
                #151C24,
                #10161D
            ) !important;

        color: #F8FAFC !important;
        border: 1px solid rgba(255,255,255,.09) !important;
    }}

    [data-testid="stMetric"] {{
        background: #131A22 !important;
        border: 1px solid rgba(255,255,255,.09) !important;
    }}

    [data-testid="stMetricLabel"] p {{
        color: #AEB7C2 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: #FF8A00 !important;
    }}

    [data-testid="stAlert"] * {{
        color: inherit !important;
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
        "¡Hola! 👋 Soy **INTI**, tu asistente virtual de **INTILED**.\n\n"
        "Puedo ayudarte a explorar soluciones de **eficiencia energética, "
        "energía solar e infraestructura eléctrica**, orientarte sobre "
        "nuestros servicios o ayudarte a realizar una "
        "**estimación teórica preliminar** de un proyecto solar.\n\n"
        "**¿Qué proyecto o necesidad tienes en mente?**"
    ),
}


# ============================================================
# ESTADOS
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        MENSAJE_INICIAL.copy()
    ]

if "modo_estimacion" not in st.session_state:
    st.session_state.modo_estimacion = False

if "resultado_solar" not in st.session_state:
    st.session_state.resultado_solar = None

if "pdf_solar" not in st.session_state:
    st.session_state.pdf_solar = None

if "datos_estimacion" not in st.session_state:
    st.session_state.datos_estimacion = {}


# ============================================================
# FUNCIONES
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


def abrir_estimacion():

    st.session_state.modo_estimacion = True
    st.session_state.resultado_solar = None
    st.session_state.pdf_solar = None


def cerrar_estimacion():

    st.session_state.modo_estimacion = False


def nueva_estimacion():

    st.session_state.resultado_solar = None
    st.session_state.pdf_solar = None
    st.session_state.datos_estimacion = {}


def nueva_conversacion():

    st.session_state.messages = [
        MENSAJE_INICIAL.copy()
    ]

    st.session_state.modo_estimacion = False
    st.session_state.resultado_solar = None
    st.session_state.pdf_solar = None
    st.session_state.datos_estimacion = {}


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
        "●  Hablar con INTI",
        use_container_width=True,
        key="side_chat",
    ):
        cerrar_estimacion()
        st.rerun()

    if st.button(
        "⚡  Soluciones",
        use_container_width=True,
        key="side_services",
    ):
        cerrar_estimacion()

        procesar_mensaje(
            "Quiero explorar las soluciones "
            "y servicios de INTILED."
        )

        st.rerun()

    if st.button(
        "📊  Estimar proyecto",
        use_container_width=True,
        key="side_quote",
    ):
        abrir_estimacion()
        st.rerun()

    if st.button(
        "◷  Agendar reunión",
        use_container_width=True,
        key="side_meeting",
    ):
        cerrar_estimacion()

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
        cerrar_estimacion()

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

    st.write("🟢 **INTI en línea**")


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
            width=68,
        )
    else:
        st.markdown("### ⚡")

with top_name:

    st.markdown("### INTI")

    st.caption(
        "INTILED Intelligence · Asistente energético"
    )

with top_status:

    st.success("● EN LÍNEA")


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
        "energéticas y transforma una necesidad "
        "en una oportunidad de proyecto."
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
st.markdown("### ¿Qué quieres hacer?")

st.caption(
    "Elige una ruta o simplemente conversa con INTI."
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

    cerrar_estimacion()

    procesar_mensaje(
        "Quiero explorar las soluciones "
        "que ofrece INTILED."
    )

    st.rerun()


if accion_solar:

    cerrar_estimacion()

    procesar_mensaje(
        "Estoy interesado en energía solar "
        "fotovoltaica. Quiero conocer qué "
        "alternativas podría evaluar."
    )

    st.rerun()


if accion_estimar:

    abrir_estimacion()
    st.rerun()


if accion_reunion:

    cerrar_estimacion()

    procesar_mensaje(
        "Quiero solicitar una reunión "
        "con el equipo de INTILED."
    )

    st.rerun()


# ============================================================
# MODO ESTIMACIÓN
# ============================================================

if st.session_state.modo_estimacion:

    st.write("")
    st.divider()

    st.caption(
        "INTI ENERGY LAB · SIMULACIÓN PRELIMINAR"
    )

    st.markdown(
        "## ☀️ Predimensionamiento solar"
    )

    st.markdown(
        "Realiza un **ejercicio teórico preliminar** "
        "para explorar cómo podría verse un sistema "
        "solar fotovoltaico según tu consumo."
    )

    st.warning(
        "⚠️ **ESTIMACIÓN TEÓRICA — NO OFICIAL**\n\n"
        "Este ejercicio no constituye una cotización oficial, "
        "oferta comercial, diseño de ingeniería ni compromiso "
        "contractual de INTILED. Los resultados requieren "
        "validación técnica y comercial."
    )

    st.write("")

    # ========================================================
    # FORMULARIO DE ESTIMACIÓN
    # ========================================================

    with st.form(
        "form_estimacion_solar"
    ):

        st.markdown(
            "### Cuéntame sobre tu proyecto"
        )

        st.caption(
            "Con estos datos INTI realizará un "
            "predimensionamiento matemático preliminar."
        )

        col1, col2 = st.columns(2)

        with col1:

            ubicacion = st.text_input(
                "📍 Ubicación del proyecto",
                value=st.session_state.datos_estimacion.get(
                    "ubicacion",
                    "Pasto"
                ),
                placeholder="Ejemplo: Pasto, Nariño",
            )

            consumo = st.number_input(
                "⚡ Consumo promedio mensual (kWh)",
                min_value=1.0,
                value=float(
                    st.session_state.datos_estimacion.get(
                        "consumo",
                        850.0
                    )
                ),
                step=10.0,
            )

        with col2:

            factura = st.number_input(
                "💵 Valor aproximado de factura mensual (COP)",
                min_value=0.0,
                value=float(
                    st.session_state.datos_estimacion.get(
                        "factura",
                        700000.0
                    )
                ),
                step=10000.0,
            )

            cobertura = st.slider(
                "🎯 Cobertura energética objetivo",
                min_value=10,
                max_value=100,
                value=int(
                    st.session_state.datos_estimacion.get(
                        "cobertura",
                        80
                    )
                ),
                step=5,
                format="%d%%",
            )

        st.write("")

        calcular = st.form_submit_button(
            "⚡ CALCULAR ESTIMACIÓN TEÓRICA",
            use_container_width=True,
        )


    # ========================================================
    # EJECUTAR CÁLCULO
    # ========================================================

    if calcular:

        try:

            st.session_state.datos_estimacion = {
                "ubicacion": ubicacion,
                "consumo": consumo,
                "factura": factura,
                "cobertura": cobertura,
            }

            resultado = calcular_sistema_fotovoltaico(
                consumo_mensual_kwh=consumo,
                valor_factura_cop=factura,
                ubicacion=ubicacion,
                porcentaje_cobertura=cobertura,
                hsp=4.5,
                performance_ratio=0.80,
                potencia_panel_w=580,
            )

            st.session_state.resultado_solar = resultado

            pdf = generar_pdf_fotovoltaico(
                resultado=resultado,
                nombre_interesado="Usuario INTI",
                proyecto=(
                    "Predimensionamiento preliminar "
                    "de sistema solar fotovoltaico"
                ),
            )

            st.session_state.pdf_solar = pdf

            resumen = generar_resumen_para_chat(
                resultado
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": resumen,
                }
            )

            st.rerun()

        except Exception as error:

            st.error(
                "No fue posible realizar la estimación. "
                f"Revisa los datos ingresados. Detalle: {error}"
            )


    # ========================================================
    # RESULTADOS
    # ========================================================

    resultado = st.session_state.resultado_solar

    if resultado is not None:

        st.write("")
        st.divider()

        st.caption(
            "RESULTADO · ESCENARIO TEÓRICO"
        )

        st.markdown(
            "## ⚡ Tu escenario energético"
        )

        st.success(
            "Cálculo completado correctamente. "
            "Recuerda que se trata de un ejercicio "
            "preliminar no oficial."
        )

        st.write("")

        m1, m2, m3, m4 = st.columns(4)

        with m1:

            st.metric(
                "Potencia estimada",
                f"{resultado.potencia_instalada_kwp:.2f} kWp",
            )

        with m2:

            st.metric(
                "Paneles estimados",
                f"{resultado.numero_paneles}",
            )

        with m3:

            st.metric(
                "Producción mensual",
                (
                    f"{resultado.produccion_estimada_kwh_mes:,.0f} "
                    "kWh"
                ),
            )

        with m4:

            st.metric(
                "Área recomendada",
                f"{resultado.area_recomendada_m2:.1f} m²",
            )

        st.write("")

        r1, r2, r3 = st.columns(3)

        with r1:

            st.metric(
                "Cobertura aproximada",
                (
                    f"{resultado.cobertura_estimada_porcentaje:.1f}%"
                ),
            )

        with r2:

            st.metric(
                "Producción anual",
                (
                    f"{resultado.produccion_estimada_kwh_anio:,.0f} "
                    "kWh"
                ),
            )

        with r3:

            if resultado.valor_factura_cop > 0:

                st.metric(
                    "Ahorro teórico mensual",
                    (
                        "$"
                        f"{resultado.ahorro_teorico_mensual_cop:,.0f}"
                        " COP"
                    ),
                )

            else:

                st.metric(
                    "Ahorro teórico",
                    "No calculado",
                )

        st.write("")

        st.info(
            f"""
**Supuestos utilizados**

☀️ Horas Sol Pico de referencia: **{resultado.hsp:.2f} h/día**

⚙️ Factor global de desempeño: **{resultado.performance_ratio * 100:.0f}%**

🔋 Potencia de módulo utilizada para el ejercicio: **{resultado.potencia_panel_w:.0f} W**

🎯 Cobertura objetivo seleccionada: **{resultado.porcentaje_cobertura_objetivo:.0f}%**

Estos parámetros corresponden a un ejercicio simplificado y
deben validarse para cada proyecto.
"""
        )

        # ====================================================
        # PDF
        # ====================================================

        if st.session_state.pdf_solar:

            st.write("")
            st.markdown(
                "### 📄 Informe de la simulación"
            )

            st.caption(
                "Descarga el resultado preliminar generado "
                "por INTI."
            )

            st.download_button(
                label="⬇️ DESCARGAR ESTIMACIÓN TEÓRICA EN PDF",
                data=st.session_state.pdf_solar,
                file_name=nombre_archivo_pdf(
                    resultado
                ),
                mime="application/pdf",
                use_container_width=True,
            )

        st.write("")

        st.warning(
            "Este resultado **NO corresponde a una cotización "
            "oficial de INTILED**. La selección definitiva de "
            "equipos, ingeniería, costos, condiciones de "
            "instalación y viabilidad deben ser revisados "
            "por profesionales autorizados."
        )

        st.markdown(
            "### ¿Quieres llevar este ejercicio a un proyecto real?"
        )

        st.write(
            "El siguiente paso recomendado es solicitar una "
            "revisión con el equipo técnico y comercial de INTILED."
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "👨‍💼 HABLAR CON EL EQUIPO",
                use_container_width=True,
                key="result_contact",
            ):

                cerrar_estimacion()

                procesar_mensaje(
                    "Ya realicé una estimación teórica de un "
                    "sistema solar con INTI y quiero comunicarme "
                    "con el equipo de INTILED para revisar "
                    "el proyecto."
                )

                st.rerun()

        with c2:

            if st.button(
                "↻ NUEVA ESTIMACIÓN",
                use_container_width=True,
                key="result_new",
            ):

                nueva_estimacion()
                st.rerun()


# ============================================================
# CHAT
# ============================================================

else:

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

            nueva_conversacion()
            st.rerun()

    st.write("")

    # ========================================================
    # MENSAJES
    # ========================================================

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

            avatar_chat = (
                AVATAR
                if avatar_ok
                else "⚡"
            )

        else:

            avatar_chat = "👤"

        with st.chat_message(
            role,
            avatar=avatar_chat,
        ):

            if role == "assistant":

                st.caption(
                    "INTI · INTILED"
                )

            st.markdown(
                content
            )

    # ========================================================
    # INPUT CHAT
    # ========================================================

    st.write("")

    with st.form(
        "inti_message_form",
        clear_on_submit=True,
    ):

        pregunta = st.text_input(
            "Mensaje",
            placeholder="Pregúntale algo a INTI...",
            label_visibility="collapsed",
        )

        enviar = st.form_submit_button(
            "➜ Enviar",
            use_container_width=True,
        )

    if enviar and pregunta.strip():

        procesar_mensaje(
            pregunta
        )

        st.rerun()

    st.caption(
        "INTI ofrece orientación inicial. Las decisiones "
        "técnicas, comerciales y contractuales son "
        "validadas por el equipo de INTILED."
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

        cerrar_estimacion()

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

        cerrar_estimacion()

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

        cerrar_estimacion()

        procesar_mensaje(
            "Quiero conocer las soluciones "
            "de infraestructura eléctrica "
            "de INTILED."
        )

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.divider()

year = datetime.now().year

footer1, footer2, footer3 = st.columns(
    [1.4, 1, 1.2],
    gap="large",
)

with footer1:

    st.markdown(
        "### INTILED S.A.S. BIC"
    )

    st.write(
        "Energía, tecnología y sostenibilidad "
        "para transformar proyectos en soluciones."
    )

with footer2:

    st.markdown(
        "### INTI"
    )

    st.write(
        "Asistente virtual inteligente para "
        "orientación inicial de proyectos."
    )

with footer3:

    st.markdown(
        "### Importante"
    )

    st.write(
        "Las estimaciones generadas por INTI "
        "son ejercicios preliminares no oficiales."
    )

st.caption(
    f"© {year} INTILED S.A.S. BIC · "
    "INTI — Intelligent Energy Experience ⚡"
)
