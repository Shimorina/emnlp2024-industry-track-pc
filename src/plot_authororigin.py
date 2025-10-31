#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly


# Read the CSV file
file_path = '../data/author_aff.csv'
df = pd.read_csv(file_path)
# df.drop_duplicates()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

del df['Institution']
del df['Type']
dfcounts=df['Country'].value_counts(normalize=True).reset_index()
dfcounts.columns=['Country','Counts']
#dfcounts.rename(index={0: "Country", 1: "Counts"})
#df.join(dfcounts, on='Country')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(dfcounts)

pie = px.pie(dfcounts, values='Counts', names='Country', labels='Country')
pie.update_traces(textposition='inside')
pie.update_layout(uniformtext_minsize=5, uniformtext_mode='hide')
pie.show()
#plotly.offline.plot(pie, filename="../data/author_affCountry_pie")
pie.write_image("../data/figures/author_affCountry_pie.png", scale=1, width=800, height=800)





