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

del df['Country']
del df['Type']
dfcounts=df['Institution'].value_counts(normalize=True).reset_index()
dfcounts.columns=['Institution','Counts']
#dfcounts.rename(index={0: "Institution", 1: "Counts"})
#df.join(dfcounts, on='Institution')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(dfcounts)

pie = px.pie(dfcounts, values='Counts', names='Institution', labels='Institution')
pie.update_traces(textposition='inside')
pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
pie.show()
#plotly.offline.plot(pie, filename="../data/author_affCountry_pie")
pie.write_image("../data/figures/author_affilitations_pie.png", scale=1, width=1500, height=1000)

#pie = dfcounts.plot(kind="pie", figsize=(20,20), legend = False, use_index=True, subplots=True, colormap="Pastel1")
#fig = pie[0].get_figure()
#fig.savefig("../data/author_affCountry_pie")

