#  -------------------------------  Copyright ---------------------------------
#  Software Name: <software name>
#  Version: <version>
#  Author: Anastasia Shimorina, Orange Innovation
#  Software description: <optional: software description text>
#  ----------------------------------------------------------------------------
from datetime import datetime


def get_timestamp():
    # Get the current date
    current_date = datetime.now()

    # Format the date as year-month-day
    timestamp = current_date.strftime('%Y-%m-%d')
    return timestamp
