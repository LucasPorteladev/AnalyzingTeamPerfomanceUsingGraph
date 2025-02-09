import requests
from bs4 import BeautifulSoup
import pandas as pd

def extrair_e_normalizar_dados():
    # Solicitar entrada do usuário
    url = input("Digite a URL da página que deseja extrair os dados: ").strip()
    nome_arquivo = input("Digite o nome do arquivo para salvar os dados (exemplo: dados.csv): ").strip()
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        jogadores_dados = {}
        
        tabelas_ids = {
            "stats_standard_12": ["Posicao", "Idade", "Jogos", "Minutos", "Gols", "Assistencias"],
            "stats_passing_12": ["Passes Concluidos", "Passes Tentados"],
            "stats_gca_12": ["Passes Perigosos"],
            "stats_defense_12": ["BotesDef", "BotesCentro", "BotesAta"],
            "stats_possession_12": ["PosseGrandeAreaDef", "PosseDefesa", "PosseCentro", "PosseAtaque", "PosseGrandeAreaAta"]
        }
        
        for tabela_id, colunas in tabelas_ids.items():
            tabela = soup.find('table', {'id': tabela_id})
            if tabela:
                for row in tabela.find_all('tr'):
                    headers = row.find_all('th')
                    if headers:
                        jogador = headers[0].text.strip()
                        if jogador:
                            if jogador not in jogadores_dados:
                                jogadores_dados[jogador] = {"Jogador": jogador}
                    
                    cells = row.find_all('td')
                    if cells:
                        for i, coluna in enumerate(colunas):
                            if i < len(cells):
                                jogadores_dados[jogador][coluna] = cells[i].text.strip()

        df = pd.DataFrame.from_dict(jogadores_dados, orient='index')
        
        numeric_columns = [col for col in df.columns if col not in ["Jogador", "Posicao", "Idade"]]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        if "Posicao" in df.columns and "Minutos" in df.columns:
            df = df[~df["Posicao"].str.contains("Goleiro", na=False)]
            df = df[df["Minutos"] >= 250]
        
        if "Minutos" in df.columns:
            df["Minutos"].replace(0, float('nan'), inplace=True)
            
            for col in numeric_columns:
                if col not in ["Jogos", "Minutos"]:
                    df[col] = df[col] / df["Minutos"]
            
            df.fillna(0, inplace=True)
        
        df.to_csv(nome_arquivo, index=False)
        print(f'Dados extraídos, normalizados e salvos em "{nome_arquivo}".')
    else:
        print('Falha na solicitação HTTP.')

extrair_e_normalizar_dados()
