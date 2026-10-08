"""
INTI - Servicio de Correo Electrónico
INTILED S.A.S. BIC
Versión 1.0

Este módulo gestiona el envío de correos electrónicos relacionados
con las solicitudes de reunión generadas por INTI.

SEGURIDAD:
Las credenciales del correo NO deben almacenarse en este archivo.
Deben recibirse desde Streamlit Secrets.

IMPORTANTE:
Enviar una solicitud por correo NO significa que la reunión
haya sido confirmada.
"""

import smtplib
import ssl

from email.message import EmailMessage
from html import escape

from modules.appointments import SolicitudReunion


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

NOMBRE_REMITENTE = "INTI | INTILED"


# ============================================================
# VALIDACIONES
# ============================================================

def _validar_configuracion(
    smtp_host,
    smtp_port,
    usuario,
    password,
):
    """
    Comprueba que existan los datos mínimos necesarios
    para conectarse al servidor de correo.
    """

    if not smtp_host:
        raise ValueError(
            "No se ha configurado el servidor SMTP."
        )

    if not smtp_port:
        raise ValueError(
            "No se ha configurado el puerto SMTP."
        )

    if not usuario:
        raise ValueError(
            "No se ha configurado el usuario de correo."
        )

    if not password:
        raise ValueError(
            "No se ha configurado la contraseña del correo."
        )


# ============================================================
# ENVÍO SMTP
# ============================================================

def enviar_correo(
    destinatario,
    asunto,
    contenido_texto,
    contenido_html,
    smtp_host,
    smtp_port,
    usuario,
    password,
    responder_a=None,
):
    """
    Envía un correo electrónico mediante SMTP.

    Retorna True si el servidor acepta correctamente
    el envío del mensaje.

    Si ocurre un error, lanza una excepción para que
    app.py pueda informar que la solicitud NO fue enviada.
    """

    _validar_configuracion(
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        usuario=usuario,
        password=password,
    )

    if not destinatario:
        raise ValueError(
            "No se ha definido el destinatario."
        )

    mensaje = EmailMessage()

    mensaje["Subject"] = asunto

    mensaje["From"] = (
        f"{NOMBRE_REMITENTE} <{usuario}>"
    )

    mensaje["To"] = destinatario

    if responder_a:
        mensaje["Reply-To"] = responder_a

    # Versión texto plano
    mensaje.set_content(
        contenido_texto
    )

    # Versión HTML
    mensaje.add_alternative(
        contenido_html,
        subtype="html",
    )

    contexto_ssl = (
        ssl.create_default_context()
    )

    puerto = int(
        smtp_port
    )

    # --------------------------------------------------------
    # PUERTO 465
    # SSL DIRECTO
    # --------------------------------------------------------

    if puerto == 465:

        with smtplib.SMTP_SSL(
            smtp_host,
            puerto,
            context=contexto_ssl,
            timeout=30,
        ) as servidor:

            servidor.login(
                usuario,
                password,
            )

            servidor.send_message(
                mensaje
            )

    # --------------------------------------------------------
    # NORMALMENTE PUERTO 587
    # STARTTLS
    # --------------------------------------------------------

    else:

        with smtplib.SMTP(
            smtp_host,
            puerto,
            timeout=30,
        ) as servidor:

            servidor.ehlo()

            servidor.starttls(
                context=contexto_ssl
            )

            servidor.ehlo()

            servidor.login(
                usuario,
                password,
            )

            servidor.send_message(
                mensaje
            )

    return True


# ============================================================
# PLANTILLA BASE HTML
# ============================================================

def _plantilla_html(
    titulo,
    subtitulo,
    contenido,
    codigo=None,
):
    """
    Plantilla visual corporativa para correos de INTI.
    """

    codigo_html = ""

    if codigo:

        codigo_html = f"""
        <div style="
            margin-top:22px;
            padding:14px 16px;
            background:#F4F6F8;
            border-radius:10px;
            font-size:13px;
            color:#667085;
        ">
            Código de seguimiento:
            <strong style="color:#111827;">
                {escape(str(codigo))}
            </strong>
        </div>
        """

    return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

</head>

<body style="
    margin:0;
    padding:0;
    background:#F3F5F7;
    font-family:Arial, Helvetica, sans-serif;
">

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    role="presentation"
>

<tr>

<td
    align="center"
    style="padding:30px 12px;"
>

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    role="presentation"
    style="
        max-width:650px;
        background:#FFFFFF;
        border-radius:18px;
        overflow:hidden;
        box-shadow:
            0 8px 30px rgba(16,24,40,.08);
    "
>

<tr>

<td
    style="
        padding:28px 34px;
        background:#0B1016;
        border-bottom:4px solid #FF6500;
    "
>

<div style="
    font-size:12px;
    letter-spacing:2px;
    color:#FF8A00;
    font-weight:bold;
">
    INTILED
</div>

<div style="
    margin-top:6px;
    font-size:27px;
    line-height:1.2;
    color:#FFFFFF;
    font-weight:bold;
">
    {escape(titulo)}
</div>

<div style="
    margin-top:8px;
    color:#C5CBD3;
    font-size:14px;
">
    {escape(subtitulo)}
</div>

</td>

</tr>


<tr>

<td style="
    padding:34px;
    color:#1D2939;
    font-size:15px;
    line-height:1.7;
">

{contenido}

{codigo_html}

</td>

</tr>


<tr>

<td style="
    padding:22px 34px;
    background:#F8F9FA;
    border-top:1px solid #EAECF0;
    color:#667085;
    font-size:12px;
    line-height:1.6;
">

<strong style="color:#111827;">
    INTI · INTILED
</strong>

<br>

Este mensaje fue generado automáticamente
como parte del proceso de atención inicial.

<br><br>

La recepción de una solicitud de reunión
<strong>no implica confirmación automática</strong>
de la fecha u hora propuestas.

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""


# ============================================================
# CORREO AL FUNCIONARIO
# ============================================================

def enviar_solicitud_a_funcionario(
    solicitud: SolicitudReunion,
    smtp_host,
    smtp_port,
    usuario,
    password,
    correo_funcionario=None,
):
    """
    Envía la nueva solicitud de reunión
    al funcionario de INTILED.
    """

    destinatario = (
        correo_funcionario
        or solicitud.correo_funcionario
    )

    if not destinatario:

        raise ValueError(
            "No se ha configurado el correo "
            "del funcionario responsable."
        )

    empresa = (
        solicitud.empresa
        if solicitud.empresa
        else "No indicada"
    )

    telefono = (
        solicitud.telefono
        if solicitud.telefono
        else "No indicado"
    )

    # --------------------------------------------------------
    # TEXTO PLANO
    # --------------------------------------------------------

    texto = f"""
NUEVA SOLICITUD DE REUNIÓN - INTI

Código:
{solicitud.codigo}

SOLICITANTE
Nombre: {solicitud.nombre}
Empresa/Entidad: {empresa}
Correo: {solicitud.correo}
Teléfono: {telefono}

FECHA PROPUESTA
{solicitud.fecha_propuesta}

HORA PROPUESTA
{solicitud.hora_propuesta}

MOTIVO
{solicitud.motivo}

IMPORTANTE:
Esta reunión todavía NO está confirmada.

Por favor revisar disponibilidad y comunicarse
con el solicitante para confirmar la reunión
o proponer una nueva fecha.

INTI | INTILED
""".strip()

    # --------------------------------------------------------
    # HTML
    # --------------------------------------------------------

    contenido = f"""

<p>
Se ha recibido una nueva solicitud de reunión
a través de <strong>INTI</strong>.
</p>

<div style="
    margin:24px 0;
    padding:20px;
    background:#FFF5ED;
    border-left:4px solid #FF6500;
    border-radius:8px;
">

<div style="
    color:#9A3412;
    font-weight:bold;
    margin-bottom:5px;
">
    REUNIÓN PENDIENTE DE CONFIRMACIÓN
</div>

La fecha y hora indicadas por el usuario
son tentativas.

</div>


<h3 style="
    color:#111827;
    margin-top:28px;
">
    Solicitante
</h3>

<table
    width="100%"
    cellpadding="8"
    cellspacing="0"
    style="
        border-collapse:collapse;
        font-size:14px;
    "
>

<tr>
<td style="
    width:35%;
    background:#F8F9FA;
    border:1px solid #EAECF0;
">
<strong>Nombre</strong>
</td>

<td style="
    border:1px solid #EAECF0;
">
{escape(solicitud.nombre)}
</td>
</tr>


<tr>
<td style="
    background:#F8F9FA;
    border:1px solid #EAECF0;
">
<strong>Empresa / Entidad</strong>
</td>

<td style="
    border:1px solid #EAECF0;
">
{escape(empresa)}
</td>
</tr>


<tr>
<td style="
    background:#F8F9FA;
    border:1px solid #EAECF0;
">
<strong>Correo</strong>
</td>

<td style="
    border:1px solid #EAECF0;
">
{escape(solicitud.correo)}
</td>
</tr>


<tr>
<td style="
    background:#F8F9FA;
    border:1px solid #EAECF0;
">
<strong>Teléfono</strong>
</td>

<td style="
    border:1px solid #EAECF0;
">
{escape(telefono)}
</td>
</tr>

</table>


<h3 style="
    color:#111827;
    margin-top:28px;
">
    Fecha propuesta
</h3>

<div style="
    display:block;
    padding:18px;
    background:#0B1016;
    color:#FFFFFF;
    border-radius:10px;
">

<span style="
    color:#FF8A00;
    font-weight:bold;
">
    FECHA
</span>

<br>

{escape(solicitud.fecha_propuesta)}

<br><br>

<span style="
    color:#FF8A00;
    font-weight:bold;
">
    HORA
</span>

<br>

{escape(solicitud.hora_propuesta)}

</div>


<h3 style="
    color:#111827;
    margin-top:28px;
">
    Motivo de la reunión
</h3>

<p>
{escape(solicitud.motivo)}
</p>


<div style="
    margin-top:28px;
    padding:18px;
    background:#F0FDF4;
    border:1px solid #BBE5C8;
    border-radius:10px;
">

<strong style="color:#166534;">
Siguiente paso
</strong>

<br><br>

Revise su disponibilidad.

Si la fecha es posible, puede responder
directamente a este correo.

Si no tiene disponibilidad, puede proponer
una fecha y hora alternativas.

</div>

"""

    html = _plantilla_html(
        titulo="Nueva solicitud de reunión",
        subtitulo="INTI · Gestión de reuniones",
        contenido=contenido,
        codigo=solicitud.codigo,
    )

    asunto = (
        f"[INTI] Nueva solicitud de reunión "
        f"{solicitud.codigo}"
    )

    return enviar_correo(
        destinatario=destinatario,
        asunto=asunto,
        contenido_texto=texto,
        contenido_html=html,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        usuario=usuario,
        password=password,

        # Cuando el funcionario pulse "Responder",
        # responderá directamente al usuario.
        responder_a=solicitud.correo,
    )


# ============================================================
# CORREO DE RECEPCIÓN AL USUARIO
# ============================================================

def enviar_recepcion_a_usuario(
    solicitud: SolicitudReunion,
    smtp_host,
    smtp_port,
    usuario,
    password,
):
    """
    Informa al usuario que INTILED recibió
    su solicitud.

    NO confirma la reunión.
    """

    texto = f"""
Hola {solicitud.nombre}.

INTI ha recibido tu solicitud de reunión.

Código:
{solicitud.codigo}

Fecha propuesta:
{solicitud.fecha_propuesta}

Hora propuesta:
{solicitud.hora_propuesta}

Motivo:
{solicitud.motivo}

IMPORTANTE:
La reunión todavía NO está confirmada.

El equipo de INTILED revisará la disponibilidad
para la fecha propuesta.

Recibirás una respuesta posteriormente por correo.

INTI | INTILED
""".strip()

    contenido = f"""

<p>
Hola <strong>{escape(solicitud.nombre)}</strong>,
</p>

<p>
Hemos recibido correctamente tu solicitud
de reunión a través de <strong>INTI</strong>.
</p>

<div style="
    margin:24px 0;
    padding:20px;
    background:#FFF5ED;
    border-left:4px solid #FF6500;
    border-radius:8px;
">

<strong style="color:#9A3412;">
La reunión todavía no está confirmada.
</strong>

<br><br>

La fecha y hora que seleccionaste serán
revisadas por el equipo de INTILED.

</div>


<table
    width="100%"
    cellpadding="9"
    cellspacing="0"
    style="
        border-collapse:collapse;
        font-size:14px;
    "
>

<tr>

<td style="
    width:35%;
    background:#F8F9FA;
    border:1px solid #EAECF0;
">
<strong>Fecha propuesta</strong>
</td>

<td style="
    border:1px solid #EAECF0;
">
{escape(solicitud.fecha_propuesta)}
</td>

</tr>


<tr>

<td style="
    background:#F8F9FA;
    border:1px solid #EAECF0;
">
<strong>Hora propuesta</strong>
</td>

<td style="
    border:1px solid #EAECF0;
">
{escape(solicitud.hora_propuesta)}
</td>

</tr>


<tr>

<td style="
    background:#F8F9FA;
    border:1px solid #EAECF0;
">
<strong>Motivo</strong>
</td>

<td style="
    border:1px solid #EAECF0;
">
{escape(solicitud.motivo)}
</td>

</tr>

</table>


<p style="
    margin-top:26px;
">
El equipo revisará la solicitud y la respuesta
será enviada al correo registrado.
</p>

"""

    html = _plantilla_html(
        titulo="Solicitud recibida",
        subtitulo="Tu solicitud está siendo revisada",
        contenido=contenido,
        codigo=solicitud.codigo,
    )

    asunto = (
        f"INTILED | Solicitud recibida "
        f"{solicitud.codigo}"
    )

    return enviar_correo(
        destinatario=solicitud.correo,
        asunto=asunto,
        contenido_texto=texto,
        contenido_html=html,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        usuario=usuario,
        password=password,
    )


# ============================================================
# CORREO DE CONFIRMACIÓN
# ============================================================

def enviar_confirmacion_a_usuario(
    solicitud: SolicitudReunion,
    smtp_host,
    smtp_port,
    usuario,
    password,
):
    """
    Envía confirmación de una reunión que YA haya
    sido aprobada por INTILED.
    """

    fecha = (
        solicitud.fecha_confirmada
        or solicitud.fecha_propuesta
    )

    hora = (
        solicitud.hora_confirmada
        or solicitud.hora_propuesta
    )

    texto = f"""
Hola {solicitud.nombre}.

Tu reunión con INTILED ha sido confirmada.

Código:
{solicitud.codigo}

Fecha:
{fecha}

Hora:
{hora}

Motivo:
{solicitud.motivo}

INTI | INTILED
""".strip()

    contenido = f"""

<p>
Hola <strong>{escape(solicitud.nombre)}</strong>,
</p>

<p>
Tenemos una buena noticia.
</p>

<div style="
    padding:22px;
    margin:22px 0;
    background:#F0FDF4;
    border:1px solid #BBE5C8;
    border-radius:12px;
">

<div style="
    color:#166534;
    font-size:18px;
    font-weight:bold;
">
✓ Reunión confirmada
</div>

<br>

<strong>Fecha:</strong>
{escape(str(fecha))}

<br>

<strong>Hora:</strong>
{escape(str(hora))}

</div>

<p>
<strong>Motivo:</strong><br>
{escape(solicitud.motivo)}
</p>

<p>
Gracias por contactar a INTILED.
</p>

"""

    html = _plantilla_html(
        titulo="Reunión confirmada",
        subtitulo="INTILED",
        contenido=contenido,
        codigo=solicitud.codigo,
    )

    asunto = (
        f"INTILED | Reunión confirmada "
        f"{solicitud.codigo}"
    )

    return enviar_correo(
        destinatario=solicitud.correo,
        asunto=asunto,
        contenido_texto=texto,
        contenido_html=html,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        usuario=usuario,
        password=password,
    )


# ============================================================
# CORREO DE REPROGRAMACIÓN
# ============================================================

def enviar_reprogramacion_a_usuario(
    solicitud: SolicitudReunion,
    smtp_host,
    smtp_port,
    usuario,
    password,
):
    """
    Informa al usuario que la fecha inicialmente
    propuesta no está disponible y presenta
    una alternativa.
    """

    if not solicitud.fecha_alternativa:
        raise ValueError(
            "No existe una fecha alternativa."
        )

    if not solicitud.hora_alternativa:
        raise ValueError(
            "No existe una hora alternativa."
        )

    texto = f"""
Hola {solicitud.nombre}.

El equipo de INTILED revisó tu solicitud de reunión.

No fue posible confirmar la fecha inicialmente propuesta.

Nueva fecha sugerida:
{solicitud.fecha_alternativa}

Nueva hora sugerida:
{solicitud.hora_alternativa}

Código:
{solicitud.codigo}

Por favor responde a este correo indicando si
la nueva fecha y hora son adecuadas para ti.

INTI | INTILED
""".strip()

    contenido = f"""

<p>
Hola <strong>{escape(solicitud.nombre)}</strong>,
</p>

<p>
El equipo de INTILED revisó tu solicitud.
</p>

<p>
No fue posible confirmar la fecha inicialmente
propuesta, por lo que queremos presentarte
una alternativa:
</p>

<div style="
    padding:22px;
    margin:22px 0;
    background:#FFF5ED;
    border:1px solid #FED7AA;
    border-radius:12px;
">

<div style="
    color:#9A3412;
    font-weight:bold;
    margin-bottom:12px;
">
NUEVA FECHA PROPUESTA
</div>

<strong>Fecha:</strong>
{escape(solicitud.fecha_alternativa)}

<br><br>

<strong>Hora:</strong>
{escape(solicitud.hora_alternativa)}

</div>

<p>
Por favor responde a este correo indicando
si la nueva fecha y hora funcionan para ti.
</p>

"""

    html = _plantilla_html(
        titulo="Propuesta de reprogramación",
        subtitulo="INTILED · Solicitud de reunión",
        contenido=contenido,
        codigo=solicitud.codigo,
    )

    asunto = (
        f"INTILED | Nueva fecha propuesta "
        f"{solicitud.codigo}"
    )

    return enviar_correo(
        destinatario=solicitud.correo,
        asunto=asunto,
        contenido_texto=texto,
        contenido_html=html,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        usuario=usuario,
        password=password,
    )
