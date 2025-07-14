# Redimensionador de Imagens via Selenium (Headless)

Este script automatiza o processo de captura e redimensionamento de imagens a partir de links fornecidos em um arquivo Excel. Ele utiliza o Selenium em modo headless para acessar imagens diretamente via navegador, renderiza com fundo branco, tira uma screenshot, redimensiona para 1000x1000 pixels e salva com 150 DPI.

---

## 🛠️ Requisitos

Instale os pacotes necessários com:

```bash
pip install selenium pillow pandas openpyxl
```

Certifique-se também de ter o **ChromeDriver** compatível com sua versão do Google Chrome.

---

## 📁 Estrutura do Excel esperada

O arquivo `imagens_lista.xlsx` deve conter as seguintes colunas:

| SKU         | Ordem | Link                                 |
|-------------|--------|--------------------------------------|
| 2608600218 | 01     | https://...imagem1.jpg               |

---

## 📌 O que o script faz

1. **Configura o Selenium com Chrome em modo headless**  
   Para que o navegador rode em segundo plano, sem abrir uma janela.

2. **Lê o Excel com os dados de SKU, Ordem e Link da imagem**

3. **Acessa o link da imagem com o Selenium**  
   Ao invés de abrir a imagem diretamente (o que poderia renderizar com fundo preto em dark mode), o script gera uma mini página HTML com fundo branco e insere a imagem nela. Isso evita faixas pretas indesejadas no resultado.

4. **Tira uma screenshot da imagem renderizada em fundo branco**

5. **Abre a imagem com PIL (Pillow)** e redimensiona proporcionalmente para 1000x1000 usando `ImageOps.pad` (com bordas brancas se necessário)

6. **Salva a imagem com 150 DPI**, no formato `SKU_ORDEM.jpg`, dentro de uma pasta com o nome do SKU

7. **Exibe o tamanho final do arquivo salvo (em kilobytes)** no terminal

---

## 🧠 Como garantimos fundo branco

Usamos um template HTML como este:

```html
<html>
  <body style="margin:0; padding:0; background-color:white; display:flex; justify-content:center; align-items:center; height:100vh;">
    <img src="LINK_DA_IMAGEM" style="max-width:100%; max-height:100%;" />
  </body>
</html>
```

Este HTML é carregado via data URL no navegador, o que garante que a imagem será renderizada centralizada sobre fundo branco, independentemente do modo do navegador.

---

## 📂 Estrutura de saída

Imagens são salvas em:

```
.../ImageResolutionChanges/imagens_convertidas/{SKU}/{SKU}_{ORDEM}.jpg
```

Exemplo:

```
C:/Users/old1ca/.../imagens_convertidas/2608600218/2608600218_01.jpg
```

---

## 📜 Trecho de código chave

```python
# Usando HTML com fundo branco para renderizar a imagem
from urllib.parse import quote

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
```

```python
# Redimensionar mantendo proporção e preenchendo fundo branco
from PIL import ImageOps
img_resized = ImageOps.pad(img, (1000, 1000), color=(255, 255, 255), method=Image.LANCZOS)

# Salvar imagem e logar tamanho
img_resized.save(caminho_saida, dpi=(150, 150))
tamanho_kb = os.path.getsize(caminho_saida) / 1024
print(f"✅ Salvo: {caminho_saida} ({tamanho_kb:.2f} KB)")
```

---

## ✅ Requisitos adicionais

- Google Chrome instalado
- ChromeDriver compatível no PATH ou no mesmo diretório do script
