import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from src.models.pessoa import Pessoa
from src.services.cep_service import CEPService

class TestCEPService(unittest.TestCase):
    @patch('src.services.cep_service.requests.get')
    def test_cep_valido(self, mock_get):
        pessoa = Pessoa("João Silva", "joao@email.com", "", "TI", "00000000000", "51020-220")
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "bairro": "Boa Viagem",
            "localidade": "Recife",
            "uf": "PE"
        }
        service = CEPService()
        service.preencher_endereco(pessoa)
        self.assertEqual(pessoa.bairro, "Boa Viagem")
        self.assertEqual(pessoa.cidade, "Recife")
        self.assertEqual(pessoa.estado, "PE")
    
if __name__ == '__main__':
    unittest.main()
