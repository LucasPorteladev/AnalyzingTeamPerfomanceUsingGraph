import pandas as pd
import matplotlib.pyplot as plt
import re
import matplotlib.patches as mpatches

# Listas de arquivos – ajuste os nomes conforme necessário
champion_spreadsheets = [
    "resultados_atletico2021.csv",
    "resultados_barcelona1819.csv",
    "resultados_barcelona2223.csv",
    "resultados_real1920.csv",
    "resultados_real2122.csv",
    "resultados_real2324.csv"
]

relegated_spreadsheets = [
    "resultados_alaves2122.csv",
    "resultados_eibar2021.csv",
    "resultados_elche2223.csv",
    "resultados_espanyol1920.csv",
    "resultados_rayo1819.csv",
    "resultados_granada2324.csv"
]

# Lista de métricas – certifique-se de que os nomes das colunas batem com os dos seus arquivos
metrics = [
    "degree",
    "weighted degree",
    "Authority",
    "Hub",
    "clustering",
    "Eccentricity",
    "closnesscentrality",
    "harmonicclosnesscentrality",
    "betweenesscentrality",
    "pageranks",
    "eigencentrality"
]

dfs = []

# Função para ler um arquivo e adicionar informações sobre time, temporada e grupo
def process_file(file, group):
    # Se os arquivos forem planilhas do Excel, utilize pd.read_excel(file)
    df = pd.read_csv(file)
    
    # Extraindo time e temporada a partir do nome do arquivo
    # Exemplo: "resultados_barcelona1819.csv" -> time = "Barcelona" e temporada = "1819"
    pattern = r"resultados_([a-zA-Z]+)([0-9]+)"
    match = re.search(pattern, file)
    if match:
        team = match.group(1).capitalize()  # Capitaliza a primeira letra
        season = match.group(2)
    else:
        team = file
        season = "unknown"
        
    df["team"] = team
    df["season"] = season
    df["group"] = group
    return df

# Processa os arquivos dos times campeões
for file in champion_spreadsheets:
    dfs.append(process_file(file, "Champion"))
    
# Processa os arquivos dos times rebaixados
for file in relegated_spreadsheets:
    dfs.append(process_file(file, "Relegated"))

# Concatena todos os DataFrames
data = pd.concat(dfs, ignore_index=True)

# Cálculo da média das métricas para cada Time/Temporada (cada arquivo pode ter múltiplas linhas)
grouped = data.groupby(["team", "season", "group"])[metrics].mean().reset_index()

# Cria colunas auxiliares para ordenação:
grouped["season_int"] = grouped["season"].astype(int)
grouped["group_order"] = grouped["group"].apply(lambda x: 0 if x == "Champion" else 1)

# Ordena: primeiro por temporada e, dentro da temporada, Champion antes de Relegated.
grouped = grouped.sort_values(by=["season_int", "group_order"])

# Cria coluna para o rótulo do eixo X (exemplo: "Barcelona - 18/19")
grouped["season_label"] = grouped["season"].apply(lambda t: f"{t[:2]}/{t[2:]}" if len(t) == 4 else t)
grouped["x_label"] = grouped.apply(lambda row: f"{row['team']} - {row['season_label']}", axis=1)

# Mapeamento de cores: Champion em azul escuro; Relegated em vermelho.
color_mapping = {"Champion": "darkblue", "Relegated": "red"}
grouped["color"] = grouped["group"].map(color_mapping)

# Gera gráficos de barras para cada métrica (médias)
for metric in metrics:
    plt.figure(figsize=(12, 6))
    
    # Cria as barras
    plt.bar(grouped["x_label"], grouped[metric], color=grouped["color"], edgecolor="black")
    
    plt.title(f"{metric}", fontsize=14)
    plt.xlabel("Team / Season", fontsize=12)
    plt.ylabel(f"{metric} mean", fontsize=12)
    
    # Ajusta os limites do eixo y
    min_val = grouped[metric].min()
    max_val = grouped[metric].max()
    if min_val == max_val:
        plt.ylim(min_val - 1, max_val + 1)
    else:
        delta = max_val - min_val
        plt.ylim(min_val - 0.1 * delta, max_val + 0.1 * delta)
    
    plt.xticks(rotation=45, ha="right", fontsize=14)
    
    # Cria patches personalizados para a legenda
    champion_patch = mpatches.Patch(color="darkblue", label="Champion")
    relegated_patch = mpatches.Patch(color="red", label="Relegated")
    
    # Adiciona legenda
    plt.legend(handles=[champion_patch, relegated_patch], loc="upper right", title="Legend", frameon=True)
    
    plt.tight_layout()
    plt.savefig(f"{metric}.png", dpi=300, bbox_inches="tight")
    plt.show()
