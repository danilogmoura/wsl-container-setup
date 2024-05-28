import unittest
from unittest.mock import patch
from src.core.system_checker import SystemChecker


class TestSystemChecker(unittest.TestCase):

    def setUp(self):
        self.mock_system = patch('platform.system').start()
        self.mock_release = patch('platform.release').start()
        self.mock_version = patch('platform.version').start()

        self.mock_system.return_value = 'Windows'
        self.mock_release.return_value = '10'
        self.mock_version.return_value = '10.0.19041'

        self.mock_check_output = patch('subprocess.check_output').start()
        self.mock_check_output.return_value = '  NAME      STATE           VERSION\n* Ubuntu    Running         2\n'

    def tearDown(self):
        patch.stopall()

    def teste_given_supported_windows_version_then_no_exception_should_be_raised(self):
        SystemChecker.check_windows_version_support()

    def teste_given_unsupported_windows_release_then_exception_should_be_raised(self):
        self.mock_release.return_value = '8'
        expected_message = "Versão '8' não suportada. As versões suportadas são: 10, 11"

        with self.assertRaises(Exception) as cm:
            SystemChecker.check_windows_version_support()
        self.assertEqual(str(cm.exception), expected_message)

    def teste_given_unsupported_windows_version_build_then_exception_should_be_raised(self):
        self.mock_version.return_value = '10.0.19040'
        expected_message = ("A versão do Windows não é suportada. Por favor, atualize para uma versão suportada a "
                            "partir do build 19041.")

        with self.assertRaises(Exception) as cm:
            SystemChecker.check_windows_version_support()
        self.assertEqual(str(cm.exception), expected_message)

    def test_given_windows_with_wsl2_installed_when_checking_wsl2_then_should_be_successful(self):
        SystemChecker.check_wsl2()

    def test_given_windows_without_wsl2_installed_when_checking_wsl2_then_exception_should_be_raised(self):
        self.mock_check_output.return_value = '  NAME      STATE           VERSION\n* Ubuntu    Stopped         1\n'

        expected_message = "O WSL2 não está instalado ou não está rodando neste sistema."

        with self.assertRaises(EnvironmentError) as cm:
            SystemChecker.check_wsl2()
        self.assertEqual(str(cm.exception), expected_message)


if __name__ == '__main__':
    unittest.main()
