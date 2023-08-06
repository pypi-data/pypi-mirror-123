

class CatalogoResponse:
    def __init__(self, Status: int, Message: str, codigo_erp: str = '', protocolo: str = '', loja: str = '') -> None:
        self.codigo_erp = codigo_erp
        self.status = Status
        self.message = Message
        self.protocolo = protocolo
        self.loja = loja


class PriceResponse:
    def __init__(self, Identifiers: list[str], Status: int, Message: str, Protocolo: str):
        self.identifiers = Identifiers
        self.status = Status
        self.message = Message
        self.protocolo = Protocolo
