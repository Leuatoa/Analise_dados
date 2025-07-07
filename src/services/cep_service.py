import requests

class CEPService:
    def consultar_cep(self, cep):
        try:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            if "erro" in data:
                return None
           
            data['ddd'] = self.obter_ddd(data.get('uf'), data.get('localidade'))
            return data
        except Exception as e:
            print(f"Erro ao consultar CEP: {e}")
            return None

    def obter_ddd(self, uf, cidade):
      
        ddd_por_estado = {
            "SP": "11",
            "RJ": "21",
            "MG": "31",
            "RS": "51",
            "PE": "81",
            "BA": "71",
           
        }

        
        return ddd_por_estado.get(uf, "11")
    
    def preencher_endereco(self, pessoa):
        data = self.consultar_cep(pessoa.cep)
        if data:
            pessoa.bairro = data.get("bairro", "")
            pessoa.cidade = data.get("localidade", "")
            pessoa.estado = data.get("uf", "")
