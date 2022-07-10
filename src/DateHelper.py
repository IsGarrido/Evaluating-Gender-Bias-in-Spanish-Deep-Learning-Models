from datetime import datetime


def FechaHoraTextual():
    return datetime.now().strftime("%Y-%m-%d %H:%M")