import pandas as pd
from fuzzywuzzy import process

# Function to try different encodings
def read_csv_with_encoding(file_path, encodings=['utf-8', 'iso-8859-1', 'cp1252', 'latin1']):
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to read the file {file_path} with any of the specified encodings.")

# Read the mapping file
try:
    mapping_df = read_csv_with_encoding('mapping.csv')
except ValueError as e:
    print(f"Error reading mapping file: {e}")
    exit(1)

# Read the new items list
try:
    new_items_df = read_csv_with_encoding('new_items.csv')
except ValueError as e:
    print(f"Error reading new items file: {e}")
    exit(1)

# Rest of your code remains the same
def find_best_match(item, mapping_dict):
    if item in mapping_dict:
        return mapping_dict[item], 100  # Exact match
    else:
        best_match, score = process.extractOne(item, mapping_dict.keys())
        return mapping_dict[best_match], score

# Create a dictionary from the mapping DataFrame for faster lookup
mapping_dict = dict(zip(mapping_df['Item'], mapping_df['Category']))

# Apply the matching function to each item in the new items list
new_items_df['Matched_Category'], new_items_df['Match_Score'] = zip(*new_items_df['Item'].apply(lambda x: find_best_match(x, mapping_dict)))

# Set a threshold for acceptable matches (e.g., 80)
threshold = 80
new_items_df['Final_Category'] = new_items_df.apply(lambda row: row['Matched_Category'] if row['Match_Score'] >= threshold else 'Unmatched', axis=1)

# Save the results to a new CSV file
new_items_df.to_csv('mapped_items.csv', index=False, encoding='utf-8')

print("Category mapping complete. Results saved to 'mapped_items.csv'.")