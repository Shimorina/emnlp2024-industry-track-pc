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
    subject = '[EMNLP Industry Track 2025] URGENT Please complete the survey!!!'
    submissions = OR_CLIENT.get_all_notes(content={'venueid':f'{VENUE_ID}'})
    print(len(submissions))
    for submission in submissions:
        #not_completed=[293,368,257,386,214,104,82,266]
        not_completed=[336]

        message = f'Dear authors, \n To facilitate the planning of our poster sessions and gather necessary information for visa support, please complete the following form as soon as possible (complete the form only ONCE per paper):\n https://docs.google.com/forms/d/e/1FAIpQLSfTq6eLR9H8hLzyiah-1QvRua1-V_MpWjP_55znBhXtd-mSwA/viewform?usp=header\n\n **Important Visa Information:**\n - If you require a visa invitation letter, please refer to the official EMNLP 2025 FAQ, specifically the section: "Where can I get a Visa invitation letter?" (https://2025.emnlp.org/faq/)\n - We also encourage you to check the latest entry requirements. Some nationalities may be eligible for a 30-day visa-free entry or a 10-Day (240-Hour) Visa-Free Transit, and it is important to verify your specific situation. You can check https://2025.emnlp.org/visa/ for more information.\n\n Please note that the deadline was on September the 30th 23:59 GMT. \n Kind Regards. \n The EMNLP 2025 Industry Track Program Chairs.'
        #print("Subject :", subject)
        #print("Message :", message)
        #print("Content:", submission.content)
        submission_id= submission.content['paperhash']['readers'][1].split('/')[3]
        #print(submission_id)
        paper_id=int(submission_id[10:])
        #print(paper_id)
        recipients = submission.content['authorids']['value']
        #print(recipients)
        if paper_id in not_completed:
            print("not completed : ", paper_id)
            OR_CLIENT.post_message(subject, recipients, message, invitation=f'{VENUE_ID}/-/Edit')

if __name__ == "__main__":
    send_email_authors()
