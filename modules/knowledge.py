"""
============================================================
INTI - BASE DE CONOCIMIENTO INSTITUCIONAL
INTILED S.A.S. BIC
============================================================

Este módulo contiene información institucional verificada
que INTI puede utilizar para responder consultas.

Fuente principal:
Sitio web oficial de INTILED S.A.S. BIC.

IMPORTANTE:
- No contiene claves API.
- No ejecuta Gemini.
- No registra usuarios.
- No realiza cotizaciones automáticamente.
- No agenda citas automáticamente.
- No radica PQR/PQRS.

Versión: 1.0
============================================================
"""


# ============================================================
# INFORMACIÓN GENERAL
# ============================================================

EMPRESA = {
    "nombre": "INTILED S.A.S. BIC",
    "nombre_corto": "INTILED",

    "descripcion": (
        "INTILED S.A.S. BIC es una empresa orientada al desarrollo "
        "de soluciones energéticas sostenibles, eficiencia energética, "
        "sistemas solares fotovoltaicos, infraestructura eléctrica "
        "y servicios técnicos especializados."
    ),

    "enfoque": (
        "La empresa desarrolla soluciones relacionadas con eficiencia "
        "energética, sostenibilidad, energía solar e infraestructura "
        "eléctrica."
    ),

    "ciudad": "Pasto",

    "departamento": "Nariño",

    "pais": "Colombia",

    "sitio_web": "https://intiled.com.co/"
}


# ============================================================
# INFORMACIÓN DE CONTACTO
# ============================================================

CONTACTO = {

    "direccion": (
        "Calle 11 #36-46, La Castellana, "
        "Pasto, Colombia"
    ),

    "telefono_1": "+57 602 733 7893",

    "telefono_2": "+57 304 670 2584",

    "correo_comercial": "comercial@intiled.com.co",

    "horario_semana": (
        "Lunes a viernes de 8:00 a. m. a 6:00 p. m."
    ),

    "horario_sabado": (
        "Sábados de 8:00 a. m. a 12:00 p. m."
    )
}


# ============================================================
# SERVICIOS
# ============================================================

SERVICIOS = {

    "programa_ure": {

        "nombre": "Programa URE",

        "descripcion": (
            "Diagnóstico técnico especializado orientado a evaluar "
            "el estado real de una instalación eléctrica, identificar "
            "pérdidas de energía, riesgos eléctricos y oportunidades "
            "de mejora en eficiencia energética."
        ),

        "objetivo": (
            "Ayudar al cliente a reducir costos, mejorar la seguridad "
            "eléctrica y optimizar el consumo de energía."
        )
    },


    "redes_electricas": {

        "nombre": (
            "Diseño y construcción de redes eléctricas"
        ),

        "descripcion": (
            "INTILED desarrolla soluciones para infraestructura "
            "eléctrica, incluyendo redes de baja tensión, media "
            "tensión, transformación y subestaciones."
        ),

        "componentes": [
            "Redes de baja tensión",
            "Redes de media tensión",
            "Transformación",
            "Subestaciones eléctricas"
        ]
    },


    "consultoria_fncer": {

        "nombre": (
            "Consultoría para proyectos de Fuentes No "
            "Convencionales de Energía Renovable - FNCER"
        ),

        "descripcion": (
            "Consultoría especializada para la estructuración "
            "y desarrollo de proyectos relacionados con fuentes "
            "no convencionales de energía renovable."
        )
    },


    "sistemas_fotovoltaicos": {

        "nombre": (
            "Diseño y construcción de sistemas fotovoltaicos"
        ),

        "descripcion": (
            "INTILED desarrolla soluciones de generación de energía "
            "solar fotovoltaica adaptadas a las necesidades "
            "energéticas de cada proyecto."
        ),

        "tipos": {

            "on_grid": (
                "Sistemas conectados a la red eléctrica que permiten "
                "generar energía solar para reducir el consumo de "
                "energía proveniente de la red."
            ),

            "off_grid": (
                "Sistemas autónomos para lugares donde no existe "
                "acceso a la red eléctrica o donde se requiere "
                "independencia energética."
            ),

            "hibridos": (
                "Sistemas que combinan diferentes fuentes de energía "
                "y tecnologías de almacenamiento o respaldo."
            )
        }
    },


    "calefaccion_piscinas": {

        "nombre": (
            "Calefacción de piscinas con bomba de calor"
        ),

        "descripcion": (
            "Soluciones para calentamiento eficiente de piscinas "
            "mediante tecnología de bomba de calor."
        )
    },


    "equipos_solares": {

        "nombre": (
            "Suministro de equipos y materiales "
            "para sistemas solares"
        ),

        "descripcion": (
            "Suministro de equipos y materiales destinados "
            "a proyectos de energía solar, con acompañamiento "
            "y respaldo técnico."
        )
    }
}


# ============================================================
# PROGRAMA URE
# ============================================================

PROGRAMA_URE = {

    "nombre": "Programa URE",

    "tipo": "Diagnóstico Técnico Especializado",

    "descripcion": (
        "El Programa URE realiza una evaluación técnica de una "
        "instalación eléctrica utilizando equipos de medición "
        "profesionales y metodologías de inspección."
    ),

    "duracion_aproximada": "4 horas",

    "valor_publicado": "$199.000 COP",

    "forma_pago_publicada": "Pago en 2 cuotas",

    "evaluaciones": [

        "Estado general de la instalación eléctrica",

        "Tableros eléctricos y sistemas de protección",

        "Circuitos de iluminación",

        "Tomacorrientes",

        "Conductores y conexiones",

        "Balance de cargas",

        "Equipos de alto consumo",

        "Consumos ocultos o energía fantasma",

        "Fugas de corriente",

        "Calidad del suministro eléctrico",

        "Riesgos de sobrecarga",

        "Riesgos de fallas eléctricas",

        "Necesidades de mantenimiento preventivo"

    ],

    "entregables": [

        "Diagnóstico detallado de la instalación",

        "Registro fotográfico de hallazgos",

        "Identificación de riesgos eléctricos",

        "Análisis de oportunidades de ahorro",

        "Recomendaciones priorizadas",

        "Plan de mantenimiento preventivo",

        "Estrategia para optimizar el consumo energético"
    ],

    "beneficios": [

        "Identificación de oportunidades de ahorro energético",

        "Mejora de la seguridad eléctrica",

        "Prevención de fallas",

        "Mayor vida útil de equipos eléctricos",

        "Reducción potencial de costos de mantenimiento",

        "Preparación de la instalación para incorporar "
        "energías renovables"
    ],

    "ahorro_potencial": (
        "Según la información publicada por INTILED, la "
        "implementación de las recomendaciones puede permitir "
        "reducciones de consumo de hasta un 30 %, dependiendo "
        "del estado de la instalación, los equipos utilizados "
        "y las mejoras ejecutadas."
    ),

    "dirigido_a": [

        "Viviendas",

        "Conjuntos residenciales",

        "Oficinas",

        "Locales comerciales",

        "Restaurantes",

        "Hoteles",

        "Clínicas",

        "Instituciones educativas",

        "Empresas",

        "Industrias"
    ]
}


# ============================================================
# SISTEMAS SOLARES
# ============================================================

SISTEMAS_SOLARES = {

    "on_grid": {

        "nombre": "Sistema Solar On-Grid",

        "descripcion": (
            "Sistema fotovoltaico conectado a la red eléctrica. "
            "Permite generar energía solar para reducir el consumo "
            "proveniente de la red."
        ),

        "aplicaciones": [
            "Residencias",
            "Empresas",
            "Comercios",
            "Instituciones"
        ]
    },


    "off_grid": {

        "nombre": "Sistema Solar Off-Grid",

        "descripcion": (
            "Sistema fotovoltaico independiente de la red eléctrica. "
            "Puede utilizar paneles solares, baterías e inversores "
            "para suministrar energía en lugares aislados."
        ),

        "aplicaciones": [
            "Zonas rurales",
            "Fincas",
            "Viviendas aisladas",
            "Lugares sin acceso a red eléctrica"
        ]
    },


    "hibrido": {

        "nombre": "Sistema Solar Híbrido",

        "descripcion": (
            "Sistema que combina generación solar con otras "
            "fuentes de energía, almacenamiento o respaldo "
            "para aumentar la disponibilidad energética."
        )
    }
}


# ============================================================
# PRINCIPIOS DE SERVICIO
# ============================================================

PRINCIPIOS = [

    "Experiencia técnica",

    "Innovación",

    "Eficiencia energética",

    "Sostenibilidad",

    "Acompañamiento integral",

    "Soporte técnico"

]


# ============================================================
# REGLAS DE USO DEL CONOCIMIENTO
# ============================================================

REGLAS_CONOCIMIENTO = """

REGLAS PARA INTI:

1. Utiliza esta información únicamente cuando sea relevante
   para la consulta del usuario.

2. No inventes servicios que no estén registrados en la
   base de conocimiento.

3. No inventes proyectos ejecutados por INTILED.

4. No inventes clientes de INTILED.

5. No inventes contratos.

6. No inventes certificaciones.

7. No inventes precios.

8. El único precio que actualmente puede mencionarse desde
   esta base es el valor publicado del Programa URE.

9. Cuando menciones el precio del Programa URE, indica que
   corresponde al valor publicado actualmente y que debe
   confirmarse con INTILED antes de contratar.

10. No garantices porcentajes de ahorro.

11. Si mencionas el ahorro potencial del Programa URE,
    explica que depende de las condiciones particulares
    de cada instalación.

12. Si una consulta requiere ingeniería de detalle,
    recomienda evaluación por profesionales de INTILED.

13. No confirmes citas automáticamente.

14. No confirmes cotizaciones automáticamente.

15. No confirmes PQR/PQRS automáticamente.

16. Si el usuario quiere contratar un servicio, puedes
    orientarlo y recopilar progresivamente la información
    necesaria para que un asesor continúe el proceso.

17. Si la información solicitada no está disponible,
    dilo claramente en lugar de inventarla.

"""


# ============================================================
# CONSTRUCCIÓN DEL CONTEXTO PARA GEMINI
# ============================================================

def obtener_contexto_intiled():
    """
    Construye el contexto institucional que puede enviarse
    al modelo de inteligencia artificial.
    """

    contexto = f"""

============================================================
INFORMACIÓN OFICIAL DISPONIBLE DE INTILED
============================================================

EMPRESA
Nombre:
{EMPRESA["nombre"]}

Descripción:
{EMPRESA["descripcion"]}

Enfoque:
{EMPRESA["enfoque"]}

Ubicación:
{EMPRESA["ciudad"]}, {EMPRESA["departamento"]}, {EMPRESA["pais"]}

Sitio web:
{EMPRESA["sitio_web"]}


------------------------------------------------------------
SERVICIOS
------------------------------------------------------------

1. {SERVICIOS["programa_ure"]["nombre"]}
{SERVICIOS["programa_ure"]["descripcion"]}

2. {SERVICIOS["redes_electricas"]["nombre"]}
{SERVICIOS["redes_electricas"]["descripcion"]}

3. {SERVICIOS["consultoria_fncer"]["nombre"]}
{SERVICIOS["consultoria_fncer"]["descripcion"]}

4. {SERVICIOS["sistemas_fotovoltaicos"]["nombre"]}
{SERVICIOS["sistemas_fotovoltaicos"]["descripcion"]}

Tipos:
- On-Grid
- Off-Grid
- Híbridos

5. {SERVICIOS["calefaccion_piscinas"]["nombre"]}
{SERVICIOS["calefaccion_piscinas"]["descripcion"]}

6. {SERVICIOS["equipos_solares"]["nombre"]}
{SERVICIOS["equipos_solares"]["descripcion"]}


------------------------------------------------------------
PROGRAMA URE
------------------------------------------------------------

Tipo:
{PROGRAMA_URE["tipo"]}

Descripción:
{PROGRAMA_URE["descripcion"]}

Duración aproximada:
{PROGRAMA_URE["duracion_aproximada"]}

Valor publicado:
{PROGRAMA_URE["valor_publicado"]}

Forma de pago publicada:
{PROGRAMA_URE["forma_pago_publicada"]}

Ahorro potencial:
{PROGRAMA_URE["ahorro_potencial"]}


------------------------------------------------------------
SISTEMAS SOLARES
------------------------------------------------------------

ON-GRID:
{SISTEMAS_SOLARES["on_grid"]["descripcion"]}

OFF-GRID:
{SISTEMAS_SOLARES["off_grid"]["descripcion"]}

HÍBRIDOS:
{SISTEMAS_SOLARES["hibrido"]["descripcion"]}


------------------------------------------------------------
CONTACTO
------------------------------------------------------------

Dirección:
{CONTACTO["direccion"]}

Teléfono:
{CONTACTO["telefono_1"]}

Celular:
{CONTACTO["telefono_2"]}

Correo comercial:
{CONTACTO["correo_comercial"]}

Horario:
{CONTACTO["horario_semana"]}
{CONTACTO["horario_sabado"]}


------------------------------------------------------------
REGLAS
------------------------------------------------------------

{REGLAS_CONOCIMIENTO}

============================================================
FIN DE INFORMACIÓN INSTITUCIONAL
============================================================
"""

    return contexto


# ============================================================
# BÚSQUEDA BÁSICA DE CONOCIMIENTO
# ============================================================

def buscar_conocimiento(consulta):
    """
    Identifica bloques de información relevantes según
    palabras presentes en la consulta.

    Posteriormente esta función podrá ser sustituida por
    búsqueda semántica/RAG.
    """

    consulta = consulta.lower()

    resultados = []


    # Programa URE

    if any(
        palabra in consulta
        for palabra in [
            "ure",
            "ahorro",
            "consumo",
            "eficiencia",
            "diagnóstico",
            "diagnostico",
            "auditoría",
            "auditoria"
        ]
    ):

        resultados.append(
            str(PROGRAMA_URE)
        )


    # Solar

    if any(
        palabra in consulta
        for palabra in [
            "solar",
            "fotovoltaico",
            "fotovoltaica",
            "panel",
            "paneles",
            "on grid",
            "on-grid",
            "off grid",
            "off-grid",
            "híbrido",
            "hibrido"
        ]
    ):

        resultados.append(
            str(SISTEMAS_SOLARES)
        )


    # Redes eléctricas

    if any(
        palabra in consulta
        for palabra in [
            "red eléctrica",
            "red electrica",
            "media tensión",
            "media tension",
            "baja tensión",
            "baja tension",
            "subestación",
            "subestacion",
            "transformador"
        ]
    ):

        resultados.append(
            str(
                SERVICIOS["redes_electricas"]
            )
        )


    # Contacto

    if any(
        palabra in consulta
        for palabra in [
            "contacto",
            "teléfono",
            "telefono",
            "celular",
            "correo",
            "email",
            "dirección",
            "direccion",
            "ubicación",
            "ubicacion",
            "horario",
            "dónde",
            "donde"
        ]
    ):

        resultados.append(
            str(CONTACTO)
        )


    # Servicios generales

    if any(
        palabra in consulta
        for palabra in [
            "servicio",
            "servicios",
            "qué hacen",
            "que hacen",
            "qué ofrece",
            "que ofrece",
            "intiled",
            "empresa"
        ]
    ):

        resultados.append(
            str(SERVICIOS)
        )


    # Si no encuentra coincidencias,
    # devuelve contexto institucional general.

    if not resultados:

        return obtener_contexto_intiled()


    return "\n\n".join(resultados)
