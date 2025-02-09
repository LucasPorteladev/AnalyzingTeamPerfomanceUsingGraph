import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def extrair_e_normalizar_dados(url, nome_arquivo):
    response = requests.get(url)

    if response.status_code == 200:
        # Analisa o conteúdo da página com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Dicionário para armazenar os dados dos jogadores
        jogadores_dados = {}

        # Lista de tabelas e IDs relevantes
        tabelas_ids = {
            "stats_standard_12": ["Posicao", "Idade", "Jogos", "Minutos", "Gols", "Assistencias"],
            "stats_passing_12": ["Passes Concluidos", "Passes Tentados"],
            "stats_gca_12": ["Passes Perigosos"],
            "stats_defense_12": ["BotesDef", "BotesCentro", "BotesAta"],
            "stats_possession_12": ["PosseGrandeAreaDef", "PosseDefesa", "PosseCentro", "PosseAtaque", "PosseGrandeAreaAta"]
        }

        # Extraindo dados de cada tabela
        for tabela_id, colunas in tabelas_ids.items():
            tabela = soup.find('table', {'id': tabela_id})
            if tabela:
                for row in tabela.find_all('tr'):
                    headers = row.find_all('th')
                    if headers:
                        jogador = headers[0].text.strip()
                        if jogador and jogador != "":  # Evita cabeçalhos vazios
                            if jogador not in jogadores_dados:
                                jogadores_dados[jogador] = {"Jogador": jogador}
                    
                    cells = row.find_all('td')
                    if cells:
                        for i, coluna in enumerate(colunas):
                            if i < len(cells):  # Evita indexação fora do range
                                jogadores_dados[jogador][coluna] = cells[i].text.strip()

        # Criar DataFrame a partir do dicionário
        df = pd.DataFrame.from_dict(jogadores_dados, orient='index')

        # Converter colunas numéricas corretamente
        numeric_columns = [col for col in df.columns if col not in ["Jogador", "Posicao", "Idade"]]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Filtrar goleiros e jogadores com menos de 250 minutos jogados
        if "Posicao" in df.columns and "Minutos" in df.columns:
            df = df[~df["Posicao"].str.contains("Goleiro", na=False)]  # Remove goleiros
            df = df[df["Minutos"] >= 250]  # Remove jogadores com menos de 250 minutos

        # Garantir que a coluna "Minutos" não tenha zero para evitar divisão por zero
        if "Minutos" in df.columns:
            df["Minutos"].replace(0, float('nan'), inplace=True)  # Substitui zeros por NaN para evitar erros

            # Normalizar as estatísticas dividindo pelo número de minutos jogados
            for col in numeric_columns:
                if col not in ["Jogos", "Minutos"]:  # Não faz sentido dividir jogos ou minutos por minutos
                    df[col] = df[col] / df["Minutos"]

            # Substituir valores NaN por 0 após a normalização
            df.fillna(0, inplace=True)

        # Salvar DataFrame no arquivo CSV
        df.to_csv(nome_arquivo, index=False)

        print(f'Dados extraídos, normalizados e salvos em "{nome_arquivo}".')

    else:
        print('Falha na solicitação HTTP.')

# Exemplo de execução
extrair_e_normalizar_dados('https://fbref.com/pt/equipes/206d90db/Barcelona-Stats', 'barcelona_normalizado.csv')
