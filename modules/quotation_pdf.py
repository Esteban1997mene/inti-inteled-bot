"""
INTI - Generador de informe PDF
INTILED S.A.S. BIC

Genera un documento informativo correspondiente a un
EJERCICIO TEÓRICO DE PREDIMENSIONAMIENTO.

NO genera cotizaciones oficiales.
"""

from io import BytesIO
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
)

from modules.quotations import (
    ResultadoFotovoltaico,
    AVISO_LEGAL,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

LOGO_PATH = Path(
    "assets/logo_intiled.png"
)

ORANGE = colors.HexColor(
    "#FF6500"
)

ORANGE_LIGHT = colors.HexColor(
    "#FFF2E8"
)

DARK = colors.HexColor(
    "#111827"
)

GRAY = colors.HexColor(
    "#667085"
)

LIGHT_GRAY = colors.HexColor(
    "#F4F6F8"
)

BORDER = colors.HexColor(
    "#E4E7EC"
)

GREEN = colors.HexColor(
    "#147A42"
)


# ============================================================
# FORMATO
# ============================================================

def moneda(valor):

    try:

        return (
            "$"
            + f"{float(valor):,.0f}"
            .replace(",", ".")
            + " COP"
        )

    except (TypeError, ValueError):

        return "$0 COP"


def numero(valor, decimales=1):

    try:

        texto = (
            f"{float(valor):,.{decimales}f}"
        )

        texto = (
            texto
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        return texto

    except (TypeError, ValueError):

        return "0"


# ============================================================
# FOOTER
# ============================================================

def _dibujar_footer(
    canvas,
    doc
):

    canvas.saveState()

    ancho, _ = A4

    canvas.setStrokeColor(
        BORDER
    )

    canvas.line(
        18 * mm,
        15 * mm,
        ancho - 18 * mm,
        15 * mm,
    )

    canvas.setFont(
        "Helvetica",
        7.5,
    )

    canvas.setFillColor(
        GRAY
    )

    canvas.drawString(
        18 * mm,
        10 * mm,
        (
            "Documento generado automáticamente por INTI. "
            "Ejercicio teórico sin validez comercial, "
            "contractual ni de ingeniería."
        ),
    )

    canvas.drawRightString(
        ancho - 18 * mm,
        10 * mm,
        f"Página {doc.page}",
    )

    canvas.restoreState()


# ============================================================
# PDF
# ============================================================

def generar_pdf_fotovoltaico(
    resultado,
    nombre_interesado="Usuario INTI",
    proyecto="Sistema Solar Fotovoltaico",
    observaciones="",
    asesor=None,
):
    """
    Genera un PDF en memoria.

    Retorna:
        bytes

    asesor puede ser:

    {
        "nombre": "...",
        "cargo": "...",
        "telefono": "...",
        "correo": "..."
    }

    IMPORTANTE:
    Los datos del asesor deben corresponder a información
    autorizada por INTILED.
    """

    # --------------------------------------------------------
    # CONVERSIÓN DEL RESULTADO
    # --------------------------------------------------------

    if isinstance(
        resultado,
        dict
    ):

        resultado = ResultadoFotovoltaico(
            **resultado
        )

    if not isinstance(
        resultado,
        ResultadoFotovoltaico
    ):

        raise TypeError(
            "resultado debe ser ResultadoFotovoltaico o dict."
        )


    # --------------------------------------------------------
    # BUFFER
    # --------------------------------------------------------

    buffer = BytesIO()


    # --------------------------------------------------------
    # DOCUMENTO
    # --------------------------------------------------------

    doc = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=18 * mm,
        leftMargin=18 * mm,

        topMargin=16 * mm,
        bottomMargin=23 * mm,

        title=(
            "Estimación Teórica Preliminar - INTILED"
        ),

        author=(
            "INTI - INTILED S.A.S. BIC"
        ),
    )


    # --------------------------------------------------------
    # ESTILOS
    # --------------------------------------------------------

    styles = getSampleStyleSheet()


    titulo = ParagraphStyle(

        "TituloINTI",

        parent=styles["Title"],

        fontName="Helvetica-Bold",

        fontSize=20,

        leading=24,

        textColor=DARK,

        alignment=TA_LEFT,

        spaceAfter=4,
    )


    subtitulo = ParagraphStyle(

        "SubtituloINTI",

        parent=styles["Normal"],

        fontName="Helvetica-Bold",

        fontSize=11,

        leading=15,

        textColor=ORANGE,

        alignment=TA_LEFT,

        spaceAfter=6,
    )


    encabezado = ParagraphStyle(

        "EncabezadoINTI",

        parent=styles["Heading2"],

        fontName="Helvetica-Bold",

        fontSize=12,

        leading=15,

        textColor=DARK,

        spaceBefore=10,

        spaceAfter=8,
    )


    normal = ParagraphStyle(

        "NormalINTI",

        parent=styles["Normal"],

        fontName="Helvetica",

        fontSize=9.5,

        leading=14,

        textColor=DARK,

        alignment=TA_LEFT,
    )


    pequeno = ParagraphStyle(

        "PequenoINTI",

        parent=normal,

        fontSize=8,

        leading=11,

        textColor=GRAY,
    )


    alerta = ParagraphStyle(

        "AlertaINTI",

        parent=normal,

        fontName="Helvetica-Bold",

        fontSize=9,

        leading=13,

        textColor=colors.HexColor(
            "#9A3412"
        ),
    )


    # --------------------------------------------------------
    # CONTENIDO
    # --------------------------------------------------------

    story = []


    # ========================================================
    # LOGO
    # ========================================================

    if LOGO_PATH.exists():

        try:

            logo = Image(
                str(LOGO_PATH),
                width=43 * mm,
                height=22 * mm,
                kind="proportional",
            )

            logo.hAlign = "LEFT"

            story.append(
                logo
            )

            story.append(
                Spacer(
                    1,
                    3 * mm
                )
            )

        except Exception:

            pass


    # ========================================================
    # TÍTULO
    # ========================================================

    story.append(

        Paragraph(
            "EJERCICIO TEÓRICO DE PREDIMENSIONAMIENTO",
            titulo,
        )
    )


    story.append(

        Paragraph(
            "Sistema Solar Fotovoltaico",
            subtitulo,
        )
    )


    # ========================================================
    # AVISO PRINCIPAL
    # ========================================================

    aviso_tabla = Table(

        [
            [
                Paragraph(
                    (
                        "<b>DOCUMENTO INFORMATIVO — "
                        "NO ES UNA COTIZACIÓN OFICIAL</b><br/>"
                        "Este documento corresponde exclusivamente "
                        "a un ejercicio teórico generado con apoyo "
                        "de INTI."
                    ),
                    alerta,
                )
            ]
        ],

        colWidths=[
            174 * mm
        ],
    )


    aviso_tabla.setStyle(

        TableStyle(
            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    ORANGE_LIGHT,
                ),

                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    ORANGE,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ]
        )
    )


    story.append(
        aviso_tabla
    )

    story.append(
        Spacer(
            1,
            6 * mm
        )
    )


    # ========================================================
    # INFORMACIÓN GENERAL
    # ========================================================

    story.append(

        Paragraph(
            "1. Información general",
            encabezado,
        )
    )


    informacion = [

        [
            "Código de referencia",
            resultado.codigo,
        ],

        [
            "Fecha",
            resultado.fecha,
        ],

        [
            "Interesado",
            nombre_interesado,
        ],

        [
            "Proyecto",
            proyecto,
        ],

        [
            "Ubicación",
            resultado.ubicacion,
        ],
    ]


    tabla_info = Table(

        informacion,

        colWidths=[
            55 * mm,
            119 * mm,
        ],
    )


    tabla_info.setStyle(

        TableStyle(
            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    LIGHT_GRAY,
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    DARK,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),

                (
                    "FONTNAME",
                    (1, 0),
                    (1, -1),
                    "Helvetica",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    .5,
                    BORDER,
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )


    story.append(
        tabla_info
    )


    # ========================================================
    # DATOS SUMINISTRADOS
    # ========================================================

    story.append(

        Paragraph(
            "2. Datos utilizados para el ejercicio",
            encabezado,
        )
    )


    datos = [

        [
            "Variable",
            "Valor",
        ],

        [
            "Consumo promedio mensual",
            (
                f"{numero(resultado.consumo_mensual_kwh, 0)} "
                "kWh/mes"
            ),
        ],

        [
            "Valor aproximado de factura",
            moneda(
                resultado.valor_factura_cop
            ),
        ],

        [
            "Cobertura energética objetivo",
            (
                f"{numero(resultado.porcentaje_cobertura_objetivo, 1)} %"
            ),
        ],

        [
            "Horas Sol Pico de referencia",
            (
                f"{numero(resultado.hsp, 2)} h/día"
            ),
        ],

        [
            "Factor de desempeño teórico",
            (
                f"{numero(resultado.performance_ratio * 100, 0)} %"
            ),
        ],

        [
            "Potencia teórica del módulo",
            (
                f"{numero(resultado.potencia_panel_w, 0)} W"
            ),
        ],
    ]


    tabla_datos = Table(

        datos,

        colWidths=[
            100 * mm,
            74 * mm,
        ],

        repeatRows=1,
    )


    tabla_datos.setStyle(

        TableStyle(
            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    DARK,
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    .5,
                    BORDER,
                ),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        LIGHT_GRAY,
                    ],
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )


    story.append(
        tabla_datos
    )


    # ========================================================
    # RESULTADOS
    # ========================================================

    story.append(

        Paragraph(
            "3. Resultado del predimensionamiento teórico",
            encabezado,
        )
    )


    resultados = [

        [
            "Resultado",
            "Estimación",
        ],

        [
            "Energía objetivo",
            (
                f"{numero(resultado.energia_objetivo_kwh_mes, 0)} "
                "kWh/mes"
            ),
        ],

        [
            "Potencia FV teórica requerida",
            (
                f"{numero(resultado.potencia_fv_teorica_kwp, 2)} "
                "kWp"
            ),
        ],

        [
            "Número teórico de módulos",
            (
                f"{resultado.numero_paneles} paneles"
            ),
        ],

        [
            "Potencia instalada resultante",
            (
                f"{numero(resultado.potencia_instalada_kwp, 2)} "
                "kWp"
            ),
        ],

        [
            "Producción mensual aproximada",
            (
                f"{numero(resultado.produccion_estimada_kwh_mes, 0)} "
                "kWh/mes"
            ),
        ],

        [
            "Producción anual aproximada",
            (
                f"{numero(resultado.produccion_estimada_kwh_anio, 0)} "
                "kWh/año"
            ),
        ],

        [
            "Cobertura energética aproximada",
            (
                f"{numero(resultado.cobertura_estimada_porcentaje, 1)} %"
            ),
        ],

        [
            "Área mínima aproximada de módulos",
            (
                f"{numero(resultado.area_minima_paneles_m2, 1)} m²"
            ),
        ],

        [
            "Área de referencia recomendada",
            (
                f"{numero(resultado.area_recomendada_m2, 1)} m²"
            ),
        ],
    ]


    tabla_resultados = Table(

        resultados,

        colWidths=[
            105 * mm,
            69 * mm,
        ],

        repeatRows=1,
    )


    tabla_resultados.setStyle(

        TableStyle(
            [

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    ORANGE,
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),

                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    .5,
                    BORDER,
                ),

                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        LIGHT_GRAY,
                    ],
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )


    story.append(
        tabla_resultados
    )


    # ========================================================
    # ESTIMACIÓN DE AHORRO
    # ========================================================

    if resultado.valor_factura_cop > 0:

        story.append(

            Paragraph(
                "4. Referencia económica teórica",
                encabezado,
            )
        )


        story.append(

            Paragraph(
                (
                    "A partir del valor de factura informado por "
                    "el usuario se obtiene únicamente una referencia "
                    "matemática simplificada. Este cálculo no considera "
                    "todos los componentes tarifarios, impuestos, "
                    "excedentes, variaciones de consumo, regulación "
                    "aplicable ni condiciones contractuales."
                ),
                normal,
            )
        )


        story.append(
            Spacer(
                1,
                3 * mm
            )
        )


        economia = [

            [
                "Costo unitario aproximado",
                (
                    f"{moneda(resultado.costo_energia_aprox_cop_kwh)}"
                    "/kWh"
                ),
            ],

            [
                "Ahorro teórico mensual",
                moneda(
                    resultado.ahorro_teorico_mensual_cop
                ),
            ],

            [
                "Ahorro teórico anual",
                moneda(
                    resultado.ahorro_teorico_anual_cop
                ),
            ],
        ]


        tabla_economia = Table(

            economia,

            colWidths=[
                100 * mm,
                74 * mm,
            ],
        )


        tabla_economia.setStyle(

            TableStyle(
                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        LIGHT_GRAY,
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold",
                    ),

                    (
                        "FONTNAME",
                        (1, 0),
                        (1, -1),
                        "Helvetica",
                    ),

                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        .5,
                        BORDER,
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                ]
            )
        )


        story.append(
            tabla_economia
        )


    # ========================================================
    # SUPUESTOS
    # ========================================================

    story.append(

        Paragraph(
            "5. Alcance y supuestos",
            encabezado,
        )
    )


    supuestos = """
    Este ejercicio utiliza un modelo simplificado basado en consumo
    energético, Horas Sol Pico, potencia nominal de módulos y un factor
    global de desempeño. No contempla de manera definitiva orientación
    e inclinación del sistema, sombras, temperatura real de operación,
    degradación, restricciones estructurales, disponibilidad de área,
    protecciones, inversores, conductores, transformadores, obras civiles,
    condiciones de conexión, regulación aplicable ni disponibilidad
    comercial de equipos.
    """


    story.append(

        Paragraph(
            supuestos,
            normal,
        )
    )


    # ========================================================
    # OBSERVACIONES
    # ========================================================

    if observaciones:

        story.append(

            Paragraph(
                "6. Observaciones",
                encabezado,
            )
        )


        story.append(

            Paragraph(
                observaciones,
                normal,
            )
        )


    # ========================================================
    # ASESOR
    # ========================================================

    if asesor:

        story.append(

            Paragraph(
                "Siguiente paso",
                encabezado,
            )
        )


        nombre = asesor.get(
            "nombre",
            "Asesor INTILED",
        )

        cargo = asesor.get(
            "cargo",
            "Asesor comercial",
        )

        telefono = asesor.get(
            "telefono",
            "",
        )

        correo = asesor.get(
            "correo",
            "",
        )


        contacto_texto = (
            "<b>Para obtener una cotización oficial y validar "
            "técnicamente el proyecto, comunícate con:</b><br/><br/>"
            f"<b>{nombre}</b><br/>"
            f"{cargo}<br/>"
        )


        if telefono:

            contacto_texto += (
                f"Teléfono: {telefono}<br/>"
            )


        if correo:

            contacto_texto += (
                f"Correo: {correo}<br/>"
            )


        contacto_texto += (
            "<br/><b>INTILED S.A.S. BIC</b>"
        )


        caja_contacto = Table(

            [
                [
                    Paragraph(
                        contacto_texto,
                        normal,
                    )
                ]
            ],

            colWidths=[
                174 * mm
            ],
        )


        caja_contacto.setStyle(

            TableStyle(
                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, -1),
                        colors.HexColor(
                            "#F0FDF4"
                        ),
                    ),

                    (
                        "BOX",
                        (0, 0),
                        (-1, -1),
                        1,
                        GREEN,
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        10,
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                ]
            )
        )


        story.append(
            caja_contacto
        )


    # ========================================================
    # AVISO LEGAL FINAL
    # ========================================================

    story.append(
        Spacer(
            1,
            7 * mm
        )
    )


    story.append(

        Paragraph(
            "AVISO IMPORTANTE",
            subtitulo,
        )
    )


    story.append(

        Paragraph(
            AVISO_LEGAL,
            pequeno,
        )
    )


    story.append(
        Spacer(
            1,
            3 * mm
        )
    )


    story.append(

        Paragraph(
            (
                "<b>INTI estima. INTILED valida y cotiza.</b>"
            ),
            normal,
        )
    )


    # ========================================================
    # CONSTRUCCIÓN
    # ========================================================

    doc.build(

        story,

        onFirstPage=_dibujar_footer,

        onLaterPages=_dibujar_footer,
    )


    pdf = buffer.getvalue()

    buffer.close()

    return pdf


# ============================================================
# NOMBRE DEL ARCHIVO
# ============================================================

def nombre_archivo_pdf(
    resultado
):

    if isinstance(
        resultado,
        dict
    ):

        codigo = resultado.get(
            "codigo",
            "INTI-EST"
        )

    else:

        codigo = getattr(
            resultado,
            "codigo",
            "INTI-EST"
        )


    codigo = (
        str(codigo)
        .replace("/", "-")
        .replace("\\", "-")
        .replace(" ", "-")
    )


    return (
        f"{codigo}_estimacion_teorica_INTILED.pdf"
    )
