import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from src.services.cpf_service import CPFService

class TestCPFService(unittest.TestCase):
    def setUp(self):
        self.cpf_service = CPFService()

    def test_cpf_valido(self):
        cpf = "940.977.298-28"
        normalizado = self.cpf_service.normalizar_cpf(cpf)
        self.assertEqual(normalizado, "94097729828")
        self.assertTrue(self.cpf_service.validar_cpf(normalizado))

    def test_cpf_invalido(self):
        cpf = "111.111.111-11"
        normalizado = self.cpf_service.normalizar_cpf(cpf)
        self.assertEqual(normalizado, "11111111111")
        self.assertFalse(self.cpf_service.validar_cpf(normalizado))

if __name__ == '__main__':
    unittest.main()
