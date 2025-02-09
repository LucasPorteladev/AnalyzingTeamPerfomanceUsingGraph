import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
while True:
    try:
        # Solicitar o caminho do arquivo CSV de entrada
        file_path = input("Digite o caminho do arquivo CSV (incluindo a extensão .csv): ").strip()
        
        # Carregar a planilha CSV
        data = pd.read_csv(file_path)
        # Selecionar as colunas para normalizar (ignorando 'Jogador', 'Posicao', 'Idade')
        columns_to_normalize = data.columns[3:]
        normalized_data = data.copy()
        # Substituir valores zero na coluna 'Jogos' por 1 para evitar divisão por zero
        data['Jogos'] = data['Jogos'].replace(0, 1)
        # Normalização (divisão pelo número de jogos)
        for col in columns_to_normalize:
            if col != 'Jogos':  # Evitar dividir o próprio número de jogos
                normalized_data[col] = data[col] / data['Jogos']
        # Tratar valores NaN, infinitos ou extremamente grandes
        normalized_data = normalized_data.replace([float('inf'), -float('inf')], 0)  # Substituir infinitos por 0
        normalized_data = normalized_data.fillna(0)  # Substituir NaN por 0
        # Selecionar apenas os dados numéricos para calcular a similaridade
        numerical_data = normalized_data[columns_to_normalize].drop(columns=['Jogos'])
        # Calcular a matriz de similaridade do cosseno
        similarity_matrix = cosine_similarity(numerical_data)
        # Converter a matriz de similaridade em um DataFrame para melhor apresentação
        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=data['Jogador'],  # Nomes dos jogadores
            columns=data['Jogador']  # Nomes dos jogadores
        )
        # Solicitar o nome do arquivo para salvar a matriz de similaridade
        output_file = input("Digite o nome do arquivo para salvar a matriz (incluindo a extensão .csv): ").strip()
        similarity_df.to_csv(output_file)
        print(f"Matriz de similaridade salva com sucesso em '{output_file}'.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    # Perguntar ao usuário se deseja realizar outro cálculo
    repeat = input("Deseja criar outra matriz de similaridade? (s/n): ").strip().lower()
    if repeat != 's':
        print("Encerrando o programa. Até a próxima!")
        break
