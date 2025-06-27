#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
from openreview_client import OR_CLIENT
from openreview_client import VENUE_ID
import argparse


def get_reviewer_profiles(reviewer_type):
    reviewer_group = OR_CLIENT.get_group(f'{VENUE_ID}/{reviewer_type}')
    # print(reviewer_group['members'])
    profiles = openreview.tools.get_profiles(
        OR_CLIENT,
        ids_or_emails=reviewer_group.members,
        with_publications=True)
    # print(profiles[0])
    print("Total of reviewers : ", len(profiles))
    rev_with_less_than_three_pub = 0
    for profile in profiles:
        print(profile.id)
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
        #    print(profile.id)
        # conditions to check
        # 3 recent publications (2019-2024)
    print('reviewers with less than 3 pubs : ',rev_with_less_than_three_pub)


# 25 reviewers with 0 papers
# 93 people with less than 4 papers -> 77 people as of 25/07
# 152 reviewers with no SS
# 195 reviewers with no ACL Anthology profile
# 73 reviewers with no dblp
# todo: extract reviewers: name, email, highest degree (year of earning), SS, dblp, acl anthology, gscholar, n of papers uploaded to OpenReview



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=str, default='r',help='mr for meta-reviewer')
    args = parser.parse_args()

    print('type r or mr : ',args.type)
    if args.type=='mr':
        get_reviewer_profiles(reviewer_type='Area_Chairs')
    else:
        get_reviewer_profiles(reviewer_type='Reviewers')
            
    
