#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
from openreview_client import OR_CLIENT
from openreview_client import VENUE_ID


def get_authors():
    """
    Extract all authors with OR profiles and take people with more than 5 publications in their profiles.
    :return:
    """
    notes = OR_CLIENT.get_all_notes(invitation=f"{VENUE_ID}/-/Submission")
    author_or_profiles = []
    profile_names = []
    author_submission_number = {}  # track submission number to send emails later
    for note in notes:
        # ignore withdrawn and desk-rejected papers
        if not note.content.get('venueid')['value'] == f'{VENUE_ID}/Submission':
            continue
        authorids = note.content.get('authorids')['value']
        # profile_names += [authorid for authorid in authorids if '@' not in authorid]
        for authorid in authorids:
            if '@' not in authorid:
                author_submission_number[authorid] = note.number
                profile_names.append(authorid)
    print('Authors with OR profile:', len(profile_names))
    profiles = openreview.tools.get_profiles(OR_CLIENT,
                                             ids_or_emails=profile_names,
                                             with_publications=True)
    for profile in profiles:
        pub_number = len(profile.content['publications'])
        if pub_number > 5:
            author_or_profiles.append(profile)
    print('Authors with OR profile and more than 5 publications:', len(author_or_profiles))
    return author_or_profiles, author_submission_number


def get_reviewers(reviewer_type):
    """
    Extract current reviewers and area chairs.
    :return:
    """
    reviewer_group = OR_CLIENT.get_group(f'{VENUE_ID}/{reviewer_type}')
    # print(reviewer_group['members'])
    profiles = openreview.tools.get_profiles(OR_CLIENT, ids_or_emails=reviewer_group.members)
    profiles_ids = [profile.id for profile in profiles]
    return profiles_ids


def filter_authors():
    """
    Remove authors if they are already reviewing/ACing
    :return:
    """
    reviewers_ids = get_reviewers('Reviewers')
    ac_ids = get_reviewers('Area_Chairs')
    authors_profiles, author_submission_numbers = get_authors()
    author_filtered = []
    for author_profile in authors_profiles:
        if author_profile.id not in reviewers_ids and author_profile.id not in ac_ids:
            author_filtered.append(author_profile)
    print('Emergency reviewer suggestions:', len(author_filtered))
    return author_filtered, author_submission_numbers


def send_invitation(profiles, author_submission_numbers):
    for profile in profiles:
        # print(profile.id, len(profile.content['publications']))
        # print(profile.content['preferredEmail'])
        # Examples of how names look like in OR:
        # {'fullname': 'Kelly Ting Wu',
        # 'preferred': False,
        # 'username': '~Kelly_Ting_Wu1'},
        # {'fullname': 'Ting Wu',
        # 'preferred': True,
        # 'username': '~Ting_Wu2'}],
        # [{'first': 'Alon', 'middle': 'Y.', 'last': 'Halevy', 'username': '~Alon_Y._Halevy1', 'fullname': 'Alon Y. Halevy'},
        # {'first': 'Alon', 'middle': 'Y.', 'last': 'Levy', 'username': '~Alon_Y._Levy1', 'fullname': 'Alon Y. Levy'}]
        '''
        'names': [{'first': 'Zheng',
                   'fullname': 'Zheng Xu',
                   'last': 'Xu',
                   'middle': '',
                   'preferred': False,
                   'username': '~Zheng_Xu2'},
                  {'first': 'Zheng',
                   'fullname': 'Zheng Xu',
                   'last': 'Xu',
                   'middle': '',
                   'preferred': False,
                   'username': '~Zheng_Xu4'}]
        '''
        # look for 'preferred' name
        first_name = 'Author'
        preferred_found = False
        if len(profile.content['names']) == 1:
            try:
                first_name = profile.content['names'][0]['first']
            except KeyError:
                first_name = profile.content['names'][0]['fullname']
        else:
            for name in profile.content['names']:
                if 'preferred' in name.keys():
                    if name['preferred']:
                        try:
                            first_name = name['first']
                        except KeyError:
                            first_name = name['fullname']
                        preferred_found = True
        if not preferred_found:
                try:
                    first_name = profile.content['names'][0]['first']
                except KeyError:
                    first_name = profile.content['names'][0]['fullname']
        if first_name == 'Author':
            print(f'\nCheck the following profile and the name extraction: {profile.id}')
            print(profile.content['names'])
        # print(first_name.title())
        message = f"Dear {first_name.title()},\n\n" \
                     f"We would like to thank you for submitting your work for the EMNLP 2024 Industry Track.\n\n" \
                     f"The Industry Track received a record number of over 330 paper submissions.\n\n" \
                     f"We would like to see if we can rely on your help, if needed, to perform emergency reviews (one or two) in the time period of 30 August to 4 September.\n" \
                     f"If you are able to help, please fill in this form by Thursday, 29 August: https://forms.gle/eq7vMgYvw7BKgbZC7" \
                     f"\n\n" \
                     f"Thank you,\n" \
                     f"The EMNLP 2024 Industry Track chairs"
        subject = '[EMNLP Industry Track 2024] Volunteering for Emergency Reviewing for EMNLP 2024 Industry Track Next Week'
        try:
            recipients = [profile.content['preferredEmail']]
        except KeyError:
            recipients = [profile.content['emailsConfirmed'][0]]
            # print(profile)
            # print(profile.content['emailsConfirmed'])
            # print(profile.content['emails'])
        # print(message, '\n\n')
        submission_number = ''
        try:
            submission_number = author_submission_numbers[profile.id]
        except KeyError:
            # extract other usernames and search there
            usernames = [username['username'] for username in profile.content['names']]
            print(usernames)
            for un in usernames:
                if un in author_submission_numbers.keys():
                    submission_number = author_submission_numbers[un]

        if not submission_number:
            print('Author was not found in submissions.', profile.id)
        parent_group = f'{VENUE_ID}/Submission{submission_number}/Authors'
        # uncomment the line below to send messages
        # OR_CLIENT.post_message(subject, recipients, message, parentGroup=parent_group,
        #                       replyTo='emnlp2024-industry-track@googlegroups.com')
        print(f'message sent to {profile.id}, {recipients}')
        print('\n\n')


def main():
    author_profiles, auth_subm_match = filter_authors()
    send_invitation(author_profiles, auth_subm_match)


if __name__ == "__main__":
    main()
