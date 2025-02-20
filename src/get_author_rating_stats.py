#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
from collections import defaultdict
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT
import numpy as np
from scipy.stats import spearmanr
import plotly.graph_objects as go


# ratings: calculate average if several ratings per one review
# ratings: calculate correlations between reviewer score and author ratings (need to have a dict {rev.score: author rating})


submissions = OR_CLIENT.get_all_notes(
    invitation=f"{VENUE_ID}/-/Submission",
    details='replies'
)

papers_with_metareviews = 301
metareviews = []
author_review_rating = []
rebuttals = []
papers_with_author_ratings = 0
# ratings_rev_score = pd.DataFrame()  # paper_id, metareview, review, rebuttal, author rating, decision
ratings_averaged = []
ratings_rev_score = []  # [[rating, review score], [rating, review score], ...]
for submission in submissions:
    rating_found = False
    average_ratings_per_paper = defaultdict(list)  # replyto: [rating1, rating2]
    review_scores = {}
    for reply in submission.details["replies"]:
        if reply["invitations"][0].endswith("Author_Review_Rating"):
            if not rating_found:
                papers_with_author_ratings += 1
            rating_found = True
            average_ratings_per_paper[reply['replyto']].append(reply['content']['review_quality']['value'])
        elif reply["invitations"][0].endswith("Official_Review"):
            review_scores[reply['id']] = reply['content']['rating']['value']
    ratings_averaged += [sum(v)/len(v) for _, v in average_ratings_per_paper.items()]
    for replyto, ratings in average_ratings_per_paper.items():
        # extract review score from the corresponding review
        ratings_rev_score.append([review_scores[replyto], sum(ratings)/len(ratings)])

    # metareviews = metareviews + [reply for reply in submission.details["replies"] if reply["invitations"][0].endswith("Meta_Review")]
    author_review_rating = author_review_rating + [reply for reply in submission.details["replies"] if reply["invitations"][0].endswith("Author_Review_Rating")]
    # rebuttals = rebuttals + [reply for reply in submission.details["replies"] if reply["invitations"][0].endswith("Rebuttal")]


author_ratings = []
for item in author_review_rating:
    author_ratings.append(item['content']['review_quality']['value'])

# Convert to numpy array for easier manipulation
data_array = np.array(ratings_rev_score)

# Extract the two variables
x = data_array[:, 0]
y = data_array[:, 1]

# Calculate Spearman correlation
correlation, p_value = spearmanr(x, y)

print(f'Spearman correlation: {correlation}, p-value: {p_value}')

print('Metareviews #:', len(metareviews))
print('Author Review Ratings #:', len(author_review_rating))
print('# of ratings averaged:', len(ratings_averaged))
print('Rebuttals #:', len(rebuttals))
print('Global average rating:', round(sum(ratings_averaged)/len(ratings_averaged), 4))
print('# of papers with author ratings:', papers_with_author_ratings,
      round(papers_with_author_ratings/(papers_with_metareviews/100), 3))


author_rating_explanation = {
    2: "Exceeds expectations",
    1: "Meets expectations",
    0: "Below expectations"
}

# Calculate frequency distribution
values, counts = np.unique(ratings_averaged, return_counts=True)


# Create a bar plot
fig = go.Figure()

# Add traces for ratings 0, 1, and 2 with legends
for value in values:
    count = counts[np.where(values == value)[0][0]]
    show_legend = value in author_rating_explanation.keys()
    fig.add_trace(go.Bar(
        x=[str(value)],  # Convert to string for categorical axis
        y=[count],  # Get the corresponding count
        name=f'Rating {value}: {author_rating_explanation[value]}' if show_legend else '',
        hoverinfo='text',
        textangle=0,  # Set text angle to 0 for normal orientation
        text=str(count),
        showlegend=show_legend  # Show legend only for specified ratings
    ))

# Format x-axis ticks to show two decimal places
formatted_ticks = [f"{value:.2f}" for value in values]

# Update layout
fig.update_layout(title=dict(
                        text='Frequency Distribution of Author Ratings',
                        font=dict(size=28)  # Set the font size for the title
                  ),
                  xaxis_title=dict(
                      text='Author Rating',
                      font=dict(size=18)
                  ),
                  xaxis=dict(
                      tickvals=[str(value) for value in values],
                      ticktext=formatted_ticks,  # Set formatted ticks
                      tickfont=dict(size=18)
                  ),
                  yaxis_title=dict(
                      text='Frequency',
                      font=dict(size=18)
                  ),
                  yaxis=dict(
                      tickfont=dict(size=18)
                  ),
                  barmode='group'
                  )

# Show the plot
fig.show()
fig.write_image(f"../data/figures/author_rating_distribution.png", scale=6, width=1920, height=1080)
