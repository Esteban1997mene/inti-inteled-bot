"""
INTI - Gestión de Solicitudes de Reunión
INTILED S.A.S. BIC
Versión 1.0

Este módulo administra las solicitudes de reunión generadas
desde INTI.

IMPORTANTE:
- Crear una solicitud NO significa que la reunión esté confirmada.
- La fecha y hora propuestas por el usuario son tentativas.
- La confirmación debe realizarla un funcionario autorizado de INTILED.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import uuid


# ============================================================
# ESTADOS DE UNA SOLICITUD
# ============================================================

ESTADO_SOLICITADA = "SOLICITADA"
ESTADO_ENVIADA = "ENVIADA_AL_FUNCIONARIO"
ESTADO_CONFIRMADA = "CONFIRMADA"
ESTADO_REPROGRAMACION = "REPROGRAMACION_PROPUESTA"
ESTADO_RECHAZADA = "RECHAZADA"
ESTADO_CANCELADA = "CANCELADA"


# ============================================================
# MODELO DE SOLICITUD
# ============================================================

@dataclass
class SolicitudReunion:
    """
    Representa una solicitud de reunión realizada desde INTI.

    La creación de este objeto NO confirma automáticamente
    una reunión.
    """

    codigo: str

    nombre: str
    correo: str

    motivo: str

    fecha_propuesta: str
    hora_propuesta: str

    telefono: Optional[str] = None
    empresa: Optional[str] = None

    funcionario: Optional[str] = None
    correo_funcionario: Optional[str] = None

    estado: str = ESTADO_SOLICITADA

    fecha_creacion: Optional[str] = None
    fecha_actualizacion: Optional[str] = None

    fecha_confirmada: Optional[str] = None
    hora_confirmada: Optional[str] = None

    fecha_alternativa: Optional[str] = None
    hora_alternativa: Optional[str] = None

    observaciones: Optional[str] = None


# ============================================================
# GENERAR CÓDIGO
# ============================================================

def generar_codigo_solicitud():
    """
    Genera un identificador para la solicitud.

    Ejemplo:
    INTI-R-20261008-A3F21C
    """

    fecha = datetime.now().strftime("%Y%m%d")

    identificador = (
        uuid.uuid4()
        .hex[:6]
        .upper()
    )

    return f"INTI-R-{fecha}-{identificador}"


# ============================================================
# LIMPIEZA DE TEXTO
# ============================================================

def _limpiar_texto(valor):
    """
    Convierte un valor en texto limpio.
    """

    if valor is None:
        return None

    valor = str(valor).strip()

    if not valor:
        return None

    return valor


# ============================================================
# VALIDAR CORREO
# ============================================================

def validar_correo(correo):
    """
    Validación básica de correo electrónico.

    No pretende reemplazar una validación avanzada,
    pero evita entradas evidentemente incorrectas.
    """

    correo = _limpiar_texto(correo)

    if not correo:
        return False

    if "@" not in correo:
        return False

    partes = correo.split("@")

    if len(partes) != 2:
        return False

    usuario, dominio = partes

    if not usuario or not dominio:
        return False

    if "." not in dominio:
        return False

    return True


# ============================================================
# CREAR SOLICITUD
# ============================================================

def crear_solicitud_reunion(
    nombre,
    correo,
    motivo,
    fecha_propuesta,
    hora_propuesta,
    telefono=None,
    empresa=None,
    funcionario=None,
    correo_funcionario=None,
):
    """
    Crea una nueva solicitud de reunión.

    IMPORTANTE:
    El estado inicial es SOLICITADA.

    Esto NO significa que la reunión haya sido confirmada.
    """

    nombre = _limpiar_texto(nombre)
    correo = _limpiar_texto(correo)
    motivo = _limpiar_texto(motivo)

    telefono = _limpiar_texto(telefono)
    empresa = _limpiar_texto(empresa)

    funcionario = _limpiar_texto(funcionario)
    correo_funcionario = _limpiar_texto(
        correo_funcionario
    )

    fecha_propuesta = _limpiar_texto(
        fecha_propuesta
    )

    hora_propuesta = _limpiar_texto(
        hora_propuesta
    )

    # --------------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------------

    if not nombre:
        raise ValueError(
            "El nombre del solicitante es obligatorio."
        )

    if not validar_correo(correo):
        raise ValueError(
            "Debes ingresar un correo electrónico válido."
        )

    if not motivo:
        raise ValueError(
            "El motivo de la reunión es obligatorio."
        )

    if not fecha_propuesta:
        raise ValueError(
            "Debes indicar una fecha tentativa."
        )

    if not hora_propuesta:
        raise ValueError(
            "Debes indicar una hora tentativa."
        )

    if (
        correo_funcionario
        and not validar_correo(correo_funcionario)
    ):
        raise ValueError(
            "El correo del funcionario no es válido."
        )

    ahora = datetime.now().isoformat(
        timespec="seconds"
    )

    solicitud = SolicitudReunion(
        codigo=generar_codigo_solicitud(),

        nombre=nombre,
        correo=correo,

        telefono=telefono,
        empresa=empresa,

        motivo=motivo,

        fecha_propuesta=fecha_propuesta,
        hora_propuesta=hora_propuesta,

        funcionario=funcionario,
        correo_funcionario=correo_funcionario,

        estado=ESTADO_SOLICITADA,

        fecha_creacion=ahora,
        fecha_actualizacion=ahora,
    )

    return solicitud


# ============================================================
# MARCAR COMO ENVIADA
# ============================================================

def marcar_como_enviada(solicitud):
    """
    Indica que la solicitud fue enviada al funcionario.

    Esto todavía NO significa que la reunión esté confirmada.
    """

    solicitud.estado = ESTADO_ENVIADA

    solicitud.fecha_actualizacion = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return solicitud


# ============================================================
# CONFIRMAR REUNIÓN
# ============================================================

def confirmar_reunion(
    solicitud,
    fecha=None,
    hora=None,
    observaciones=None,
):
    """
    Confirma una reunión.

    Esta función debe utilizarse únicamente después de que
    el funcionario autorizado confirme disponibilidad.
    """

    fecha_final = (
        _limpiar_texto(fecha)
        or solicitud.fecha_propuesta
    )

    hora_final = (
        _limpiar_texto(hora)
        or solicitud.hora_propuesta
    )

    solicitud.estado = ESTADO_CONFIRMADA

    solicitud.fecha_confirmada = fecha_final
    solicitud.hora_confirmada = hora_final

    solicitud.observaciones = _limpiar_texto(
        observaciones
    )

    solicitud.fecha_actualizacion = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return solicitud


# ============================================================
# PROPONER REPROGRAMACIÓN
# ============================================================

def proponer_reprogramacion(
    solicitud,
    nueva_fecha,
    nueva_hora,
    observaciones=None,
):
    """
    Registra una fecha alternativa propuesta por INTILED.

    La reunión todavía NO queda confirmada.
    El usuario debe aceptar posteriormente la nueva fecha.
    """

    nueva_fecha = _limpiar_texto(
        nueva_fecha
    )

    nueva_hora = _limpiar_texto(
        nueva_hora
    )

    if not nueva_fecha:
        raise ValueError(
            "Debes indicar la nueva fecha propuesta."
        )

    if not nueva_hora:
        raise ValueError(
            "Debes indicar la nueva hora propuesta."
        )

    solicitud.estado = (
        ESTADO_REPROGRAMACION
    )

    solicitud.fecha_alternativa = (
        nueva_fecha
    )

    solicitud.hora_alternativa = (
        nueva_hora
    )

    solicitud.observaciones = _limpiar_texto(
        observaciones
    )

    solicitud.fecha_actualizacion = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return solicitud


# ============================================================
# ACEPTAR REPROGRAMACIÓN
# ============================================================

def aceptar_reprogramacion(solicitud):
    """
    Confirma la fecha alternativa previamente propuesta.

    Debe ejecutarse después de que el usuario acepte
    la nueva fecha y hora.
    """

    if (
        not solicitud.fecha_alternativa
        or not solicitud.hora_alternativa
    ):
        raise ValueError(
            "No existe una fecha alternativa pendiente."
        )

    solicitud.estado = ESTADO_CONFIRMADA

    solicitud.fecha_confirmada = (
        solicitud.fecha_alternativa
    )

    solicitud.hora_confirmada = (
        solicitud.hora_alternativa
    )

    solicitud.fecha_actualizacion = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return solicitud


# ============================================================
# RECHAZAR
# ============================================================

def rechazar_solicitud(
    solicitud,
    observaciones=None,
):
    """
    Marca la solicitud como rechazada.
    """

    solicitud.estado = ESTADO_RECHAZADA

    solicitud.observaciones = _limpiar_texto(
        observaciones
    )

    solicitud.fecha_actualizacion = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return solicitud


# ============================================================
# CANCELAR
# ============================================================

def cancelar_solicitud(
    solicitud,
    observaciones=None,
):
    """
    Cancela una solicitud.
    """

    solicitud.estado = ESTADO_CANCELADA

    solicitud.observaciones = _limpiar_texto(
        observaciones
    )

    solicitud.fecha_actualizacion = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    return solicitud


# ============================================================
# CONVERTIR A DICCIONARIO
# ============================================================

def solicitud_a_dict(solicitud):
    """
    Convierte la solicitud a diccionario.

    Será útil posteriormente para:
    - Streamlit Session State
    - bases de datos
    - panel administrativo
    - reportes
    """

    return asdict(solicitud)


# ============================================================
# RESUMEN PARA EL USUARIO
# ============================================================

def generar_resumen_usuario(solicitud):
    """
    Genera el mensaje que INTI puede mostrar al usuario
    después de crear la solicitud.
    """

    empresa = ""

    if solicitud.empresa:
        empresa = (
            f"\n🏢 **Empresa/Entidad:** "
            f"{solicitud.empresa}"
        )

    return f"""
### 📅 Solicitud de reunión recibida

**Código:** `{solicitud.codigo}`

👤 **Solicitante:** {solicitud.nombre}
{empresa}

📍 **Fecha tentativa:** {solicitud.fecha_propuesta}

🕐 **Hora tentativa:** {solicitud.hora_propuesta}

📧 **Correo de contacto:** {solicitud.correo}

**Motivo:**  
{solicitud.motivo}

---

⚠️ **La reunión todavía no está confirmada.**

La fecha y hora indicadas corresponden a una propuesta inicial.
La solicitud debe ser revisada por el equipo de **INTILED**.

Cuando exista confirmación o sea necesario proponer una nueva fecha,
el usuario deberá ser informado por correo electrónico.
""".strip()


# ============================================================
# RESUMEN PARA FUNCIONARIO
# ============================================================

def generar_resumen_funcionario(solicitud):
    """
    Genera un resumen estructurado para incluir posteriormente
    en el correo enviado al funcionario de INTILED.
    """

    telefono = (
        solicitud.telefono
        if solicitud.telefono
        else "No suministrado"
    )

    empresa = (
        solicitud.empresa
        if solicitud.empresa
        else "No suministrada"
    )

    return f"""
NUEVA SOLICITUD DE REUNIÓN - INTI

Código:
{solicitud.codigo}

SOLICITANTE
----------------------------------------
Nombre: {solicitud.nombre}
Empresa/Entidad: {empresa}
Correo: {solicitud.correo}
Teléfono: {telefono}

REUNIÓN PROPUESTA
----------------------------------------
Fecha tentativa: {solicitud.fecha_propuesta}
Hora tentativa: {solicitud.hora_propuesta}

MOTIVO
----------------------------------------
{solicitud.motivo}

ESTADO
----------------------------------------
{solicitud.estado}

IMPORTANTE
----------------------------------------
Esta solicitud fue generada mediante INTI.

La fecha y hora todavía no constituyen una reunión confirmada.
Se requiere validación de disponibilidad por parte del funcionario
o equipo responsable de INTILED.
""".strip()
