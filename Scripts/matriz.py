import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

while True:
    try:
        # Ask for the input CSV file path
        file_path = input("Enter the CSV file path (including the .csv extension): ").strip()
        
        # Load the CSV spreadsheet
        data = pd.read_csv(file_path)

        # Select the columns to normalize (ignoring 'Player', 'Position', 'Age')
        columns_to_normalize = data.columns[3:]
        normalized_data = data.copy()

        # Normalization (dividing by the number of games)
        for col in columns_to_normalize:
            if col != 'Games':  # Avoid dividing by the number of games itself
                normalized_data[col] = data[col] / data['Games']

        # Handle NaN values after normalization
        normalized_data = normalized_data.fillna(0)  # Replace NaN with 0

        # Select only the numerical data to calculate similarity
        numerical_data = normalized_data[columns_to_normalize].drop(columns=['Games'])

        # Calculate the cosine similarity matrix
        similarity_matrix = cosine_similarity(numerical_data)

        # Convert the similarity matrix to a DataFrame for better presentation
        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=data['Player'],  # Player names
            columns=data['Player']  # Player names
        )

        # Ask for the output file name to save the similarity matrix
        output_file = input("Enter the file name to save the matrix (including the .csv extension): ").strip()
        similarity_df.to_csv(output_file)

        print(f"Similarity matrix successfully saved to '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Ask if the user wants to create another similarity matrix
    repeat = input("Do you want to create another similarity matrix? (y/n): ").strip().lower()
    if repeat != 'y':
        print("Ending the program. See you next time!")
        break
