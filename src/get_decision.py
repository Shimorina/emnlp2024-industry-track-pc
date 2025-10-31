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
    notes = OR_CLIENT.get_all_notes(invitation=f"{VENUE_ID}/-/Submission", details='replies')
    submission_info = {} 
    for note in notes:
        # ignore withdrawn and desk-rejected papers
        if not note.content.get('venueid')['value'] == f'{VENUE_ID}' :
            continue

        authors = note.content.get('authors')['value']
        authorids = note.content.get('authorids')['value']
        #print("Authors ", authorids)
        profiles = openreview.tools.get_profiles(OR_CLIENT, authorids, with_preferred_emails='{VENUE_ID}/-/Preferred_Emails')
        #names = [profile.content['names'][0]['fullname'] for profile in profiles]
        emails = [profile.get_preferred_email() for profile in profiles]
        
        #submission_id = note.content.get('paperhash')['readers'][1].split('/')[3]
        #get review ratings
        # for each submission get replies that have the Rating invitation
        reply_rating = [reply for reply in note.details["replies"] if any(invitation.endswith("/-/Official_Review") for invitation in reply['invitations'])]
        #print("reply_rating ", reply_rating)
        # for each rating get the reviewer that's being evaluated
        reviewer_ratings=[]
        for reply in reply_rating:
            # add the rating to the reviewer_ratings list
            reviewer_ratings.append(reply['content']['rating']['value'])
        avg = sum(reviewer_ratings) / float(len(reviewer_ratings))
        submission_info[note.number] = [
            avg,
            note.number,
            note.content.get('title')['value'],
            ', '.join(authors),
            ', '.join(authorids)
            # note.content.get('TLDR')['value']
        ]
    return submission_info

def get_decision_from_or():
    venue_group = OR_CLIENT.get_group(VENUE_ID)
    #print("venue_group content: ",venue_group.content.keys())
    submission_name = venue_group.content['submission_name']['value']
    submissions = OR_CLIENT.get_all_notes(invitation=f'{VENUE_ID}/-/{submission_name}', details='replies')
    
    print("submissions", type(submissions))
    decisions = [openreview.api.Note.from_json(reply) for s in submissions for reply in s.details['replies']
               if any(invitation.endswith("Decision") for invitation in reply['invitations'])]
    #replies = [reply for s in submissions for reply in s.details['replies'] if any(invitation.endswith(reply_type) for invitation in reply['invitations'])]
    print('# of reviews submitted:', len(decisions))
    return decisions


def write_meta_reviews_to_csv(reviews,submissions):
    invitation = OR_CLIENT.get_invitation(f'{VENUE_ID}/-/Decision')
    content = invitation.edit['invitation']['edit']['note']['content']
    # print(content)
    keylist = list(content.keys())

    decisions = {} 
    header = []
    for review in reviews:
        submission_id = review.invitations[0].split('/')[3]
        paper_id=int(submission_id[10:])
        decinfo=[]
        header=keylist+["Score","Id","Title","Authors","Authors_ids"]
        for key in keylist:
            value = review.content.get(key)
            if value is not None and 'value' in value:
                if review.content.get(key)['value']:
                    decinfo.append(review.content.get(key)['value'])
                else:
                    decinfo.append('')
            else:
                # Handle the case where value is None or 'value' key is missing
                # print(key, value)
                decinfo.append('')

        if paper_id not in submissions :
            print (" WARNING Paper %d not in the submissions ",paper_id)
            continue
        decinfo.extend(submissions[paper_id])
        decisions[paper_id]=decinfo.copy()



    with open('../data/decisions.csv', 'w') as outfile:
        csvwriter = csv.writer(outfile, delimiter=',')
        # Write header
        t = csvwriter.writerow(header)
        for ppid in decisions.keys():
            decinfo=decisions[ppid]
            s = csvwriter.writerow(decinfo)

if __name__ == "__main__":
    submissions=get_submissions()
    print(type(submissions))
    print("total of submissions: ",len(submissions.keys()))
    decisions= get_decision_from_or()
    write_meta_reviews_to_csv(decisions,submissions)
    print(len(decisions))
