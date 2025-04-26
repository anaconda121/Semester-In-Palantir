import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

# define possible incident types
incident_types = [
    "Minor Threat",
    "Suspicious Activity",
    "Information",
    "Assistance Request",
    "Medical Aid",
    "Resolved",
]

# map incident types to priority levels
priority_map = {
    "Minor Threat": 2,
    "Suspicious Activity": 3,
    "Medical Aid": 2,
    "Assistance Request": 3,
    "Information": 4,
    "Resolved": 4,
}

# define possible status updates and radio channels
status_opts   = ["Dispatched", "En Route", "On Scene", "Closed", "Logged"]
radio_channels = ["PD1", "PD2", "FD1", "EMS1"]

# define possible locations with lat/lon
locations = [
    ("Uris Library",        42.4475, -76.4854),
    ("Anabel Taylor Hall",  42.4493, -76.4835),
    ("North Campus Dorms",  42.4551, -76.4729),
    ("Kosher Dining Hall",  42.4498, -76.4821),
    ("Ho Plaza",            42.4479, -76.4840),
    ("Duffield Hall",       42.4448, -76.4847),
    ("Engineering Quad",    42.4440, -76.4830),
]

# define available police, fire, ems units
units_pool = [
    "Cornell CUPD Unit 1", "Cornell CUPD Unit 2", "Cornell CUPD Unit 3",
    "Cornell CUPD Unit 4", "Cornell CUPD Unit 5", "Cornell CUPD Unit 6",
    "Cornell CUPD Unit 7", "Ithaca PD Car 3",    "Ithaca PD Car 8",
    "Ithaca PD Car 12",    "Ithaca PD Car 14",   "Ithaca PD Car 21",
    "Ithaca FD Truck 1",   "Bangs EMS 902",
]

# keywords to simulate bias-related minor threats
minor_bias_keywords = [
    "bias graffiti",
    "offensive flyer",
    "verbal harassment",
    "derogatory slur",
    "threatening note (non-violent)",
    "harassing email"
]

# probability that a non-minor-threat gets linked to a follow-up
p_followup_positive = 0.15

# initialize rows and starting timestamp
rows = []
current_time = datetime(2023, 10, 25, 14, 0)

# simulate 150 incident records
for idx in range(150):

    # increment time randomly between 1 and 8 minutes
    current_time += timedelta(minutes=int(np.random.randint(1, 9)))

    # randomly choose incident type and location
    inc_type = random.choice(incident_types)
    loc_name, lat, lon = random.choice(locations)
    units = random.sample(units_pool, random.randint(1, 3))

    is_positive = False

    # if minor threat, it's a positive label
    if inc_type == "Minor Threat":
        is_positive = True
        kw = random.choice(minor_bias_keywords)
        call_text = f"{kw.capitalize()} reported at {loc_name}."
    # some other cases can randomly be linked to bias follow-up
    elif random.random() < p_followup_positive:
        is_positive = True
        call_text = (
            f"Follow-up patrol related to earlier bias incident at {loc_name}."
        )
    else:
        call_text = f"{inc_type} reported at {loc_name}."

    # if incident is linked to social media, generate a fake id
    post_id = f"sm_{145900 + random.randint(0, 200)}" if is_positive else None

    # append row
    rows.append(
        {
            "cad_event_id": f"CU-20231029-{idx + 1:03d}",
            "timestamp": current_time,
            "incident_type": inc_type,
            "priority": priority_map[inc_type],
            "radio_channel": random.choice(radio_channels),
            "location": loc_name,
            "geo_lat": lat,
            "geo_lon": lon,
            "units_dispatched": units,
            "call_text": call_text,
            "status": random.choice(status_opts),
            "linked_social_media_post_id": post_id,
            "label": int(is_positive)
        }
    )

# convert to dataframe and save as csv
df = pd.DataFrame(rows)
df.to_csv("police_report_data.csv", index=False)
