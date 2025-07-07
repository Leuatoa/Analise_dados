import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.services.phone_service import PhoneService

class TestPhoneService(unittest.TestCase):
    def setUp(self):
        self.phone_service = PhoneService()

    def test_telefone_completo(self):
        observacoes = []
        ddd, numero, erro = self.phone_service.normalizar_telefone("81988887777", "", observacoes)
        telefone_formatado = f"{ddd} {numero}" if ddd and numero else None
        self.assertEqual(telefone_formatado, "81 988887777")
        self.assertIsNone(erro)

    def test_telefone_sem_ddd(self):
        observacoes = []
        ddd, numero, erro = self.phone_service.normalizar_telefone("988887777", "51020-220", observacoes)
        telefone_formatado = f"{ddd} {numero}" if ddd and numero else None
        self.assertEqual(telefone_formatado, "81 988887777")
        self.assertIsNone(erro)

    def test_telefone_vazio(self):
        observacoes = []
        ddd, numero, erro = self.phone_service.normalizar_telefone("", "", observacoes)
        telefone_formatado = f"{ddd} {numero}" if ddd and numero else ""
        self.assertEqual(telefone_formatado, "")
        self.assertEqual(erro, "Celular ausente")

    def test_telefone_invalido(self):
        observacoes = []
        ddd, numero, erro = self.phone_service.normalizar_telefone("123", "", observacoes)
        telefone_formatado = f"{ddd} {numero}" if ddd and numero else "123"
        self.assertEqual(telefone_formatado, "123")
        self.assertEqual(erro, "Número inválido")

if __name__ == '__main__':
    unittest.main()
