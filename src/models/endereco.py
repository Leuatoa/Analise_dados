class Endereco:
    def __init__(self, cep: str, logradouro: str, numero: str, complemento: str = '', bairro: str = '', cidade: str = '', estado: str = ''):
        self.cep = self._normalizar_cep(cep)
        self.logradouro = logradouro.strip().title()
        self.numero = numero.strip()
        self.complemento = complemento.strip()
        self.bairro = bairro.strip().title()
        self.cidade = cidade.strip().title()
        self.estado = estado.strip().upper()

    def _normalizar_cep(self, cep: str) -> str:
    
        numeros = ''.join(filter(str.isdigit, cep))
        if len(numeros) == 8:
            return f"{numeros[:5]}-{numeros[5:]}"
        return cep 

    def __str__(self):
        parts = [f"{self.logradouro}, {self.numero}"]
        if self.complemento:
            parts.append(f"Compl.: {self.complemento}")
        if self.bairro:
            parts.append(self.bairro)
        parts.append(f"{self.cidade} - {self.estado}")
        parts.append(f"CEP: {self.cep}")
        return ', '.join(parts)

    def validar_cep(self) -> bool:
       
        numeros = ''.join(filter(str.isdigit, self.cep))
        return len(numeros) == 8

