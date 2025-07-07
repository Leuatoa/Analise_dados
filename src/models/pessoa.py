import re
from src.services.gender_service import GenderAPIService
from src.services.cpf_service import CPFService
from src.services.phone_service import PhoneService
from src.services.cep_service import CEPService


class Pessoa:
    PREPOSICOES = {"da", "de", "do", "das", "dos", "e"}

    def __init__(self, nome, email, celular, interesse, cpf, cep):
        self.nome_completo = self.normalizar_nome(nome)
        self.primeiro_nome, self.segundo_nome = self.extrair_nomes(nome)
        self.email = email
        self.interesse = interesse
        self.cpf = self.normalizar_cpf(cpf)
        self.cep = self.normalizar_cep(cep)
        self.bairro = ""
        self.cidade = ""
        self.estado = ""
        self.celular = ""
        self.genero = ""
        self.observacoes = []
        
        print(f"Nome completo: {self.nome_completo} | Primeiro: {self.primeiro_nome} | Segundo: {self.segundo_nome}")

        self.valida_e_normaliza(celular)

    def normalizar_nome(self, nome):
    
        palavras = nome.strip().split()
        resultado = []
        for p in palavras:
            p_lower = p.lower()
            if p_lower in self.PREPOSICOES:
                resultado.append(p_lower)
            else:
                resultado.append(p.capitalize())
        return " ".join(resultado)

    def extrair_nomes(self, nome):
        partes = nome.strip().split()
        if not partes:
             return "", ""

        primeiro = partes[0].capitalize()

        segundo_partes = []
        for parte in partes[1:-1]:
            if parte.lower() in self.PREPOSICOES:
                segundo_partes.append(parte.lower())
            else:
                segundo_partes.append(parte.capitalize())

        segundo = " ".join(segundo_partes)
        return primeiro, segundo




    def normalizar_cpf(self, cpf):
        if cpf:
            return re.sub(r"\D", "", cpf)
        return ""

    def normalizar_cep(self, cep):
        if cep:
            return re.sub(r"\D", "", cep)
        return ""

    def valida_e_normaliza(self, celular):
     
        phone_service = PhoneService()
        cep_service = CEPService()
        cpf_service = CPFService()

        
        if self.cpf:
            if not cpf_service.validar_cpf(self.cpf):
                self.observacoes.append("CPF inválido")
        else:
            self.observacoes.append("CPF ausente")

        if self.cep:
            info = cep_service.consultar_cep(self.cep)
            if info:
                self.bairro = info.get("bairro", "")
                self.cidade = info.get("localidade", "")
                self.estado = info.get("uf", "")
            else:
                self.observacoes.append("CEP inválido ou não encontrado")
        else:
            self.observacoes.append("CEP ausente")

    
        if not celular:
            self.observacoes.append("Celular ausente")
            self.celular = ""
        else:
            ddd, num_formatado, erro = phone_service.normalizar_telefone(celular, self.cep)
            if erro:
                self.observacoes.append(erro)
            self.celular = f"{ddd} {num_formatado}" if ddd and num_formatado else celular

    def inferir_genero(self, api_service: GenderAPIService):
        if self.primeiro_nome:
            resposta = api_service.inferir_genero(self.primeiro_nome)
            genero = resposta.get("gender")
            if genero:
                self.genero = genero
            else:
                self.genero = "unknown"
                self.observacoes.append("Gênero não inferido")
        else:
            self.genero = "unknown"
            self.observacoes.append("Nome para gênero ausente")

        print(f"[DEBUG] Gênero para {self.primeiro_nome}: {self.genero}")

