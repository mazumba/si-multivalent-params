def get_settings(dirname: str) -> [str, bool]:
    if 'tri_tetra' == dirname:
        return {'gaussian': 0.3, 'omit': True}
    if 'deca_bi' == dirname:
        return {'gaussian': False, 'omit': False}
