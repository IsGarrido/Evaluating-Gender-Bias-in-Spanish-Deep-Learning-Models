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
