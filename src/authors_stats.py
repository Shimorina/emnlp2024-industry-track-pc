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


def author_stats():
    subject = '[EMNLP Industry Track 2025] Author Rebuttal Period has started deadline 06/09/2025 23:59 GMT'
    recipients = [f'{VENUE_ID}/Authors']
    print(recipients)
    submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/Submission')
    author_list=[]
    print(len(submissions))
    for submission in submissions:

        recipients = submission.content['authorids']['value']
        print("recipients:", recipients)
        author_list.extend(recipients)

    print("total of authors: ", len(author_list))

if __name__ == "__main__":
    author_stats()
