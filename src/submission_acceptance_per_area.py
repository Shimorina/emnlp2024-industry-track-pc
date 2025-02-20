#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go


# Step 1: Read the CSV files
decisions_df = pd.read_csv('../data/reviews-2024-11-22.csv')  # Contains submission_id and decision
areas_df = pd.read_csv('../data/paper_areas.csv')          # Contains submission_id and area (areas were defined manually by PCs)

# Replace specific decision text
decisions_df['decision'] = decisions_df['decision'].replace('Accept (condition: ethics)', 'Accept')
areas_df['area'] = areas_df['area'].str.split(': ').str[-1]

# Merge the two DataFrames on submission_id
merged_df = pd.merge(decisions_df, areas_df, left_on='submission_id', right_on='submission-id')

# Fill missing decisions with "withdrawn"
merged_df['decision'] = merged_df['decision'].fillna('Withdrawn')

# Step 2: Calculate frequency distribution of areas
area_distribution = merged_df.groupby(['area', 'decision']).size().reset_index(name='count')

# Calculate total counts for each area
total_counts = area_distribution.groupby('area')['count'].sum().reset_index(name='total_count')

# Merge total counts back to area_distribution
area_distribution = pd.merge(area_distribution, total_counts, on='area')

# Sort by total count in descending order
area_distribution = area_distribution.sort_values(by='total_count', ascending=False)

# Create a sorted list of areas based on total counts
sorted_areas = area_distribution['area'].unique()

# Create a mapping of area names to their original order based on total counts
area_order = area_distribution[['area', 'total_count']].drop_duplicates().set_index('area')['total_count'].to_dict()

# Step 3: Create a bar plot using Plotly go
fig = go.Figure()

# Create a list of all areas for consistent ordering
all_areas = area_distribution['area'].unique()

# Add bars for each decision type
for decision in ['Accept', 'Reject', 'Withdrawn']:  # Include 'other' for any additional decision types
    decision_data = area_distribution[area_distribution['decision'] == decision].copy()  # Create a copy

    # Ensure all areas are represented
    decision_data = decision_data.set_index('area').reindex(all_areas, fill_value=0).reset_index()

    # Sort decision_data by total_count using area_order
    decision_data['area'] = pd.Categorical(decision_data['area'], categories=area_order.keys(), ordered=True)
    decision_data = decision_data.sort_values('area', key=lambda x: x.map(area_order), ascending=False)

    # Set text to display only if count is greater than 0
    text_counts = decision_data['count'].where(decision_data['count'] > 0, '')

    fig.add_trace(go.Bar(
        x=decision_data['area'],
        y=decision_data['count'],
        name=decision,
        text=text_counts,
        textposition='outside',
    ))

# Update layout
fig.update_layout(
    barmode='stack',
    title=dict(
        text='Frequency Distribution of Submission Areas',
        font=dict(size=28)  # Set the font size for the title
        ),
    xaxis_title=dict(
        text='Area',
        font=dict(size=18)
      ),
    xaxis=dict(
        tickfont=dict(size=18),
        tickangle=-50
      ),
    yaxis_title=dict(
        text='Frequency',
        font=dict(size=18)
      ),
    yaxis=dict(
        tickfont=dict(size=18),
      )
)

# Show the plot
fig.show()

fig.write_image(f"../data/figures/acceptance_per_area.png", scale=6, width=1920, height=1080)
