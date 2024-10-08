#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
from collections import defaultdict
import csv
from openreview_client import OR_CLIENT
from openreview_client import VENUE_ID


def get_reviewer_profiles(reviewer_type):
    reviewer_group = OR_CLIENT.get_group(f'{VENUE_ID}/{reviewer_type}')
    # print(reviewer_group['members'])
    profiles = openreview.tools.get_profiles(
        OR_CLIENT,
        ids_or_emails=reviewer_group.members,
        with_publications=True)
    # print(profiles[0])
    rev_with_less_than_three_pub = 0
    for profile in profiles:
        content = {
          'authorids': profile.id
        }
        # print(profile.id, len(profile.content['publications']))
        pub_number = len(profile.content['publications'])
        # check if SS is linked
        if 'semanticScholar' in profile.content.keys():
            sem_scholar = True
            sem_scholar_profile = profile.content['semanticScholar']
        else:
            sem_scholar = False
            sem_scholar_profile = 'NA'
        if pub_number == 0:  # or not sem_scholar:
            rev_with_less_than_three_pub += 1
        # publications = openreview.tools.iterget_notes(client, content=content) #, invitation='dblp.org/-/record')
        # print(publications)
            # print(profile.id, pub_number, sem_scholar_profile)
            print(profile.id)
        # conditions to check
        # 3 recent publications (2019-2024)
    print(rev_with_less_than_three_pub)


# 25 reviewers with 0 papers
# 93 people with less than 4 papers -> 77 people as of 25/07
# 152 reviewers with no SS
# 195 reviewers with no ACL Anthology profile
# 73 reviewers with no dblp
# todo: extract reviewers: name, email, highest degree (year of earning), SS, dblp, acl anthology, gscholar, n of papers uploaded to OpenReview


# get_reviewer_profiles(reviewer_type='Reviewers')
# get_reviewer_profiles(reviewer_type='Area_Chairs')


def get_submissions(ignore_withdrawn_deskrejected=True):
    notes = OR_CLIENT.get_all_notes(invitation=f"{VENUE_ID}/-/Submission")
    submission_info = defaultdict(list)
    for note in notes:
        if ignore_withdrawn_deskrejected:
            # ignore withdrawn and desk-rejected papers
            if not note.content.get('venueid')['value'] == f'{VENUE_ID}/Submission':
                continue
        authors = note.content.get('authors')['value']
        authorids = note.content.get('authorids')['value']
        submission_info[note.number] = [
            note.content.get('title')['value'],
            ', '.join(note.content.get('keywords')['value']),
            note.content.get('abstract')['value'],
            ', '.join(authors),
            ', '.join(authorids)
            # note.content.get('TLDR')['value']
        ]

        '''if (note.content.get("pdf")):
            f = OR_CLIENT.get_attachment(note.id, 'pdf')
            with open(f'./submissions_31_July/paper{note.number}.pdf', 'wb') as op:
                op.write(f)'''
        '''if (note.content.get("supplementary_material")):
            f = client.get_attachment(note.id, 'supplementary_material')
            with open(f'./submissions/paper{note.number}_supplementary_material.zip', 'wb') as op:
                op.write(f)'''
    with open(f'./submissions_31_July/all-submissions-31-July-2024.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['submission-id', 'title', 'keywords', 'abstract', 'authors', 'authorids'])
        for k, v in sorted(submission_info.items()):
            writer.writerow([k, *v])


# get_submissions()
