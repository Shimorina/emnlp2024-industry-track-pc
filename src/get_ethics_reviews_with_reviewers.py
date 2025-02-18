#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  SPDX-FileCopyrightText: Copyright (c) 2024 Orange Innovation
#
#  This software is confidential and proprietary information of Orange Innovation. You shall not disclose such
#  Confidential Information and shall not copy, use or distribute it in whole or in part without the prior written
#  consent of Orange Innovation.
#
#  Author: Anastasia Shimorina, Orange Innovation, DATAAI/AITT/Deskiñ
#  Email: anastasia.shimorina@orange.com
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
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
from utils import get_timestamp


def get_reviews_and_reviewers():
    venue_group = OR_CLIENT.get_group(VENUE_ID)

    # names for submission and reviews
    submission_name = venue_group.content['submission_name']['value']
    ethics_review_name = venue_group.content['ethics_review_name']['value']

    submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/{submission_name}', details='replies')

    reviews_with_reviewers = []
    all_submitted_reviewers = set()
    for submission in submissions:
        if 'flagged_for_ethics_review' in submission.content:
            # Assigned reviewers per submission
            submission_reviewers = OR_CLIENT.get_group(f'{VENUE_ID}/{submission_name}{submission.number}/Ethics_Reviewers')
            # Replies
            # sift through the replies for the official reviews (maybe useful if I want to compute interactions as well)
            # reviews = [r for r in submission.details['directReplies'] if f'{venue_id}/{submission_name}{submission.number}/-/{review_name}' in r['invitations']]
            # direct reviews from notes
            reviews = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/{submission_name}{submission.number}/-/{ethics_review_name}')
            # print(f'Reviews per submission {submission.number}:', len(reviews))
            # the review note has a field called "signatures" that contains a group id,
            # if you get that group then you can check its member that must contain the profile id of the reviewer that posted that review.
            for review in reviews:
                rev_signature = review.signatures[0]  # e.g., 'EMNLP/2024/Industry_Track/Submission000/Reviewer_XXX'
                group = OR_CLIENT.get_group(rev_signature)
                reviewer = group.members[0]
                all_submitted_reviewers.add(reviewer)
                try:
                    reviews_with_reviewers.append([submission.number,
                                                   submission.content['title']['value'],
                                                   reviewer,
                                                   review.content['ethics_review']['value'],
                                                   review.content['recommendation']['value']
                                                   ]
                                                  )
                # we added the Ethics field later, so there were some reviews posted without the Ethics field
                except KeyError:
                    print(review)

    # get all reviewers who accepted to review and identify people who didn't submit any review at the end
    reviewer_group = OR_CLIENT.get_group(f'{VENUE_ID}/Ethics_Reviewers')
    all_reviewers = reviewer_group.members
    print('All ethics reviewers registered', len(all_reviewers))  # 430 reviewers (incl. emergency)
    print('Ethics Reviewers who submitted:', len(all_submitted_reviewers))  # 384 reviewers
    with open(f'../data/ethics-reviewers-{get_timestamp()}.txt', 'w') as f:
        for rev in sorted(all_submitted_reviewers):
            f.write(f'{rev}\n')

    revs_not_submitted = set(all_reviewers).difference(all_submitted_reviewers)
    with open(f'../data/ethics-reviewers-not-submitted-{get_timestamp()}.txt', 'w') as f:
        for rev in sorted(revs_not_submitted):
            f.write(f'{rev}\n')
    print('Ethics Reviewers who registered but did not submit', len(revs_not_submitted))  # 47

    with open(f'../data/ethics-reviews-and-reviewers-{get_timestamp()}.csv', 'w') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        csvwriter.writerow(['submission_id', 'title', 'reviewer', 'review', 'recommendation'])
        csvwriter.writerows(reviews_with_reviewers)


get_reviews_and_reviewers()
