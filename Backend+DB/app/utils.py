# small helper functions can go here
def to_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default
