#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
from collections import defaultdict
import csv
import openreview
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT
from utils import get_timestamp


def get_accepted_info():
    OR_CLIENT.impersonate(VENUE_ID)
    print("Venue ID ", VENUE_ID)
    submissions = OR_CLIENT.get_all_notes(content={'venueid': VENUE_ID})
    submission_info = defaultdict(list)
    for note in submissions:
        authors = note.content.get('authors')['value']
        authorids = note.content.get('authorids')['value']
        emails = []
        affiliations=[]
        domains=[]
        countries=[]
        for authorid in authorids:
            if authorid.startswith('~'):
                profile_with_emails = OR_CLIENT.search_profiles(ids=[authorid])
                try:
                    emails.append(profile_with_emails[0].content['preferredEmail'])
                except KeyError:
                    emails.append(profile_with_emails[0].content['emails'][0])
                    print("KeyError")
            else:
                emails.append(authorid)
                #profile = openreview.tools.get_profile(OR_CLIENT,authorid)
                if 'history' in profile_with_emails[0].content.keys():
                    affiliations.append(profile_with_emails[0].content['history'][0]['institution']['name'])
                    domains.append(profile_with_emails[0].content['history'][0]['institution']['domain'])
                    if 'country' in profile_with_emails[0].content['history'][0]['institution'].keys():
                        countries.append(profile_with_emails[0].content['history'][0]['institution']['country'])
                    elif 'city' in profile_with_emails[0].content['history'][0]['institution'].keys():
                        countries.append(profile_with_emails[0].content['history'][0]['institution']['city'])
        if note.number=='455':
            continue
        submission_info[note.number] = [
            note.content.get('title')['value'],
            # ', '.join(note.content.get('keywords')['value']),
            ', '.join([text.title() for text in authors]),
            ', '.join(authorids),
            ', '.join(emails),
            ', '.join(affiliations),
            ', '.join(domains),
            ', '.join(countries)
        ]

    print("submission length :",len(submission_info.keys()))

    with open(f'../data/accepted-papers-{get_timestamp()}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['paper-id', 'title','authors', 'authorids', 'emails','affiliation','domain','country'])
        for k, v in sorted(submission_info.items()):
            writer.writerow([k, *v])


get_accepted_info()
