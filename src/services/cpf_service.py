class CPFService:
    def normalizar_cpf(self, cpf):
        return ''.join(filter(str.isdigit, cpf))

    def validar_cpf(self, cpf):
        cpf = self.normalizar_cpf(cpf)
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False

        def calc_digito(cpf, peso_inicial):
            soma = 0
            peso = peso_inicial
            for i in range(peso_inicial - 1):
                soma += int(cpf[i]) * peso
                peso -= 1
            resto = (soma * 10) % 11
            return 0 if resto == 10 else resto

        d1 = calc_digito(cpf, 10)
        d2 = calc_digito(cpf, 11)

        return d1 == int(cpf[9]) and d2 == int(cpf[10])
