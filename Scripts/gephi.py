import pandas as pd

def process_spreadsheet():
    while True:
        # Ask the user for the name of the file to open
        file_path = input("Enter the name of the CSV file you want to open (with extension): ")

        try:
            # Load the similarity matrix from the CSV file
            data = pd.read_csv(file_path)

            # Create nodes spreadsheet
            nodes = pd.DataFrame({
                "ID": range(len(data["Player"])),
                "LABEL": data["Player"]
            })

            # Create edges spreadsheet
            edges = []
            for i, row in data.iterrows():
                for j, weight in enumerate(row[1:], start=1):
                    if i < j:  # Avoid duplication since the graph is undirected
                        edges.append({
                            "SOURCE": i,
                            "TARGET": j - 1,
                            "TYPE": "undirected",
                            "WEIGHT": weight
                        })

            edges_df = pd.DataFrame(edges)

            # Ask for output file names
            nodes_file = input("Enter the name of the file to save the nodes (with .csv extension): ")
            edges_file = input("Enter the name of the file to save the edges (with .csv extension): ")

            # Save the spreadsheets as CSV files
            nodes.to_csv(nodes_file, index=False)
            edges_df.to_csv(edges_file, index=False)

            print(f"The spreadsheets were successfully generated:")
            print(f"- Nodes Spreadsheet: {nodes_file}")
            print(f"- Edges Spreadsheet: {edges_file}")

        except Exception as e:
            print(f"Error processing the file: {e}")

        # Ask the user if they want to process another file
        continue_process = input("Do you want to process another file? (y/n): ").strip().lower()
        if continue_process != 'y':
            print("Process terminated.")
            break

# Call the main function
process_spreadsheet()
