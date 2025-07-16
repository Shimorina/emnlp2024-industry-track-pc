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

def updating_reduced_load(rload):

    #invitation=head+'/-/Custom_Max_Papers'
    #print("invitation : ", invitation)
    venue_group = OR_CLIENT.get_group(VENUE_ID)
    #print("content: ", venue_group)
    #print(type(venue_group.content['area_chairs_custom_max_papers_id']))
    #print(venue_group.content['area_chairs_custom_max_papers_id'])
    custom_max_papers_invitation_id = venue_group.content['area_chairs_custom_max_papers_id']['value']
    grouped_edges = OR_CLIENT.get_grouped_edges(
        invitation = custom_max_papers_invitation_id,
        groupby = 'tail' 
    )
    print("number of edges: ", len(grouped_edges))
    for edge in grouped_edges:
        nbACMin_w=0
        for value in  edge['values']:
            print("invitation : ",value['invitation'])
            if value['invitation']!= 'EMNLP/2025/Industry_Track/Area_Chairs/-/Custom_Max_Papers':
                continue
            print("profile id ", value['tail'])
            print("weight: ", value['weight'])
            if value['tail'] not in ('~Ondrej_Dusek1','~Johannes_Heinecke1') and value['weight']==10:
                print("NOT ENOUGH.... setting to 15")
                
                print("changing load of ", value['tail'])
                OR_CLIENT.post_edge(openreview.api.Edge(
                    invitation=value['invitation'],
                    head=VENUE_ID+'/Area_Chairs',
                    tail=value['tail'],
                    signatures=[VENUE_ID+'/Program_Chairs'],
                    weight=rload
                ))
                nbACMin_w+=1

        print("Total of AC with load lower than 5 ", nbACMin_w)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reduced_load", type=int , default=15)
    args = parser.parse_args()

    print('load : ',args.reduced_load)
    updating_reduced_load(args.reduced_load)





