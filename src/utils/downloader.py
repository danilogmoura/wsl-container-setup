import requests
from tqdm import tqdm
from src.exceptions import DownloadException


class Downloader:

    @staticmethod
    def get(url, destination, show_progress=True):
        if not url or not url.strip():
            raise ValueError("URL não pode ser nula ou vazia")

        if not destination or not destination.strip():
            raise ValueError("Destino não pode ser nulo ou vazio")

        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, disable=not show_progress)

            with open(destination, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()

            if total_size != 0 and progress_bar.n != total_size:
                raise DownloadException("Ocorreu um erro durante o download")

        except requests.exceptions.Timeout as e:
            raise DownloadException("O download demorou muito", e)
        except requests.exceptions.RequestException as e:
            raise DownloadException("Erro ao fazer o download", e)
        except Exception as e:
            raise DownloadException("Erro inesperado ao fazer o download", e)
