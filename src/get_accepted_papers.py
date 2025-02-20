#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
from collections import defaultdict
import csv
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT
from utils import get_timestamp


def get_accepted_info():
    submissions = OR_CLIENT.get_all_notes(content={'venueid': VENUE_ID})
    submission_info = defaultdict(list)
    for note in submissions:
        authors = note.content.get('authors')['value']
        authorids = note.content.get('authorids')['value']
        emails = []
        for authorid in authorids:
            if authorid.startswith('~'):
                profile_with_emails = OR_CLIENT.search_profiles(ids=[authorid])
                try:
                    emails.append(profile_with_emails[0].content['preferredEmail'])
                except KeyError:
                    emails.append(profile_with_emails[0].content['emails'][0])
            else:
                print('No OR id:', authorid)
                emails.append(authorid)
        submission_info[note.number] = [
            note.content.get('title')['value'],
            # ', '.join(note.content.get('keywords')['value']),
            note.content.get('abstract')['value'],
            ', '.join([text.title() for text in authors]),
            ', '.join(authorids),
            ', '.join(emails)
        ]

    with open(f'../data/accepted-papers-{get_timestamp()}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['submission-id', 'title', 'abstract', 'authors', 'authorids', 'emails'])
        for k, v in sorted(submission_info.items()):
            writer.writerow([k, *v])


get_accepted_info()
