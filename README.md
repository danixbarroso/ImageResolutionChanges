# Redimensionador de Imagens via Selenium (Headless)

Este script automatiza o processo de captura e redimensionamento de imagens a partir de links fornecidos em um arquivo Excel. Ele utiliza o Selenium em modo headless para acessar imagens diretamente via navegador, captura uma screenshot da imagem renderizada, redimensiona para 1000x1000 pixels e salva com 150 DPI.

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

3. **Acessa o link da imagem** com Selenium e aguarda o carregamento

4. **Identifica a tag `<img>` na página** e obtém o link direto da imagem via atributo `src`

5. **Recarrega o link direto da imagem no navegador** e tira uma screenshot da imagem renderizada

6. **Abre a imagem com PIL (Pillow)** e redimensiona para 1000x1000 pixels

7. **Salva a imagem com 150 DPI**, no formato `SKU_ORDEM.jpg`, dentro de uma pasta com o nome do SKU

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
# Redimensionar e salvar com 150 DPI
img_resized = img.resize((1000, 1000), Image.LANCZOS)
img_resized.save(caminho_saida, dpi=(150, 150))
```

---

## ✅ Requisitos adicionais

- Google Chrome instalado
- ChromeDriver compatível no PATH ou no mesmo diretório do script
