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
import argparse

def getting_assigned_papers(rw_profile, rew):
    head=VENUE_ID+'/'+rew
    invitation=head+'/-/Assignment&tail='+rw_profile
    print("invitation : ", invitation)
    print("head : ", head)

    return OR_CLIENT.get_all_edges( invitation=invitation, tail=rw_profile)


def send_email_reviewer_subgroup(rev_group):
    """Send emails to reviewers who have less than 4 papers in their OR profile."""
    subject = '[EMNLP Industry Track 2025] papers has been assigned on OpenReview'
    parentGroup = f'{VENUE_ID}/{rev_group}'
    reviewers = OR_CLIENT.get_group(f'{VENUE_ID}/{rev_group}')
    profiles = openreview.tools.get_profiles(
        OR_CLIENT,
        ids_or_emails=reviewers.members,
        with_publications=True)
    for profile in profiles:
        # print(profile.id, len(profile.content['publications']))
        pub_number = len(profile.content['publications'])
        print("group : ", rev_group)
        print(profile.id, pub_number)
        print(profile.content['preferredEmail'])
        print("***KEYS****", profile.content.keys())
        print("keys: ", profile.content['names'])
        # look for 'preferred' name
        if rev_group=="Reviewers":
            first_name = "Reviewer" 
        else:
            first_name = "Area Chair"

        if len(profile.content['names']) == 1:
            try:
                first_name = profile.content['names'][0]['first']
            except KeyError:
                first_name = profile.content['names'][0]['fullname']
        else:
            for name in profile.content['names']:
                if 'preferred' in name.keys():
                    try:
                        first_name = name['first']
                    except KeyError:
                        first_name = name['fullname']
        print(first_name)
        if first_name == 'Reviewer':
            print(f'Check the following profile and the name extraction: {profile.id}')
            print(profile)
        #print("****Asigned Papers****")
        #edges=getting_assigned_papers(profile.id,rev_group)
        #print("type of edges : ",type(edges))
        #print("edges : ",edges)
        #print("****End Assigned Papers****")
        message = f'Dear {first_name},\n\n' \
                  f'Thank you for agreeing to serve on the EMNLP Industry Track this year!\n\n' \
                  f'You can now consult the assigned papers on OpenReview.\n' \
                  f'or check the assigned papers in : https://openreview.net/group?id=EMNLP/2025/Industry_Track/Reviewers#assigned-submissions \n\n' \
                  f'Thank you!\n\n' \
                  f'Best,\n' \
                  f'EMNLP Industry Track PC Chairs'
        recipients = [profile.id]
        invitation = VENUE_ID+'/-/Edit'
        print(message)
        # uncomment the line below to send messages
        OR_CLIENT.post_message(subject, recipients, message, invitation=invitation, parentGroup=parentGroup, replyTo='emnlp2025-industry-track@googlegroups.com')
        print(f'message {subject} sent to {profile.id}, {recipients}')
        print('\n\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rtype", type=str, default='r')
    args = parser.parse_args()
    print("rtype: ",args.rtype)
    if args.rtype == 'r':
        send_email_reviewer_subgroup(rev_group='Reviewers')
    else:
        send_email_reviewer_subgroup(rev_group='Area_Chairs')  # to see if ACs have their OR profile updated
