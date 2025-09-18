#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
import csv
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT


def get_reviews_from_or():
    venue_group = OR_CLIENT.get_group(VENUE_ID)
    print("venue_group content: ",venue_group.content.keys())
    submission_name = venue_group.content['submission_name']['value']
    submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/{submission_name}', details='replies')
    review_name = venue_group.content['review_name']['value']

    reviews = [openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies']
               if f'{VENUE_ID}/{submission_name}{s.number}/-/{review_name}' in reply['invitations']]
    print('# of reviews submitted:', len(reviews))
    # print(reviews[0])
    return reviews


def write_reviews_to_csv(reviews):
    invitation = OR_CLIENT.get_invitation(f'{VENUE_ID}/-/Official_Review')
    content = invitation.edit['invitation']['edit']['note']['content']
    # print(content)
    keylist = list(content.keys())

    with open('../data/reviews.csv', 'w') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        # Write header
        keylist.insert(0, 'forum')
        keylist.insert(1, 'submission_id')
        t = csvwriter.writerow(keylist)
        for review in reviews:
            valuelist = []
            valuelist.append(review.forum)
            #  'invitations': ['EMNLP/2024/Industry_Track/Submission296/-/Official_Review']
            submission_id = review.invitations[0].split('/')[3]
            valuelist.append(submission_id)
            for key in keylist:
                if key != 'forum' and key != 'submission_id':
                    value = review.content.get(key)
                    if value is not None and 'value' in value:
                        if review.content.get(key)['value']:
                            valuelist.append(review.content.get(key)['value'])
                        else:
                            valuelist.append('')
                    else:
                        # Handle the case where value is None or 'value' key is missing
                        # print(key, value)
                        valuelist.append('')
            s = csvwriter.writerow(valuelist)


def main():
    write_reviews_to_csv(get_reviews_from_or())


if __name__ == "__main__":
    main()
