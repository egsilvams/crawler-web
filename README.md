# 🌐 Crawler Web

![Interface do Crawler Web](![image](templates\image.PNG)


## 📌 Descrição

O **Crawler Web** é uma aplicação desenvolvida em Python que realiza a captura de **todas as URLs** existentes em um site a partir de uma URL inicial. 

Você pode configurar o número de **clusters** (de 1 a 100) para acelerar a extração paralela das URLs. Ao final do processo, um **arquivo `.txt`** é gerado contendo todos os links encontrados.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Flask (interface web)
- Docker (para containerização)
- Jenkins (para integração e automação de deploy)

---

## ⚙️ Como Executar

### 🔹 Clonando o Repositório

 - git clone https://github.com/egsilvams/crawler-web.git
 - cd crawler-web

---

### 🔹 Rodando com Docker

 - Build da imagem:
    - docker build -t crawler-web .

 - Executando o container:
    - docker run -d -p 5000:5000 --name crawler-web-container crawler-web

 - Acesse no navegador:
    - http://localhost:5000

---
