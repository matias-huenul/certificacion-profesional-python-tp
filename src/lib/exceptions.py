class SetupError(Exception):
    """
    Excepción a ser lanzada ante un error de
    configuración.
    """
    pass

class OperationError(Exception):
    """
    Excepción a ser lanzada ante un código de
    operación inválido ingresado por el usuario.
    """
    pass

class APIError(Exception):
    """
    Excepción a ser lanzada ante un error de la API.
    """
    pass
