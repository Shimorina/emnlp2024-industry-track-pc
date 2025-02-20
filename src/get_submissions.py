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
            with open(f'../data/paper{note.number}.pdf', 'wb') as op:
                op.write(f)'''
        '''if (note.content.get("supplementary_material")):
            f = client.get_attachment(note.id, 'supplementary_material')
            with open(f'../data/paper{note.number}_supplementary_material.zip', 'wb') as op:
                op.write(f)'''
    with open(f'../data/all-submissions-31-July-2024.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['submission-id', 'title', 'keywords', 'abstract', 'authors', 'authorids'])
        for k, v in sorted(submission_info.items()):
            writer.writerow([k, *v])


get_submissions()
