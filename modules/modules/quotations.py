"""
INTI - Motor de estimaciones teóricas
INTILED S.A.S. BIC

Este módulo realiza ejercicios teóricos de predimensionamiento.

IMPORTANTE:
Los resultados NO constituyen una cotización oficial, oferta comercial,
diseño de ingeniería, estudio técnico definitivo ni compromiso contractual
de INTILED S.A.S. BIC.
"""

from dataclasses import dataclass, asdict
from math import ceil
from datetime import datetime
import uuid


# ============================================================
# CONFIGURACIÓN
# ============================================================

VERSION_MOTOR = "1.0"

AVISO_LEGAL = (
    "EJERCICIO TEÓRICO - NO OFICIAL. "
    "Los resultados presentados son estimaciones preliminares con fines "
    "informativos y orientativos. No constituyen una cotización oficial, "
    "oferta comercial, diseño de ingeniería ni compromiso contractual de "
    "INTILED S.A.S. BIC. Todo proyecto debe ser validado posteriormente "
    "por el equipo técnico y comercial de INTILED."
)


# ============================================================
# MODELO DE RESULTADOS
# ============================================================

@dataclass
class ResultadoFotovoltaico:

    codigo: str
    fecha: str

    ubicacion: str

    consumo_mensual_kwh: float
    valor_factura_cop: float

    porcentaje_cobertura_objetivo: float

    hsp: float
    performance_ratio: float

    potencia_panel_w: float

    energia_objetivo_kwh_mes: float

    potencia_fv_teorica_kwp: float

    numero_paneles: int

    potencia_instalada_kwp: float

    produccion_estimada_kwh_mes: float
    produccion_estimada_kwh_anio: float

    cobertura_estimada_porcentaje: float

    area_panel_m2: float
    area_minima_paneles_m2: float
    area_recomendada_m2: float

    costo_energia_aprox_cop_kwh: float

    ahorro_teorico_mensual_cop: float
    ahorro_teorico_anual_cop: float

    aviso_legal: str

    def como_diccionario(self):
        return asdict(self)


# ============================================================
# UTILIDADES
# ============================================================

def generar_codigo_estimacion():

    fecha = datetime.now().strftime("%Y%m%d")

    identificador = (
        uuid.uuid4()
        .hex[:6]
        .upper()
    )

    return f"INTI-EST-{fecha}-{identificador}"


def _validar_numero(
    valor,
    nombre,
    minimo=0,
    permitir_cero=False
):

    try:
        numero = float(valor)

    except (TypeError, ValueError):

        raise ValueError(
            f"{nombre} debe ser un valor numérico."
        )

    if permitir_cero:

        if numero < minimo:

            raise ValueError(
                f"{nombre} no puede ser menor que {minimo}."
            )

    else:

        if numero <= minimo:

            raise ValueError(
                f"{nombre} debe ser mayor que {minimo}."
            )

    return numero


# ============================================================
# PREDIMENSIONAMIENTO FOTOVOLTAICO
# ============================================================

def calcular_sistema_fotovoltaico(
    consumo_mensual_kwh,
    valor_factura_cop=0,
    ubicacion="No especificada",
    porcentaje_cobertura=80,
    hsp=4.5,
    performance_ratio=0.80,
    potencia_panel_w=580,
    area_panel_m2=2.6,
    factor_area_instalacion=1.20
):
    """
    Realiza un ejercicio TEÓRICO de predimensionamiento
    de un sistema solar fotovoltaico.

    Parámetros
    ----------
    consumo_mensual_kwh:
        Consumo promedio mensual del usuario.

    valor_factura_cop:
        Valor aproximado de la factura mensual.

    ubicacion:
        Municipio o ubicación general del proyecto.

    porcentaje_cobertura:
        Porcentaje del consumo que se desea compensar.

    hsp:
        Horas Sol Pico de referencia.

    performance_ratio:
        Factor global simplificado de desempeño.

        Ejemplo:
        0.80 = 80 %

    potencia_panel_w:
        Potencia nominal teórica de cada módulo.

    area_panel_m2:
        Área aproximada ocupada por un módulo.

    factor_area_instalacion:
        Factor adicional para separaciones,
        mantenimiento y disposición.

    IMPORTANTE
    ----------
    Esto NO reemplaza:
    - visita técnica,
    - estudio de sombras,
    - diseño eléctrico,
    - análisis estructural,
    - estudio de conexión,
    - selección definitiva de equipos,
    - propuesta comercial.
    """

    # --------------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------------

    consumo = _validar_numero(
        consumo_mensual_kwh,
        "El consumo mensual"
    )

    factura = _validar_numero(
        valor_factura_cop,
        "El valor de la factura",
        minimo=0,
        permitir_cero=True
    )

    cobertura = _validar_numero(
        porcentaje_cobertura,
        "El porcentaje de cobertura"
    )

    if cobertura > 100:

        raise ValueError(
            "El porcentaje de cobertura no puede superar 100 %."
        )

    hsp = _validar_numero(
        hsp,
        "Las Horas Sol Pico"
    )

    pr = _validar_numero(
        performance_ratio,
        "El factor de desempeño"
    )

    if pr > 1:

        raise ValueError(
            "El performance ratio debe expresarse entre 0 y 1."
        )

    panel_w = _validar_numero(
        potencia_panel_w,
        "La potencia del panel"
    )

    area_panel = _validar_numero(
        area_panel_m2,
        "El área del panel"
    )

    factor_area = _validar_numero(
        factor_area_instalacion,
        "El factor de área"
    )


    # --------------------------------------------------------
    # 1. ENERGÍA OBJETIVO
    # --------------------------------------------------------

    energia_objetivo = (
        consumo
        * cobertura
        / 100
    )


    # --------------------------------------------------------
    # 2. POTENCIA FV TEÓRICA
    #
    # Energía mensual ≈
    # kWp × HSP × días × PR
    # --------------------------------------------------------

    potencia_fv_teorica = (
        energia_objetivo
        /
        (
            hsp
            * 30
            * pr
        )
    )


    # --------------------------------------------------------
    # 3. NÚMERO DE PANELES
    # --------------------------------------------------------

    potencia_panel_kw = (
        panel_w / 1000
    )

    numero_paneles = ceil(
        potencia_fv_teorica
        /
        potencia_panel_kw
    )


    # --------------------------------------------------------
    # 4. POTENCIA INSTALADA RESULTANTE
    # --------------------------------------------------------

    potencia_instalada = (
        numero_paneles
        * potencia_panel_kw
    )


    # --------------------------------------------------------
    # 5. PRODUCCIÓN ESTIMADA
    # --------------------------------------------------------

    produccion_mensual = (
        potencia_instalada
        * hsp
        * 30
        * pr
    )

    produccion_anual = (
        produccion_mensual
        * 12
    )


    # --------------------------------------------------------
    # 6. COBERTURA ESTIMADA
    # --------------------------------------------------------

    cobertura_estimada = (
        produccion_mensual
        /
        consumo
        * 100
    )

    cobertura_estimada = min(
        cobertura_estimada,
        100
    )


    # --------------------------------------------------------
    # 7. ÁREA
    # --------------------------------------------------------

    area_minima = (
        numero_paneles
        * area_panel
    )

    area_recomendada = (
        area_minima
        * factor_area
    )


    # --------------------------------------------------------
    # 8. COSTO PROMEDIO APROXIMADO DE ENERGÍA
    # --------------------------------------------------------

    if factura > 0:

        costo_energia = (
            factura
            /
            consumo
        )

    else:

        costo_energia = 0


    # --------------------------------------------------------
    # 9. AHORRO TEÓRICO
    #
    # No se presenta como ahorro garantizado.
    # --------------------------------------------------------

    energia_compensable = min(
        produccion_mensual,
        consumo
    )

    ahorro_mensual = (
        energia_compensable
        * costo_energia
    )

    ahorro_anual = (
        ahorro_mensual
        * 12
    )


    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    return ResultadoFotovoltaico(

        codigo=generar_codigo_estimacion(),

        fecha=datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        ),

        ubicacion=(
            ubicacion.strip()
            if ubicacion
            else "No especificada"
        ),

        consumo_mensual_kwh=round(
            consumo,
            2
        ),

        valor_factura_cop=round(
            factura,
            0
        ),

        porcentaje_cobertura_objetivo=round(
            cobertura,
            1
        ),

        hsp=round(
            hsp,
            2
        ),

        performance_ratio=round(
            pr,
            3
        ),

        potencia_panel_w=round(
            panel_w,
            0
        ),

        energia_objetivo_kwh_mes=round(
            energia_objetivo,
            2
        ),

        potencia_fv_teorica_kwp=round(
            potencia_fv_teorica,
            2
        ),

        numero_paneles=numero_paneles,

        potencia_instalada_kwp=round(
            potencia_instalada,
            2
        ),

        produccion_estimada_kwh_mes=round(
            produccion_mensual,
            2
        ),

        produccion_estimada_kwh_anio=round(
            produccion_anual,
            2
        ),

        cobertura_estimada_porcentaje=round(
            cobertura_estimada,
            1
        ),

        area_panel_m2=round(
            area_panel,
            2
        ),

        area_minima_paneles_m2=round(
            area_minima,
            2
        ),

        area_recomendada_m2=round(
            area_recomendada,
            2
        ),

        costo_energia_aprox_cop_kwh=round(
            costo_energia,
            2
        ),

        ahorro_teorico_mensual_cop=round(
            ahorro_mensual,
            0
        ),

        ahorro_teorico_anual_cop=round(
            ahorro_anual,
            0
        ),

        aviso_legal=AVISO_LEGAL
    )


# ============================================================
# RESUMEN PARA INTI
# ============================================================

def generar_resumen_para_chat(resultado):

    if isinstance(
        resultado,
        ResultadoFotovoltaico
    ):

        r = resultado

    elif isinstance(
        resultado,
        dict
    ):

        r = ResultadoFotovoltaico(
            **resultado
        )

    else:

        raise TypeError(
            "El resultado debe ser ResultadoFotovoltaico o dict."
        )


    texto = f"""
### ⚡ Estimación teórica preliminar

**IMPORTANTE: este resultado NO es una cotización oficial de INTILED.**

Con los datos suministrados, el ejercicio teórico arroja aproximadamente:

- **Consumo:** {r.consumo_mensual_kwh:,.0f} kWh/mes
- **Cobertura objetivo:** {r.porcentaje_cobertura_objetivo:.0f} %
- **Potencia FV teórica:** {r.potencia_fv_teorica_kwp:.2f} kWp
- **Paneles estimados:** {r.numero_paneles} módulos de {r.potencia_panel_w:,.0f} W
- **Potencia instalada resultante:** {r.potencia_instalada_kwp:.2f} kWp
- **Producción aproximada:** {r.produccion_estimada_kwh_mes:,.0f} kWh/mes
- **Cobertura aproximada:** {r.cobertura_estimada_porcentaje:.1f} %
- **Área recomendada de referencia:** {r.area_recomendada_m2:.1f} m²

Los resultados dependen de supuestos simplificados y deben validarse mediante una revisión técnica del sitio.

**INTI estima. INTILED valida y cotiza.**
"""

    return texto.strip()