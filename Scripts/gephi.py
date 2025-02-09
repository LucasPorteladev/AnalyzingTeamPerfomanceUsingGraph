import pandas as pd
def process_planilha():
    while True:
        # Perguntar ao usuário o nome do arquivo a ser aberto
        file_path = input("Digite o nome do arquivo CSV que deseja abrir (com extensão): ")
        try:
            # Carregar a matriz de similaridade a partir do arquivo CSV
            data = pd.read_csv(file_path)
            # Criar planilha de nós (Nodes)
            nodes = pd.DataFrame({
                "ID": range(len(data["Jogador"])),
                "LABEL": data["Jogador"]
            })
            # Criar planilha de arestas (Edges)
            edges = []
            for i, row in data.iterrows():
                for j, weight in enumerate(row[1:], start=1):
                    if i < j:  # Evitar duplicação porque o grafo é não-direcionado
                        edges.append({
                            "SOURCE": i,
                            "TARGET": j - 1,
                            "TYPE": "undirected",
                            "WEIGHT": weight
                        })
            edges_df = pd.DataFrame(edges)
            # Perguntar os nomes dos arquivos de saída
            nodes_file = input("Digite o nome do arquivo para salvar os nós (com extensão .csv): ")
            edges_file = input("Digite o nome do arquivo para salvar as arestas (com extensão .csv): ")
            # Salvar as planilhas em arquivos CSV
            nodes.to_csv(nodes_file, index=False)
            edges_df.to_csv(edges_file, index=False)
            print(f"As planilhas foram geradas com sucesso:")
            print(f"- Planilha de Nós: {nodes_file}")
            print(f"- Planilha de Arestas: {edges_file}")
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
        # Perguntar ao usuário se deseja processar outro arquivo
        continue_process = input("Deseja processar outro arquivo? (s/n): ").strip().lower()
        if continue_process != 's':
            print("Processo encerrado.")
            break
# Chamar a função principal
process_planilha()
