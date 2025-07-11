#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Lina Rojas, Orange Research 
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
import csv
from openreview_client import VENUE_ID
from openreview_client import OR_CLIENT
import argparse



# For Reviewers
def updating_reduced_load(rw_profile, rload, rtype):
    if rtype == 'r':
        rew="Reviewers"
    else:
        rew="Area_Chairs"

    head=VENUE_ID+'/'+rew
    invitation=head+'/-/Custom_Max_Papers'
    print("invitation : ", invitation)
    print("head : ", head)
        
    OR_CLIENT.post_edge(openreview.api.Edge(
        invitation=invitation,
        head=head,
        tail=rw_profile,
        signatures=[VENUE_ID+'/Program_Chairs'],
        weight=rload
    ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mail", type=str)
    parser.add_argument("reduced_load", type=int , default=1)
    parser.add_argument("rtype", type=str, default='r')
    args = parser.parse_args()

    print('email : ',args.mail)
    profile = openreview.tools.get_profile(OR_CLIENT,args.mail)
    print('profile : ',profile.id)
    print('load : ',args.reduced_load)
    print('rtype : ',args.rtype)
    updating_reduced_load(profile.id, args.reduced_load, args.rtype)





