#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT
from collections import defaultdict


# names for submission and reviews
venue_group = OR_CLIENT.get_group(VENUE_ID)
submission_name = venue_group.content['submission_name']['value']
review_name = venue_group.content['review_name']['value']

# Fetch all submissions for the conference
submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/{submission_name}', details='replies')

# Initialize a set to hold reviewers who didn't submit reviews
inactive_reviewers = set()

notsubmitted_reviewers = defaultdict(int)  # reviewer: n_not_submitted_reviews

# Loop through each submission to check assigned reviewers
for submission in submissions:
    # Assigned reviewers per submission
    assigned_reviewers = OR_CLIENT.get_group(f'{VENUE_ID}/{submission_name}{submission.number}/Reviewers')
    # Fetch the reviews for the submission
    reviews = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/{submission_name}{submission.number}/-/{review_name}')
    reviewer_signatures = [note.signatures[0] for note in reviews]
    # Check for reviewers who haven't submitted a review
    notsubmitted = set(assigned_reviewers.anon_members).difference(reviewer_signatures)
    if notsubmitted:
        for reviewer_signature in notsubmitted:
            # get the user name by getting the index in anon_members and retrieve in members by index
            rev_username = assigned_reviewers.members[assigned_reviewers.anon_members.index(reviewer_signature)]
            inactive_reviewers.add(rev_username)
            notsubmitted_reviewers[rev_username] += 1

# Print the list of inactive reviewers
print("Reviewers who were assigned but didn't submit reviews:", len(inactive_reviewers))  # 68
for reviewer, n_reviews in notsubmitted_reviewers.items():
    print(reviewer, n_reviews)
    # 5 reviewers with 2 papers load didn't submit anything
    # other 5 reviewers with 2 papers load submit only 1 review
    # 1 reviewer with 4 papers load didn't submit anything
    # 22 reviewers with 3 papers load didn't submit anything
    # 35 reviewers who didn't submit 1 review are considered as reviewers who didn't do the full load
