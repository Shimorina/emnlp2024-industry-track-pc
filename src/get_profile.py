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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mail", type=str)
    args = parser.parse_args()
    print('email : ',args.mail)
    profile = openreview.tools.get_profile(OR_CLIENT,args.mail)
    print('profile : ',profile.id)
    print(profile.content.keys())
    print('gscholar :',profile.content['gscholar'])





