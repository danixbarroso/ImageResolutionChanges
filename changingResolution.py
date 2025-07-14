from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from PIL import ImageOps
import os
import pandas as pd
from io import BytesIO
# Cria HTML com fundo branco
from urllib.parse import quote

# Configurar Selenium com Chrome em modo headless
options = Options()
options.add_argument("--headless")  # Modo invisível
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1000,1000")  # Tamanho fixo para capturas
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Carrega o Excel
df = pd.read_excel("imagens_lista.xlsx")

for index, row in df.iterrows():
    sku = str(row["SKU"]).zfill(10)
    ordem = str(row["Ordem"]).zfill(2)
    url = row["Link"]

    try:
        driver.get(url)
        driver.implicitly_wait(5)

        # Se o link abrir diretamente a imagem, podemos capturar o src do <img>
        img_element = driver.find_element(By.TAG_NAME, "img")
        img_src = img_element.get_attribute("src")

        html_template = f"""
        <html>
        <body style="margin:0; padding:0; background-color:white; display:flex; justify-content:center; align-items:center; height:100vh;">
            <img src="{img_src}" style="max-width:100%; max-height:100%;" />
        </body>
        </html>
        """

        html_data_url = "data:text/html;charset=utf-8," + quote(html_template)
        driver.get(html_data_url)
        screenshot = driver.get_screenshot_as_png()

        # Carrega como imagem PIL e redimensiona
        img = Image.open(BytesIO(screenshot))
        # Redimensionar mantendo proporção e preencher bordas (letterbox)
        img_resized = ImageOps.pad(img, (1000, 1000), color=(255, 255, 255), method=Image.LANCZOS)

        # Salvar
        nome_arquivo = f"{sku}_{ordem}.jpg"
        # Pasta de saída
        output_folder = f"C:/Users/old1ca/OneDrive - Bosch Group/Documents/ImageResolutionChanges/imagens_convertidas/{sku}"
        os.makedirs(output_folder, exist_ok=True)
        caminho_saida = os.path.join(output_folder, nome_arquivo)
        img_resized.save(caminho_saida, dpi=(300, 300))
        # Obter tamanho em KB
        tamanho_kb = os.path.getsize(caminho_saida) / 1024
        print(f"✅ Salvo: {caminho_saida} ({tamanho_kb:.2f} KB)")

    except Exception as e:
        print(f"❌ Erro com {url}: {e}")

driver.quit()