#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
import openreview
import os
from dotenv import load_dotenv


load_dotenv()


OR_CLIENT = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username=os.getenv('OPENREVIEW_USERNAME'),
    password=os.getenv('OPENREVIEW_PASSWORD'),
)

VENUE_ID = "EMNLP/2025/Industry_Track"
