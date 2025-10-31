#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd
import plotly.express as px


# Read the CSV file
file_path = '../data/author_aff.csv'
df = pd.read_csv(file_path)
# df.drop_duplicates()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

del df['Institution']
del df['Country']
dfcounts=df['Type'].value_counts(normalize=True).reset_index()
dfcounts.columns=['Type','Counts']
#dfcounts.rename(index={0: "Type", 1: "Counts"}).reset_index()
#df.join(dfcounts, on='Type')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(dfcounts)

pie = px.pie(dfcounts, values='Counts', names='Type', labels='Type')
pie.update_traces(textposition='inside')
pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie.show()
pie.write_image("../data/figures/author_affType_pie.png")
