from datetime import datetime, time, timedelta


def es_dia_laboral(fecha):
    """
    Lunes=0 ... Domingo=6
    Domingo no se trabaja.
    """
    return fecha.weekday() != 6


def generar_horarios_para_fecha(fecha, intervalo_minutos=30):
    """
    Genera horarios disponibles según el día:
    - Lunes a viernes: 07:00 a 20:00
    - Sábado: 08:00 a 15:00
    - Domingo: sin servicio
    """
    if fecha.weekday() == 6:
        return []

    horarios = []

    def agregar_bloque(hora_inicio, hora_fin):
        actual = datetime.combine(fecha, hora_inicio)
        fin = datetime.combine(fecha, hora_fin)
        paso = timedelta(minutes=intervalo_minutos)

        while actual <= fin:
            horarios.append(actual.strftime("%H:%M"))
            actual += paso

    if fecha.weekday() == 5:
        agregar_bloque(time(8, 0), time(15, 0))
    else:
        agregar_bloque(time(7, 0), time(20, 0))

    return horarios