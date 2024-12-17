def to_menu_lookup(state):
    """Transición al nodo `menu_lookup` si el query contiene 'menú'."""
    if "menú" in state["query"].lower():
        return {"_next": "menu_lookup"}
    return {"_next": "end"}


def to_make_reservation(state):
    """Transición al nodo `make_reservation` si el query contiene 'reserva'."""
    if "reserva" in state["query"].lower():
        return {"_next": "make_reservation"}
    return {"_next": "end"}

