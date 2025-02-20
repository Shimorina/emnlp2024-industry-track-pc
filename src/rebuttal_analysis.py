#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT


submissions = OR_CLIENT.get_all_notes(
    invitation=f"{VENUE_ID}/-/Submission",
    details='replies'
)

# take all replies "rebuttal" with their ids. Loop through other replies to look for the same id in 'replyto'
rebuttals = []
count_paper_with_rebuttals = 0
rebuttal_response_found = 0  # calculate how many reviewers replied to rebuttal
official_comments_reply_id = []
count_confidential_comments = 0
for submission in submissions:
    rebuttals = rebuttals + [reply for reply in submission.details["replies"] if reply["invitations"][0].endswith("Rebuttal")]
    rebuttal_found = False
    for reply in submission.details["replies"]:
        if reply["invitations"][0].endswith("Rebuttal"):
            if not rebuttal_found:
                rebuttal_found = True
                count_paper_with_rebuttals += 1
        # collect all official comments and what they replied to
        elif reply["invitations"][0].endswith("Official_Comment") and 'Reviewer' in reply["writers"][1]:  # writers should be reviewers not authors
            official_comments_reply_id.append(reply['replyto'])   # id of what the official comment replies to
        # calculate how many confidential comments to AC/PC were left
        elif reply["invitations"][0].endswith("Official_Comment") and 'Authors' in reply["writers"][1]:
            if len(reply['readers']) <= 3:
                count_confidential_comments += 1



rebuttal_note_ids = [note['id'] for note in rebuttals]
# take only rebuttals with a reply from reviewers. i.e., the items that exist in both sets (rebuttals and official comments)
reviewers_replies_count = len(set(rebuttal_note_ids).intersection(set(official_comments_reply_id)))

# other_comments = set(rebuttal_note_ids).difference(set(official_comments_reply_id))

print('# of comments reviewers left:', len(official_comments_reply_id))  # 400, i.e. 53%
print('# of replies to rebuttal (by reviewers):', reviewers_replies_count)  # 193, i.e. 25.66% of rebuttals were answered


print('# Rebuttals:', len(rebuttals))  # 752 rebuttals were written
print('# papers with rebuttal:', count_paper_with_rebuttals)  # 249 papers who wrote rebuttal
print('% papers with rebuttal:', round(count_paper_with_rebuttals/318*100, 3))  # 78.302%

print('# of confidential comments to AC/PC:', count_confidential_comments)  # 55 comments
