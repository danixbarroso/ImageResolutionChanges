# Import required libraries
import pandas as pd
from PIL import Image
from random_user_agent.user_agent import UserAgent  # For rotating User-Agent headers
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
from requests_kerberos import HTTPKerberosAuth  # For Kerberos-authenticated requests
from urllib.parse import urlparse
from io import BytesIO
import os
import time
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy configuration (Bosch internal network)
proxy_port = '8080'
proxy_ip = 'rb-proxy-de.bosch.com'

# Custom adapter to handle Kerberos authentication through proxy
class HTTPAdapterWithProxyKerberosAuth(requests.adapters.HTTPAdapter):
    def proxy_headers(self, proxy):
        headers = {}
        auth = HTTPKerberosAuth()
        parsed_url = urlparse(proxy)
        negotiate_details = auth.generate_request_header(None, parsed_url.hostname, is_preemptive=True)
        headers['Proxy-Authorization'] = negotiate_details
        return headers

# Define allowed software and OS types for User-Agent rotation
software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

# Instantiate UserAgent rotator with filters
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)


user_agents = user_agent_rotator.get_user_agents()
# Function to make HTTP requests with retry logic and Kerberos proxy authentication
def fetch_with_retry(url, retries=3, backoff_factor=2.0):
    session = requests.Session()
    session.proxies = {"http": f'{proxy_ip}:{proxy_port}', "https": f'{proxy_ip}:{proxy_port}'}
    session.mount('http://', HTTPAdapterWithProxyKerberosAuth())
    session.mount('https://', HTTPAdapterWithProxyKerberosAuth())

    for i in range(retries):
        # Get list of user-agents and select a random one
        random_user_agent = user_agent_rotator.get_random_user_agent()
        try:
            headers = {
                'User-Agent': random_user_agent,
                'Referer': 'https://www.photoshelter.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive'
            }
            response = session.get(url, headers=headers, verify=False)

            # Handle different HTTP responses
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                wait_time = backoff_factor * (2 ** i)
                print(f"Error 429. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            elif response.status_code == 403:
                wait_time = backoff_factor * (10 ** i)
                print(f"Error 403. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            elif response.status_code == 407:
                wait_time = backoff_factor * (10 ** i)
                print(f"Error 407. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Error accessing page: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
    return None

# Nome da pasta de saída
output_folder = "imagens_convertidas"
os.makedirs(output_folder, exist_ok=True)

df = pd.read_excel('imagens_lista.xlsx')

# Iterar pelas linhas
for index, row in df.iterrows():
    sku = str(row['SKU']).zfill(10)  # Garante 10 dígitos
    ordem = str(row['Ordem']).zfill(2)  # Garante 2 dígitos
    url = row['Link']

    try:
        # Baixar a imagem
        response = fetch_with_retry(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        # Redimensionar para 1000x1000
        img_resized = img.resize((1000, 1000), Image.LANCZOS)

        # Nome do arquivo de saída
        nome_arquivo = f"{sku}_{ordem}.jpg"
        caminho_saida = os.path.join(output_folder, nome_arquivo)

        # Salvar com 200 DPI
        img_resized.save(caminho_saida, dpi=(200, 200))

        print(f"✅ Salvo: {caminho_saida}")

    except Exception as e:
        print(f"❌ Erro com {url}: {e}")

