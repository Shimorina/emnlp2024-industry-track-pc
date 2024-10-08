#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT
import csv
from datetime import datetime


# Fetch all submissions for the venue
venue_group = OR_CLIENT.get_group(VENUE_ID)
submission_name = venue_group.content['submission_name']['value']
submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/{submission_name}', details='replies')


review_name = venue_group.content['review_name']['value']
meta_review_name = venue_group.content['meta_review_name']['value']
ethics_review_name = venue_group.content['ethics_review_name']['value']

# construct paper#, meta-review recommendation, note_review1, note_review2, note_review3, etc...
# todo: add AC name


papers_with_review_info = []
print('total submissions:', len(submissions))
count_withdrawn_deskrejected = 0
for submission in submissions:
    # exclude desk-rejected and withdrawn
    if submission.content['venueid']['value'] == f'{VENUE_ID}/Submission':
        title = submission.content['title']['value']
        submission_info = [submission.number, title]
        has_metareview = False
        has_ethics_review = False
        ethics_reviews = []
        for reply in submission.details['replies']:
            if f'{VENUE_ID}/{submission_name}{submission.number}/-/{review_name}' in reply['invitations']:
                review_note = openreview.api.Note.from_json(reply)
                reviewer_grade = review_note.content['rating']['value']
                submission_info.append(reviewer_grade)
            elif f'{VENUE_ID}/{submission_name}{submission.number}/-/{meta_review_name}' in reply['invitations']:
                metareview_note = openreview.api.Note.from_json(reply)
                metareviewer_grade = metareview_note.content['Paper_recommendation']['value']
                metareviewer_confidence = metareview_note.content['confidence']['value']
                metareviewer_id = metareview_note.signatures[0].split('_')[-1]
                submission_info.insert(2, metareviewer_grade)
                submission_info.insert(3, metareviewer_confidence)
                # submission_info.insert(4, metareviewer_id)
                has_metareview = True
            elif f'{VENUE_ID}/{submission_name}{submission.number}/-/{ethics_review_name}' in reply['invitations']:
                ethics_review_note = openreview.api.Note.from_json(reply)
                ethics_recommendation = ethics_review_note.content['recommendation']['value']
                ethics_reviews.append(ethics_recommendation)
                has_ethics_review = True
        if not has_metareview:
            submission_info.insert(2, 'None')
            submission_info.insert(3, 'None')
        if not has_ethics_review:
            submission_info.insert(4, 'NA')
        else:
            submission_info.insert(4, '\n'.join(ethics_reviews))
        papers_with_review_info.append(submission_info)
    else:
        count_withdrawn_deskrejected += 1
        if submission.number == 91:
            print(submission.number)

print('deskrejected/withdrawn:', count_withdrawn_deskrejected)
print('active submissions:', len(papers_with_review_info))

# Get the current date
current_date = datetime.now()

# Format the date as year-month-day
timestamp = current_date.strftime('%Y-%m-%d')

with open(f'data/reviews-{timestamp}.csv', 'w') as outfile:
    csvwriter = csv.writer(outfile, delimiter=',')
    csvwriter.writerow(['submission_id', 'title', 'AC_recommendation', 'AC_confidence', 'ethics_reviews',
                        'review_rating1',
                        'review_rating2', 'review_rating3', 'review_rating4', 'review_rating5',
                        'review_rating6', 'review_rating7', 'review_rating8'])
    csvwriter.writerows(papers_with_review_info)
