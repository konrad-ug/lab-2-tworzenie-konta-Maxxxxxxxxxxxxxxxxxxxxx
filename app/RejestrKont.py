import Account

class RejestrKont:
    lista = []

    @classmethod
    def dodaj(cls, konto: Account):
        cls.lista.append(konto)

    @classmethod
    def find(cls, p) -> Account:
        for i in cls.lista:
            if i.pesel == p:
                return i

    @classmethod 
    def count(cls) -> int:
        return len(cls.lista)