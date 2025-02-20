#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd
import ast


# Step 1: Read the CSV file
df = pd.read_csv('../data/affiliations-accepted.csv')

# Step 2: Create a new DataFrame to store paper IDs and their affiliations
paper_affiliations = {}

for index, row in df.iterrows():
    paper_ids = ast.literal_eval(row['papers_ids'])  # Convert string representation of set to actual set
    affiliation = row['affiliation']
    affiliation_type = row['affiliation_type']

    for paper_id in paper_ids:
        if paper_id not in paper_affiliations:
            paper_affiliations[paper_id] = {'affiliations': set(), 'types': set()}
        paper_affiliations[paper_id]['affiliations'].add(affiliation)
        paper_affiliations[paper_id]['types'].add(affiliation_type)

# Step 3: Create a DataFrame from the paper_affiliations dictionary
result_df = pd.DataFrame.from_dict(paper_affiliations, orient='index')
result_df.reset_index(inplace=True)
result_df.rename(columns={'index': 'paper_id'}, inplace=True)

# todo: write df result to disk and annotate manually

# Function to determine affiliation type statistics
def affiliation_type_statistics(row):
    types = row['types']
    if len(types) == 1:
        return 'only ' + types.pop()
    else:
        return 'mixed'


# Apply the function to get statistics
result_df['affiliation_type_statistics'] = result_df.apply(affiliation_type_statistics, axis=1)

# Step 4: Count papers by affiliation type and collect their IDs
affiliation_summary = result_df.groupby('affiliation_type_statistics')['paper_id'].agg(list).reset_index()
affiliation_summary['number_of_papers'] = affiliation_summary['paper_id'].apply(len)

# Step 5: Print the output
for _, row in affiliation_summary.iterrows():
    print(f"{row['affiliation_type_statistics']}, {row['number_of_papers']}, {row['paper_id']}")


# find out which id is missing
list_of_accepted_papers = pd.read_csv('../data/accepted-papers-2024-10-15.csv')
print(set(list_of_accepted_papers['submission-id']).difference(set(result_df['paper_id'])))
