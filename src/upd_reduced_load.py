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
def updating_reduced_load(rw_profile, rload):
    client.post_edge(openreview.api.Edge(
        invitation=venue_id+'/Reviewers/-/Custom_Max_Papers',
        head=VENUE_ID+'/Reviewers',
        tail='~'+rw_profile,
        signatures=[venue_id+'/Program_Chairs'],
        weight=rload
    ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mail", type=str)
    parser.add_argument("reduced_load", type=int , default=1)
    args = parser.parse_args()

    print('email : ',args.mail)
    profile = openreview.tools.get_profile(OR_CLIENT,args.mail)
    print('profile : ',profile.id)
    print('load : ',args.reduced_load)
    #updating_reduced_load(profile.id, args.reduced_load)





