#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go


# Load the CSV file into a DataFrame
df = pd.read_csv('../data/reviews-2024-11-22.csv')

# Step 1: Filter out rows where 'decision' is None or empty
df_filtered = df[df['decision'].notna()].copy()  # Use .copy() to avoid SettingWithCopyWarning

# Replace specific decision text
df_filtered['decision'] = df_filtered['decision'].replace('Accept (condition: ethics)', 'Accept')

# Step 2: Calculate the average review rating for each submission, ignoring None values
# review_rating_columns = [f'review_rating{i}' for i in range(1, 9)]
# df_filtered.loc[:, 'average_rating'] = df_filtered[review_rating_columns].mean(axis=1, skipna=True)

# Step 3: Create a frequency distribution of average ratings
rating_counts = df_filtered['AC_recommendation'].value_counts().reset_index()
rating_counts.columns = ['AC_recommendation', 'frequency']

# Sort the DataFrame by average_rating
rating_counts = rating_counts.sort_values(by='AC_recommendation', ascending=False)

# Step 4: Calculate accept and reject counts for each average rating
accept_counts = df_filtered[df_filtered['decision'] == 'Accept'].groupby('AC_recommendation').size().reindex(rating_counts['AC_recommendation'], fill_value=0)
reject_counts = df_filtered[df_filtered['decision'] == 'Reject'].groupby('AC_recommendation').size().reindex(rating_counts['AC_recommendation'], fill_value=0)

# Format average_rating to two decimal places
rating_counts['AC_recommendation'] = rating_counts['AC_recommendation'].round(2)

# Step 5: Create a bar plot
fig = go.Figure()

# Add bars for accept and reject counts
fig.add_trace(go.Bar(
    x=rating_counts['AC_recommendation'].astype(str),
    y=accept_counts,
    name='Accept',
    marker=dict(line=dict(width=1)),  # Add stroke
    hoverinfo='text',
    text=accept_counts,
    textangle=0,  # Set text angle to 0 for normal orientation
))

fig.add_trace(go.Bar(
    x=rating_counts['AC_recommendation'].astype(str),
    y=reject_counts,
    name='Reject',
    marker=dict(line=dict(width=1)),  # Add stroke
    hoverinfo='text',
    text=reject_counts,
    textangle=0,  # Set text angle to 0 for normal orientation
))

# Update layout
fig.update_layout(
    barmode='stack',  # Stack bars to show proportions
    showlegend=True,
    title=dict(
        text='Frequency Distribution of Meta-Review Recommendations and Decisions',
        font=dict(size=28)  # Set the font size for the title
        ),
    xaxis_title=dict(
        text='Meta-review Recommendation',
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
fig.write_image(f"../data/figures/decision_vs_metareview_recommendations.png", scale=6, width=1920, height=1080)
