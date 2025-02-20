# PC-ing 2024 EMNLP Industry Track

This repository contains template emails for Program Chairs (PCs) and scripts for interacting with OpenReview and calculating some conference statistics.

## OpenReview Scripts

### Installation
1. Install requirements `pip install -r requirements.txt`
2. Create `.env` file with your OpenReview credentials. 

    ```txt
    OPENREVIEW_USERNAME=email@email.com
    OPENREVIEW_PASSWORD=password
    ```

3. For running with other venues: modify `VENUE_ID` in [openreview_client.py](src%2Fopenreview_client.py).

### Disclaimer

Please note that the scripts in this repository were developed very rapidly and under a constrained timeframe.

### Getting Conference Statistics

Get conference data:
- [get_accepted_papers.py](src%2Fget_accepted_papers.py): get a list of accepted papers
- [get_ethics_reviews_with_reviewers.py](src%2Fget_ethics_reviews_with_reviewers.py): get ethics reviews and reviewers
- [get_metareviews_ethics_review_scores_decisions.py](src%2Fget_metareviews_ethics_review_scores_decisions.py): get metareviews, ethics reviews, review scores, and decisions
- [get_reviewers.py](src%2Fget_reviewers.py): info about OR profiles for reviewers and meta-reviewers (# of publications imported in OR)
- [get_reviews.py](src%2Fget_reviews.py): get reviews with all fields of the review form (score, main text, weaknesses, strengths, ethics)
- [get_reviews_with_reviewers.py](src%2Fget_reviews_with_reviewers.py): get reviews with all fields of the review form (score, main text, weaknesses, strengths, ethics)
- [get_submissions.py](src%2Fget_submissions.py): get all submissions (needs to be run prior to the decision phase)

Conference statistics:
- [affiliation_stats.py](src%2Faffiliation_stats.py): affiliation statistics (academia, industry, both)
- [calculate_authors.py](src%2Fcalculate_authors.py): # of authors who submitted a paper
- [decision_plots.py](src%2Fdecision_plots.py): frequency distribution of average review ratings and decisions
- [get_inactive_reviewers.py](src%2Fget_inactive_reviewers.py): # of reviewers who were assigned but didn't submit reviews
- [get_review_ratings.py](src%2Fget_review_ratings.py): get author ratings for each review
- [rebuttal_analysis.py](src%2Frebuttal_analysis.py): # of papers with rebuttal; # of confidential comments to PC/AC; # of replies to rebuttal 

Generate graphics (see [figures](data%2Ffigures)):
- [conf_analysis.py](src%2Fconf_analysis.py): distribution of reviewer scores, reviewer/AC confidence, number of reviewers per paper
- [authors_per_paper_plot.py](src%2Fauthors_per_paper_plot.py): # of authors per paper
- [get_author_rating_stats.py](src%2Fget_author_rating_stats.py): author ratings for reviews; correlations between reviewer score and author ratings
- [metareview_decision_plot.py](src%2Fmetareview_decision_plot.py): distribution of meta-review recommendations vs. PC decisions
- [plot_review_length.py](src%2Fplot_review_length.py): frequency distribution of review lengths in tokens
- [submission_acceptance_per_area.py](src%2Fsubmission_acceptance_per_area.py): distribution of submission areas (defined manually by PCs) and acceptance decisions

Misc:
- [reviewer_suggestions_from_authors.py](src%2Freviewer_suggestions_from_authors.py): extract submission authors and invite them as emergency reviewers by sending an email
- [send_emails_reviewers.py](src%2Fsend_emails_reviewers.py): send emails to reviewers who have less than 4 papers in their OR profile


## Template Emails

You can find email templates for authors, reviewers, meta-reviewers in [template_emails](template_emails).

## PC Report

[Slides](https://docs.google.com/presentation/d/1OYl8Bg-ZXpdzw1xM8TU1Ar4WHs5cmB0s5vpWUllWpkc/edit?usp=sharing)

## Contact
<emnlp2024-industry-track@googlegroups.com>
