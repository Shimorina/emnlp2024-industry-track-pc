#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT


# Fetch all submissions for the venue
venue_group = OR_CLIENT.get_group(VENUE_ID)
submission_name = venue_group.content['submission_name']['value']
submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/{submission_name}', details='replies')


review_name = venue_group.content['review_name']['value']

# reviews = [openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies']
#          if f'{VENUE_ID}/{submission_name}{s.number}/-/{review_name}' in reply['invitations']]

reviews = []
for submission in submissions:
    for reply in submission.details['replies']:
        if f'{VENUE_ID}/{submission_name}{submission.number}/-/{review_name}' in reply['invitations']:
            reviews.append(openreview.api.Note.from_json(reply))

print('# of reviews', len(reviews))


'''for review in reviews:
    print(review.content['review']['value'])'''
ratings = []
for submission in submissions:
    for reply in submission.details['replies']:
        for iterator in range(1, 4):
            # 'EMNLP/2024/Industry_Track/Submission104/Official_Review3/-/Author_Review_Rating'
            if f'{VENUE_ID}/{submission_name}{submission.number}/Official_Review{iterator}/-/Author_Review_Rating' in reply['invitations']:
                ratings.append(openreview.api.Note.from_json(reply))

'''for rating in ratings:
    print(rating.content['review_quality']['value'])'''
