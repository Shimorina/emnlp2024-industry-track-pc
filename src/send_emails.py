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


def send_email_reviewer_subgroup(rev_group='Reviewers'):
    """Send emails to reviewers who have less than 4 papers in their OR profile."""
    subject = '[EMNLP Industry Track 2024] please upload your papers to OpenReview'
    parentGroup = f'{VENUE_ID}/{rev_group}'
    reviewers = OR_CLIENT.get_group(f'{VENUE_ID}/{rev_group}')
    profiles = openreview.tools.get_profiles(
        OR_CLIENT,
        ids_or_emails=reviewers.members,
        with_publications=True)
    for profile in profiles:
        # print(profile.id, len(profile.content['publications']))
        pub_number = len(profile.content['publications'])
        if pub_number < 4:
        # if profile.id == '~Anastasia_Shimorina1':
            print(profile.id, pub_number)
            print(profile.content['preferredEmail'])
            print(profile.content['semanticScholar'])
            # {'fullname': 'Kelly Ting Wu',
            # 'preferred': False,
            # 'username': '~Kelly_Ting_Wu1'},
            # {'fullname': 'Ting Wu',
            # 'preferred': True,
            # 'username': '~Ting_Wu2'}],
            # look for 'preferred' name
            first_name = 'Reviewer'
            if len(profile.content['names']) == 1:
                try:
                    first_name = profile.content['names'][0]['first']
                except KeyError:
                    first_name = profile.content['names'][0]['fullname']
            else:
                for name in profile.content['names']:
                    if name['preferred']:
                        try:
                            first_name = name['first']
                        except KeyError:
                            first_name = name['fullname']
            if first_name == 'Reviewer':
                print(f'Check the following profile and the name extraction: {profile.id}')
                # print(profile)
            # print(first_name)
            message = f'Dear {first_name},\n\n' \
                      f'Thank you for agreeing to serve as Reviewer for the EMNLP Industry Track this year!\n\n' \
                      f'We see that you have {pub_number} paper(s) in your OpenReview profile. If you think this number is correct, please ignore this message.\n' \
                      f'If not, please check your OpenReview profile. Make sure that (1) you add a link to your DBLP profile, click "import papers from DBLP", ' \
                      f'and then delete any papers corresponding to areas you do not wish to review in; and (2) you add a link to your Semantic Scholar profile. ' \
                      f'The updated profile is critical for us to properly assign papers to you.\n\n' \
                      f'This guide to OpenReview may help you: https://docs.google.com/presentation/d/1CkfR94WxEPEZEyCN--ydC7K3wY4g-5ZiFd2HM8LRSXg/edit#slide=id.gf84c08a109_0_0 \n\n' \
                      f'Thank you!\n\n' \
                      f'Best,\n' \
                      f'EMNLP Industry Track PC Chairs'
            recipients = [profile.content['preferredEmail']]
            # print(message)
            # uncomment the line below to send messages
            # OR_CLIENT.post_message(subject, recipients, message, parentGroup=parentGroup,
            #                        replyTo='emnlp2024-industry-track@googlegroups.com')
            print(f'message sent to {profile.id}, {recipients}')
            print('\n\n')
            break


send_email_reviewer_subgroup(rev_group='Area_Chairs')
