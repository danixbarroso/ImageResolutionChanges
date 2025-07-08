from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import os
import pandas as pd
from io import BytesIO

# Configurar Selenium com Chrome em modo headless
options = Options()
options.add_argument("--headless")  # Modo invisível
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1200,1200")  # Tamanho fixo para capturas
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

        # Baixar a imagem como base64 (via navegador)
        driver.get(img_src)
        screenshot = driver.get_screenshot_as_png()

        # Carrega como imagem PIL e redimensiona
        img = Image.open(BytesIO(screenshot))
        img_resized = img.resize((1000, 1000), Image.LANCZOS)

        # Salvar
        nome_arquivo = f"{sku}_{ordem}.jpg"
        # Pasta de saída
        output_folder = f"C:/Users/old1ca/OneDrive - Bosch Group/Documents/ImageResolutionChanges/imagens_convertidas/{sku}"
        os.makedirs(output_folder, exist_ok=True)
        caminho_saida = os.path.join(output_folder, nome_arquivo)
        img_resized.save(caminho_saida, dpi=(150, 150))

        print(f"✅ Salvo: {caminho_saida}")

    except Exception as e:
        print(f"❌ Erro com {url}: {e}")

driver.quit()