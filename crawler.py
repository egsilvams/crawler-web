import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

lock = threading.Lock()
contador = 0

def extrair_urls(html, base_url, dominio_base, prefixo_base):
    soup = BeautifulSoup(html, "html.parser")
    urls = set()
    for tag in soup.find_all("a", href=True):
        href = tag['href']
        url_completa = urljoin(base_url, href)
        if url_completa.startswith("http"):
            dominio_url = urlparse(url_completa).netloc
            if dominio_url == dominio_base and url_completa.startswith(prefixo_base):
                urls.add(url_completa)
    return urls

def salvar_em_arquivo(lista, nome_arquivo="urls_encontradas.txt"):
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for url in sorted(lista):
            f.write(url + "\n")
    print(f"\n💾 URLs salvas em: {nome_arquivo}")

def tentar_ate_3_vezes(url, timeout=10):
    global contador
    for tentativa in range(1, 4):
        try:
            print(f"🌐 Tentativa {tentativa} para acessar: {url}")
            resposta = requests.get(url, timeout=timeout)
            if resposta.status_code == 200:
                contador = contador + 1
                return resposta.text
            else:
                print(f"⚠️ Status {resposta.status_code} em {url}")
        except Exception as e:
            print(f"❌ Erro ao tentar acessar {url} (tentativa {tentativa}): {e}")
        time.sleep(1)
    return None

def processar_url(url, dominio_base, prefixo_base, urls_encontradas, urls_para_visitar):
    html = tentar_ate_3_vezes(url)
    if html:
        novas_urls = extrair_urls(html, url, dominio_base, prefixo_base)
        with lock:
            for nova_url in novas_urls:
                if nova_url not in urls_encontradas:
                    urls_para_visitar.add(nova_url)

def crawler(url_inicial, num_clusters):
    dominio_base = urlparse(url_inicial).netloc
    prefixo_base = url_inicial.rstrip("/")
    urls_encontradas = set()
    urls_para_visitar = set([url_inicial])

    with ThreadPoolExecutor(max_workers = num_clusters) as executor:
        while urls_para_visitar:
            os.system('cls')  # Limpa o terminal no Windows
            print(f"\n📌 {len(urls_para_visitar)} URLs para visitar - {len(urls_encontradas)} já processadas")
            tarefas = []
            urls_lote = list(urls_para_visitar)

            # Marcar URLs como processadas antes de iniciar threads
            with lock:
                for url in urls_lote:
                    urls_encontradas.add(url)
                urls_para_visitar.clear()

            for url in urls_lote:
                tarefas.append(
                    executor.submit(processar_url, url, dominio_base, prefixo_base, urls_encontradas, urls_para_visitar)
                )

            for future in as_completed(tarefas):
                print(f"📌 {contador} URLs já processadas - {len(urls_encontradas)} para visitar")
                pass  # só aguarda finalização

    salvar_em_arquivo(urls_encontradas)
    return list(urls_encontradas)
