from datetime import datetime, time, timedelta


def es_dia_laboral(fecha):
    """
    Lunes=0 ... Domingo=6
    Domingo no se trabaja.
    """
    return fecha.weekday() != 6


def generar_horarios_para_fecha(fecha):
    """
    Genera horarios de 30 min según el día:
    - Lunes a viernes: 07:00 a 14:00 y 15:00 a 18:00
    - Sábado: 07:00 a 14:00
    - Domingo: no hay servicio
    """
    if fecha.weekday() == 6:
        return []

    horarios = []

    def agregar_bloque(hora_inicio, hora_fin):
        actual = datetime.combine(fecha, hora_inicio)
        fin = datetime.combine(fecha, hora_fin)

        while actual < fin:
            horarios.append(actual.strftime("%H:%M"))
            actual += timedelta(minutes=30)

    # Sábado
    if fecha.weekday() == 5:
        agregar_bloque(time(7, 0), time(14, 0))
    else:
        # Lunes a viernes
        agregar_bloque(time(7, 0), time(14, 0))
        agregar_bloque(time(15, 0), time(18, 0))

    return horarios