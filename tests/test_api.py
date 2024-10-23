import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from api.app import hasil
from flask import Flask

class TestHasil(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_get_request(self):
        with self.app.test_request_context(method='GET'):
            response = hasil()
            self.assertIn('identifikasi.html', response.template_name)
            self.assertEqual(response.context['hasil'], '-')
            self.assertEqual(response.context['logs'], '')

    @patch('pandas.read_csv')
    @patch('api.app.Library')
    def test_post_request_with_file(self, mock_library, mock_read_csv):
        test_data = pd.DataFrame(np.random.rand(5,10))
        mock_read_csv.return_value = test_data
        
        mock_lib_instance = MagicMock()
        mock_lib_instance.logs = ['Processing...', 'Complete']
        mock_lib_instance.wavelet.return_value = 'wavelet_output'
        mock_lib_instance.CNN.return_value = 'cnn_output'
        mock_lib_instance.deteksi.return_value = 'Normal'
        mock_library.return_value = mock_lib_instance

        with self.app.test_request_context(method='POST'):
            mock_file = MagicMock()
            mock_file.filename = 'test.csv'
            
            with patch('flask.request.files') as mock_files:
                mock_files.__getitem__.return_value = mock_file
                response = hasil()
                
                data = response.get_json()
                self.assertEqual(data['prediction'], 'Normal')
                self.assertEqual(data['filename'], 'test.csv')
                self.assertEqual(data['logs'], 'Processing...\nComplete')

    def test_post_request_without_file(self):
        with self.app.test_request_context(method='POST'):
            with patch('flask.request.files', new={}):
                response = hasil()
                data = response.get_json()
                self.assertIn('prediction', data)

    @patch('pandas.read_csv')
    def test_invalid_file_format(self, mock_read_csv):
        mock_read_csv.side_effect = pd.errors.EmptyDataError
        
        with self.app.test_request_context(method='POST'):
            mock_file = MagicMock()
            mock_file.filename = 'invalid.csv'
            
            with patch('flask.request.files') as mock_files:
                mock_files.__getitem__.return_value = mock_file
                with self.assertRaises(pd.errors.EmptyDataError):
                    hasil()
