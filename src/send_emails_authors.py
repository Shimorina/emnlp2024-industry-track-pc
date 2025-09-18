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


def send_email_authors():
    subject = '[EMNLP Industry Track 2025] Author Rebuttal Period has started deadline 06/09/2025 23:59 GMT'
    recipients = [f'{VENUE_ID}/Authors']
    print(recipients)
    submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/Submission')
    print(len(submissions))
    for submission in submissions:
        subject = f'Message regarding Submission #{submission.number}'
        message = f'Dear authors, \n Please go to your submission and prepare your response to ALL reviewers. \n Find your submission here: https://openreview.net/forum?id={submission.forum}, then click on the "Rebuttal" button at the top right and fill in the form with your responses. Please note that the deadline is on September the 6th 23:59 GMT. \n Kind Regards. \n The EMNLP 2025 Industry Track Program Chairs.'
        print("Subject :", subject)
        print("Message :", message)
        print("Content:", submission.content)

        recipients = submission.content['authorids']['value']
        OR_CLIENT.post_message(subject, recipients, message, invitation=f'{VENUE_ID}/-/Edit')

if __name__ == "__main__":
    send_email_authors()
