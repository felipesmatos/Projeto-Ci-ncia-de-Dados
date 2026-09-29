import requests
from bs4 import BeautifulSoup
import gdown
import re

def baixar_dados_prf(ano, palavra_chave="multa"):
    url_portal = "https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    print(f"[{ano}] Acessando o portal da PRF...")
    try:
        response = requests.get(url_portal, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Erro ao acessar o portal: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
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
    print(f"[{ano}] Iniciando o download de {nome_arquivo}...")

    # como os arquivos estão hospedados no drive, estamos utilizando a biblioteca gdown para fazer o download
    try:
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', link_download)
        
        if match:
            file_id = match.group(1)
            gdown.download(id=file_id, output=nome_arquivo, quiet=False)
        else:
            gdown.download(url=link_download, output=nome_arquivo, quiet=False)
            
        print(f"[{ano}] Download finalizado: {nome_arquivo}\n")
        return nome_arquivo
    except Exception as e:
        print(f"[{ano}] Erro durante o download com gdown: {e}\n")
        return None


anos_desejados = [2023, 2024]

for ano in anos_desejados:
    baixar_dados_prf(ano, palavra_chave="multa")