#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Lina Rojas, Orange Research
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
import csv
from collections import defaultdict
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT

def get_submissions():
    OR_CLIENT.impersonate(VENUE_ID)
    notes = OR_CLIENT.get_all_notes(invitation=f"{VENUE_ID}/-/Submission")
    submission_info = {} 
    for note in notes:
        # ignore withdrawn and desk-rejected papers
        if not note.content.get('venueid')['value'] == f'{VENUE_ID}/Submission':
            continue
        authors = note.content.get('authors')['value']
        authorids = note.content.get('authorids')['value']
        #print("Authors ", authorids)
        profiles = openreview.tools.get_profiles(OR_CLIENT, authorids, with_preferred_emails='{VENUE_ID}/-/Preferred_Emails')
        #names = [profile.content['names'][0]['fullname'] for profile in profiles]
        emails = [profile.get_preferred_email() for profile in profiles]
        
        #submission_id = note.content.get('paperhash')['readers'][1].split('/')[3]
        submission_info[note.number] = [
            note.number,
            note.content.get('title')['value'],
            ', '.join(authors),
            ', '.join(emails),
            ', '.join(authorids),
            note.content.get('abstract')['value']
            # note.content.get('TLDR')['value']
        ]
    return submission_info

def get_meta_reviews_from_or():
    venue_group = OR_CLIENT.get_group(VENUE_ID)
    #print("venue_group content: ",venue_group.content.keys())
    submission_name = venue_group.content['submission_name']['value']
    submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/{submission_name}', details='replies')
    meta_review_name = venue_group.content['meta_review_name']['value']
    print("submissions", type(submissions))
    reviews = [openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies']
               if f'{VENUE_ID}/{submission_name}{s.number}/-/{meta_review_name}' in reply['invitations']]
    print('# of reviews submitted:', len(reviews))
    return reviews


def write_meta_reviews_to_csv(reviews,submissions):
    invitation = OR_CLIENT.get_invitation(f'{VENUE_ID}/-/Meta_Review')
    content = invitation.edit['invitation']['edit']['note']['content']
    # print(content)
    keylist = list(content.keys())

    metarw = {} 
    header = []
    for review in reviews:
        submission_id = review.invitations[0].split('/')[3]
        paper_id=int(submission_id[10:])
        metarwinfo=[]
        header=keylist[1:]+["Id","Title","Authors","Emails","Authors_ids","Abstract"]
        rejected=False
        for key in keylist:
            if key == 'metareview':
                continue
            if key == 'recommendation':
                value = review.content.get(key)
                if value['value']=="Reject":
                    rejected=True
                    break 

            if key != 'forum' and key != 'submission_id':
                value = review.content.get(key)
                if value is not None and 'value' in value:
                    if review.content.get(key)['value']:
                        metarwinfo.append(review.content.get(key)['value'])
                    else:
                        metarwinfo.append('')
                else:
                    # Handle the case where value is None or 'value' key is missing
                    # print(key, value)
                    metarwinfo.append('')
        if rejected:
            continue
        if paper_id not in submissions :
            print (" WARNING Paper %d not in the submissions ", paper_id)
            continue
        metarwinfo.extend(submissions[paper_id])
        metarw[paper_id]=metarwinfo.copy()



    with open('../data/meta_reviews.csv', 'w') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        # Write header
        t = csvwriter.writerow(header)
        for ppid in metarw.keys():
            metarwinfo=metarw[ppid]
            s = csvwriter.writerow(metarwinfo)

if __name__ == "__main__":
    submissions=get_submissions()
    print(type(submissions))
    print(len(submissions.keys()))
    metarws= get_meta_reviews_from_or()
    write_meta_reviews_to_csv(metarws,submissions)
    #print(len(get_reviews_from_or()))
