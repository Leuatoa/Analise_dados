import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from src.services.gender_service import GenderAPIService

class TestGenderService(unittest.TestCase):
    @patch('src.services.gender_service.requests.get')
    def test_genderize_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'gender': 'male'}
        
        service = GenderAPIService()
        genero_data = service.inferir_genero("Carlos")
        genero = genero_data.get("gender", "unknown")  # extrair o gênero do dict retornado
        
        self.assertEqual(genero, 'male')

if __name__ == '__main__':
    unittest.main()
