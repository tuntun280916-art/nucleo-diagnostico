
from datetime import datetime, time, timedelta


def es_dia_laboral(fecha):
    return fecha.weekday() != 6


def generar_horarios_para_fecha(fecha):

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
        agregar_bloque(time(14, 0), time(16, 0))
        agregar_bloque(time(16, 0), time(20, 0))

    return horarios
