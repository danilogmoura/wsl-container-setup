from unittest import TestCase
from unittest.mock import patch, Mock
from src.utils.downloader import Downloader
from src.exceptions.download_exception import DownloadException
import requests
import tempfile
import os


class TestDownloader(TestCase):
    __URL = "http://example.com/file"

    def setUp(self):
        self.mock_requests = patch('requests.get').start()
        self.mock_response = Mock()
        self.mock_response.iter_content.return_value = [b'test data']
        self.mock_response.headers = {'content-length': '9'}
        self.mock_requests.return_value = self.mock_response

        self.temp_dir = tempfile.gettempdir()
        self.unique_filename = os.path.join(self.temp_dir, "downloader_test.txt")

    def tearDown(self):
        patch.stopall()

        if os.path.exists(self.unique_filename):
            os.remove(self.unique_filename)

    def test_given_valid_url_and_destination_when_downloading_then_file_should_be_created(self):
        Downloader.get(self.__URL, self.unique_filename)
        self.mock_requests.assert_called_once_with(self.__URL, stream=True, timeout=10)
        self.assertTrue(os.path.exists(self.unique_filename))

    def test_given_valid_url_and_destination_when_downloading_then_file_should_have_correct_content(self):
        Downloader.get(self.__URL, self.unique_filename)
        with open(self.unique_filename, 'rb') as f:
            content = f.read()
        self.assertEqual(content, b'test data')

    def test_given_url_when_downloading_and_timeout_then_raise_download_exception(self):
        self.mock_requests.side_effect = requests.exceptions.Timeout
        with self.assertRaises(DownloadException) as cm:
            Downloader.get(self.__URL, self.unique_filename)
        self.assertEqual(str(cm.exception), "O download demorou muito")

    def test_given_url_when_downloading_and_request_exception_then_raise_download_exception(self):
        self.mock_requests.side_effect = requests.exceptions.RequestException
        with self.assertRaises(DownloadException) as cm:
            Downloader.get(self.__URL, self.unique_filename)
        self.assertEqual(str(cm.exception), "Erro ao fazer o download")

    def test_given_url_when_downloading_and_unexpected_exception_then_raise_exception(self):
        self.mock_requests.side_effect = Exception
        with self.assertRaises(DownloadException) as cm:
            Downloader.get(self.__URL, self.unique_filename)
        self.assertEqual(str(cm.exception), "Erro inesperado ao fazer o download")

    def test_given_invalid_url_when_downloading_then_raise_value_error(self):
        with self.assertRaises(ValueError) as cm:
            Downloader.get('', self.unique_filename)
        self.assertEqual(str(cm.exception), "URL não pode ser nula ou vazia")

    def test_given_invalid_destination_when_downloading_then_raise_value_error(self):
        with self.assertRaises(ValueError) as cm:
            Downloader.get(self.__URL, '')
        self.assertEqual(str(cm.exception), "Destino não pode ser nulo ou vazio")
