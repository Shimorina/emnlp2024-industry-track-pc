#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd


df = pd.read_csv('../data/all-submissions-31-July-2024.csv')

authors_column = df.iloc[:, 5]

# Split authors by comma and create a list of unique authors
unique_authors = set()

for authors in authors_column:
    # Split by comma and strip whitespace
    unique_authors.update(author.strip() for author in authors.split(','))

# Get the length of the unique authors list
unique_authors_length = len(unique_authors)

print(unique_authors_length)

# for element in sorted(list(unique_authors)):
#    print(element)
