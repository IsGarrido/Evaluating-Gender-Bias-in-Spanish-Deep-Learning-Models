from datetime import datetime

class DateHelper:

    def __init__(self) -> None:
        pass

    def FechaHoraTextual():
        return datetime.now().strftime("%Y-%m-%d %H:%M")