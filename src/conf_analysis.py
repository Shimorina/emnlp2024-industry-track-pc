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
# file_path = '../data/reviews-2024-11-22.csv'  # for AC confidence scores
df = pd.read_csv(file_path)


# Define the legend explanation
rev_score_explanation = {
    10: "Top 5% of accepted papers, seminal paper",
    9: "Top 15% of accepted papers, strong accept",
    8: "Top 50% of accepted papers, clear accept",
    7: "Good paper, accept",
    6: "Marginally above acceptance threshold",
    5: "Marginally below acceptance threshold",
    4: "Ok but not good enough - rejection",
    3: "Clear rejection",
    2: "Strong rejection",
    1: "Trivial or wrong"
}

confidence_explanation = {
    5: "The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature",
    4: "The reviewer is confident but not absolutely certain that the evaluation is correct",
    3: "The reviewer is fairly confident that the evaluation is correct",
    2: "The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper",
    1: "The reviewer's evaluation is an educated guess"
}

confidence_ac_explanation = {
    5: "The area chair is absolutely certain",
    4: "The area chair is confident but not absolutely certain",
    3: "The area chair is somewhat confident",
    2: "The area chair is not sure",
    1: "The area chair's evaluation is an educated guess"
}


def create_barplot_from_csv(value):
    # Create bar plot
    fig = go.Figure()

    if value == 'reviewer score':
        # Count occurrences of each rating
        range_list = range(1, 11)
        value_counts = df['rating'].value_counts().reindex(range_list, fill_value=0)
        rating_explanation = rev_score_explanation
        tick_text = [f'{i}: {rating_explanation[i]}' for i in range_list]
    elif value == 'reviewer confidence':
        range_list = range(1, 6)
        value_counts = df['confidence'].value_counts().reindex(range_list, fill_value=0)
        rating_explanation = confidence_explanation
        tick_text = [f'{i}' for i in range_list]
    elif value == 'AC Confidence':
        range_list = range(1, 6)
        value_counts = df['AC_confidence'].value_counts().reindex(range_list, fill_value=0)
        rating_explanation = confidence_ac_explanation
        tick_text = [f'{i}' for i in range_list]
    elif value == 'numbers of reviews per paper':
        range_list = range(1, 9)
        review_counts = df.groupby('submission_id').size().reset_index(name='number_of_reviews')
        # Count the frequency of each number of reviews
        frequency = review_counts['number_of_reviews'].value_counts().reset_index()
        frequency.columns = ['number_of_reviews', 'frequency']
        # Sort the DataFrame by number_of_reviews for better readability
        frequency = frequency.sort_values(by='number_of_reviews').reset_index(drop=True)
        # Convert the DataFrame to a dictionary
        value_counts = frequency.set_index('number_of_reviews')['frequency'].to_dict()
        rating_explanation = None
        tick_text = [f'{i}' for i in range_list]
    else:
        print('config not found')

    # Add bars for each rating
    for rating, count in value_counts.items():
        if value == 'reviewer score':
            legend_template = f'Rating {rating}: {rating_explanation[rating]}'
        elif value == 'reviewer confidence' or value == 'AC Confidence':
            legend_template = f'confidence: {rating}'
        elif value == 'numbers of reviews per paper' or value == 'review length':
            legend_template = None
        fig.add_trace(go.Bar(
            x=[rating],
            y=[count],
            name=legend_template,
            hoverinfo='text',
            text=f'{count}'
        ))

    # Update layout
    fig.update_layout(
        title=dict(
            text=f'{value.title()} Frequency Distribution',
            font=dict(size=28),
        ),
        xaxis_title=dict(
            # text='Score',
            # text='Number of Reviews per Paper',
            text='Confidence',
            font=dict(size=18)
        ),
        yaxis_title=dict(
            text='Frequency',
            font=dict(size=18)
        ),
        xaxis=dict(
            tickvals=list(range_list),  # Ensure all ticks from 1 to 10 or 5 are shown
            ticktext=tick_text,
            tickfont=dict(size=18)
        ),
        yaxis=dict(
            tickfont=dict(size=18)
        ),
        barmode='stack',
        showlegend=False  # only for numbers of reviews per paper
    )

    # Show figure
    fig.show()
    fig.write_image(f"../data/figures/{value}_distribution.png", scale=6, width=1920, height=1080)


create_barplot_from_csv('reviewer score')
# create_barplot_from_csv('reviewer confidence')
# create_barplot_from_csv('numbers of reviews per paper')
# create_barplot_from_csv('AC Confidence')  # need to change the csv
