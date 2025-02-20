#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go


# Read the CSV file
file_path = '../data/reviews-and-reviewers-2024-10-08.csv'
df = pd.read_csv(file_path)

# Calculate the number of tokens (length) in each review
df['review_length'] = df.apply(lambda row: len(
    (str(row['review']) + ' ' + str(row['weaknesses']) + ' ' + str(row['strengths'])).split()), axis=1)


# Define bins from 0 to 1800 with an interval of 20
bins = list(range(0, 1660, 20))  # Creates bins: 0, 20, 40, ..., 1800
labels = [f'{i}-{i + 20}' for i in bins[:-1]]  # Create labels for the bins

# Create a new column for binned review lengths
df['length_bins'] = pd.cut(df['review_length'], bins=bins, labels=labels, right=False)

# Calculate the frequency distribution of the binned review lengths
frequency_distribution = df['length_bins'].value_counts().reindex(labels, fill_value=0).reset_index()

# Calculate the frequency distribution of review lengths
# frequency_distribution = df['review_length'].value_counts().reset_index()
frequency_distribution.columns = ['review_length', 'frequency']

# Calculate the mean and median review lengths
mean_length = df['review_length'].mean()
median_length = df['review_length'].median()

# Determine the bin for mean and median
mean_bin_index = int(mean_length // 20)
median_bin_index = int(median_length // 20)

# Get the corresponding bin labels
mean_bin_label = labels[mean_bin_index] if mean_bin_index < len(labels) else labels[-1]
median_bin_label = labels[median_bin_index] if median_bin_index < len(labels) else labels[-1]

# Create the bar chart using Plotly Graph Objects
fig = go.Figure(data=[
    go.Bar(
        x=frequency_distribution['review_length'],
        y=frequency_distribution['frequency'],
    )
])

# Add a line for the mean value
fig.add_shape(
    type='line',
    x0=mean_bin_label,
    x1=mean_bin_label,
    y0=0,
    y1=frequency_distribution['frequency'].max(),
    line=dict(color='orange', width=2, dash='dash'),
)
# Add a line for the median value
fig.add_shape(
    type='line',
    x0=median_bin_label,
    x1=median_bin_label,
    y0=0,
    y1=frequency_distribution['frequency'].max(),
    line=dict(width=2, dash='dash'),
)

# Update layout
fig.update_layout(
    # barmode='stack',  # Stack bars to show proportions
    # showlegend=True,
    title=dict(
        text='Frequency Distribution of Review Lengths',
        font=dict(size=28)  # Set the font size for the title
        ),
    xaxis_title=dict(
        text='Review Length (Number of Tokens)',
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

# Add annotation for the mean line
fig.add_annotation(
    x=mean_bin_label,
    y=frequency_distribution['frequency'].max(),  # Position the annotation
    text='Mean: {:.2f}'.format(mean_length),
    showarrow=False,
    # arrowhead=2,
    ax=0,
    ay=-40,
    font=dict(color='orange')
)
fig.add_annotation(
    x=median_bin_label,
    y=frequency_distribution['frequency'].max() * 0.9,  # Position the annotation
    text='Median: {:.2f}'.format(median_length),
    showarrow=False,
    # arrowhead=2,
    ax=0,
    ay=-40
)

# Show the plot
fig.show()
fig.write_image(f"../data/figures/review_length_freq_distr_binned.png", scale=6, width=1920, height=1080)
