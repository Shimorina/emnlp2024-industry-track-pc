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
        if not note.content.get('venueid')['value'] == f'{VENUE_ID}/Submission':
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
            note.number
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
    print(content.keys())
    keylist = list(content.keys())

    metarw = {} 
    header = []
    for review in reviews:
        submission_id = review.invitations[0].split('/')[3]
        paper_id=int(submission_id[10:])
        metarwinfo=[]
        if paper_id not in submissions :
            print (" WARNING Paper %d not in the submissions ", paper_id)
            continue

        metarwinfo.append(paper_id)
        header=["paper_number",	"decision","comment" ]
        for key in keylist:
            if key in ['confidence', 'Ethical_Considerations', 'Award_Nomination'] :
                continue 
            if key == "recommendation":
                value = review.content.get(key)
                if "Accept" in value['value']:
                    if paper_id in [200,1,153,90,146,241,150,448,187,305,120,270,256,414,291,71,278,145]:
                        metarwinfo.append("Accept (Oral)")
                    else:
                        metarwinfo.append("Accept (Poster)")
                else:
                        metarwinfo.append("Reject")


            if key != 'forum' and key != 'submission_id' and key !="recommendation":
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
        
        metarw[paper_id]=metarwinfo.copy()



    with open('../data/all_meta_reviews.csv', 'w') as outfile:
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
