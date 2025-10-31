#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go


# Step 1: Read the CSV files
submissions_df = pd.read_csv('../data/all-submissions-27-10-2025.csv')
decisions_df = pd.read_csv('../data/all_decisions.csv')

# Replace specific decision text
decisions_df['decision'] = decisions_df['recommendation'].replace('Accept (condition: ethics)', 'Accept')

# Step 2: Calculate the number of authors for each submission
submissions_df['num_authors'] = submissions_df['authorids'].apply(lambda x: len(x.split(', ')))

# Step 3: Merge the DataFrames on submission-id
merged_df = pd.merge(submissions_df[['Id', 'num_authors']],
                      decisions_df,
                      left_on='Id',
                      right_on='Id',
                      how='outer')

#merged_df['recommendation'].fillna(value='Withdrawn', inplace=True)
merged_df.to_csv('../data/all_subm_rec_before.csv', sep=',', encoding='utf-8')
merged_df.fillna({'recommendation': 'Withdrawn'}, inplace=True)
merged_df.to_csv('../data/all_subm_rec_after.csv', sep=',', encoding='utf-8')

# Step 4: Create a frequency distribution of the number of authors
frequency_distribution = merged_df['num_authors'].value_counts().sort_index().reset_index()
frequency_distribution.columns = ['num_authors', 'frequency']

# Step 5: Create a frequency distribution of the number of authors by decision type
frequency_distribution = merged_df.groupby(['num_authors', 'recommendation']).size().reset_index(name='frequency')

# Step 6: Create a bar plot using Plotly go
fig = go.Figure()

# Add bars for each decision type
for decision in sorted(frequency_distribution['recommendation'].unique()):  # sort to make Accept blue
    decision_data = frequency_distribution[frequency_distribution['recommendation'] == decision]
    fig.add_trace(go.Bar(
        x=decision_data['num_authors'],
        y=decision_data['frequency'],
        name=decision,
        text=decision_data['frequency'],
        textposition='auto',
        textangle=0,  # Set text angle to 0 for normal orientation
    ))

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text='Histogram Number of Authors per Submission',
        font=dict(size=28)  # Set the font size for the title
        ),
    xaxis_title=dict(
        text='Number of Authors',
        font=dict(size=18)
      ),
    xaxis=dict(
        tickfont=dict(size=18)
      ),
    yaxis_title=dict(
        text='Frequency',
        font=dict(size=18)
      ),
    yaxis=dict(
        tickfont=dict(size=18)
      )
)

# Show the plot
fig.show()

fig.write_image(f"../data/figures/authors_per_paper.png", scale=6, width=1920, height=1080)
