import re
from src.services.cep_service import CEPService

class PhoneService:
    def normalizar_telefone(self, telefone, cep, observacoes):
        numeros = re.sub(r"\D", "", telefone or "")
        erro = None

        if not numeros:
            erro = "Celular ausente"
            return None, None, erro

        if numeros.startswith("0"):
            numeros = numeros[1:]

        if len(numeros) == 11:
            ddd = numeros[:2]
            numero = numeros[2:]
        elif len(numeros) == 9:
            ddd = None
            numero = numeros
        elif len(numeros) == 10:
            ddd = numeros[:2]
            numero = numeros[2:]
        else:
            ddd = None
            numero = numeros

        if not ddd and cep:
            cep_service = CEPService()
            info = cep_service.consultar_cep(cep)
            if info:
                ddd = info.get("ddd")
            if not ddd:
                erro = "DDD não encontrado e não informado"

        if numero and len(numero) == 8 and not numero.startswith("9"):
            numero = "9" + numero

        if numero and len(numero) == 9:
            return ddd, numero, erro
        else:
            erro = "Número inválido"
            return ddd, numero, erro
