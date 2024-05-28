import platform
import subprocess


class SystemChecker:
    __MIN_SUPPORTED_BUILD: int = 19041

    @staticmethod
    def check_windows_version_support():
        supported_release = ["10", "11"]
        build = int(platform.version().split(".")[2])

        release = platform.release()

        if platform.system() != "Windows":
            raise Exception("Sistema operacional não suportado")

        if release not in supported_release:
            raise Exception(
                f"Versão '{release}' não suportada. As versões suportadas são: {', '.join(supported_release)}")

        if "10" == release and build < SystemChecker.__MIN_SUPPORTED_BUILD:
            raise Exception(
                f"A versão do Windows não é suportada. Por favor, atualize para uma versão suportada a partir do "
                f"build {SystemChecker.__MIN_SUPPORTED_BUILD}.")

    @staticmethod
    def check_wsl2():
        try:
            output = subprocess.check_output(["wsl", "--list", "--verbose"], stderr=subprocess.STDOUT, text=True)
            if "2" not in output:
                raise EnvironmentError("O WSL2 não está instalado ou não está rodando neste sistema.")
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def check_requirements():
        SystemChecker.check_windows_version_support()
        SystemChecker.check_wsl2()
