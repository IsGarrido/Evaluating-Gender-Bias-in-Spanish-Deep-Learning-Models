class StringHelper:

    def __init__(self) -> None:
        pass

    def as_file_name(text : str):
        t = text.replace(" ", "_")

        # DEJAR [MASK] como MASK
        t = t.replace("[", "")
        t = t.replace("]", "")

        # Quitar slash del nombre del modelo
        t = t.replace("/", "_")

        # Quitar puntos
        t = t.replace(".", "")
        return t

    def from_int(val: int, leading_zeroes = 0):
        s: str = str(val)
        if leading_zeroes > 0:
            return s.zfill(leading_zeroes)
        else:
            return s