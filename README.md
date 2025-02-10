# Analyzing Team Performance Using Graph Theory Metrics

This repository contains the research paper *"Analyzing Team Performance Using Graph Theory Metrics"*, which explores the application of graph theory in football analytics. The study investigates the structural differences between championship-winning and relegated teams in La Liga by constructing player similarity networks and applying various network metrics.

## Abstract

In modern football analytics, understanding the factors that drive team success is crucial. This research models teams as player similarity graphs, where nodes represent players and weighted edges quantify performance similarities. By leveraging centrality and connectivity measures such as degree, closeness centrality, betweenness centrality, clustering coefficient, and PageRank, the study identifies key structural differences between successful and underperforming teams. The findings reveal that championship teams exhibit more cohesive network structures, whereas relegated teams often rely on a few key players, exposing strategic vulnerabilities. The insights derived from this analysis can inform tactical planning, recruitment strategies, and team performance optimization.

## Contents

- 📄 **Research Paper**: Full text of the paper in PDF format.
- 📊 **Datasets**: (Data used in the process and data visualization)
- 📎 **Scripts**: (Codes used in the process)

## Key Topics

- Graph Theory in Sports Analytics
- Football Performance Evaluation
- Network Science in Team Cohesion
- Centrality and Connectivity Metrics
- Tactical Planning and Recruitment Strategy

## Installation Instructions

To run the scripts in this repository, ensure you have the required Python libraries installed. You can install them using the following command:

```sh
pip install pandas scikit-learn requests beautifulsoup4
```

## How to Run

### 1. **Select the Team and Season**

- First, choose the team and season you want to analyze.
- Use the **Fbref URL** in this format:

```sh
https://fbref.com/pt/equipes/206d90db/2023-2024/Barcelona-Estatisticas
```

Replace the **team code** **team name** and **season year** in the URL to match your selection.

### 2. **Run `script.py`**

- After choosing your team and season, run the `script.py` file.
- The script will prompt you to:
1. Input the **Fbref URL** (from Step 1).
2. Specify the name of the file where you want to save the data (make sure to end the filename with `.csv`).

### 3. **Run `matriz.py`**

- Next, run the `matriz.py` file.
- The script will ask you to:
1. Provide the name of the **CSV file** generated by `script.py` (from Step 2).
2. Specify the name for the file to save the **similarity matrix** (again, make sure to add `.csv` at the end).

### 4. **Run `gephi.py`**

- Finally, run the `gephi.py` file.
- The script will:
1. Ask you to provide the **CSV file** created by `matriz.py` (from Step 3).
2. Prompt you for the name of the final output file (with `.csv` extension) that will be formatted for Gephi visualization.

## Notes

- **Order Matters**: Be sure to run the scripts in the listed order, as each step depends on the output of the previous one.
- **File Names**: Always use `.csv` extensions for the files generated and saved by each script.

## Article
[![📄 Article](https://img.shields.io/badge/📄-Read%20Article-blue)](https://github.com/LucasPorteladev/AnalyzingTeamPerfomanceUsingGraph/blob/master/Analyzing%20Team%20Performance%20Using%20Graph%20Theory%20Metrics.pdf)

## Author

**Lucas Portela**  
[GitHub Profile](https://github.com/LucasPorteladev)  

If you have any questions or would like to collaborate, feel free to reach out:  
[Email Address](mailto:lucas.portela@aluno.cefetmg.br)

## How to Cite

If you use this research in your work, please cite it as:

> L. C. Portela, "Analyzing Team Performance Using Graph Theory Metrics," 
> Federal Center of Technological Education of Minas Gerais, 2024.
