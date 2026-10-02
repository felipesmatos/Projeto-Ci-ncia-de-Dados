import requests
from bs4 import BeautifulSoup
import gdown
import re
import os

def baixar_dados_prf(ano, palavra_chave="multa"):
    url_portal = "https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    pasta_destino = "./data/raw"
    os.makedirs(pasta_destino, exist_ok=True)
    print(f"[{ano}] Acessando o portal da PRF...")

    try:
        resposta = requests.get(url_portal, headers=headers)
        resposta.raise_for_status()
    except Exception as e:
        print(f"Erro ao acessar o portal: {e}")
        return None

    soup = BeautifulSoup(resposta.content, 'html.parser')
    link_download = None
    
    # o objetivo aqui é procurar todas as linhas da tabela e achar uma que se encaixe nos requisistos
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        
        if len(tds) >= 2:
            descricao = tds[0].get_text(strip=True).lower()
            
            if str(ano) in descricao and (palavra_chave in descricao or 'infrac' in descricao):
                link_tag = tds[1].find('a', href=True)
                # aqui ele achou a linha que se encaixa e está verificando se tem o link de download
                if link_tag:
                    link_download = link_tag['href']
                    break
                    
    if not link_download:
        print(f"[{ano}] Link de download não encontrado na página para o ano {ano}.")
        return None

     # os prints são para ter maior controle  das operações e para debug
    print(f"[{ano}] Link encontrado: {link_download}")
    nome_arquivo = f"infracoes_prf_{ano}.zip"
    caminho_data = os.path.join(pasta_destino, nome_arquivo)
    print(f"[{ano}] Iniciando o download de {nome_arquivo} para {caminho_data}...")

     # como os arquivos estão hospedados no drive, estamos utilizando a biblioteca gdown para fazer o download
    try:
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', link_download)
        
        if match:
            id_arquivo = match.group(1)
            gdown.download(id=id_arquivo, output=caminho_data, quiet=False)
        else:
            gdown.download(url=link_download, output=caminho_data, quiet=False)
            
        print(f"[{ano}] Download finalizado: {caminho_data}\n")
        return caminho_data
    
    except Exception as e:
        print(f"[{ano}] Erro durante o download com gdown: {e}\n")
        return None


anos_desejados = [2023, 2024]

for ano in anos_desejados:
    baixar_dados_prf(ano, palavra_chave="acidentes")