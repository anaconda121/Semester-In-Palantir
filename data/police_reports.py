import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

incident_types = [
    "Minor Threat",
    "Suspicious Activity",
    "Information",
    "Assistance Request",
    "Medical Aid",
    "Resolved",
]

priority_map = {
    "Minor Threat": 2,
    "Suspicious Activity": 3,
    "Medical Aid": 2,
    "Assistance Request": 3,
    "Information": 4,
    "Resolved": 4,
}

status_opts   = ["Dispatched", "En Route", "On Scene", "Closed", "Logged"]
radio_channels = ["PD1", "PD2", "FD1", "EMS1"]

locations = [
    ("Uris Library",        42.4475, -76.4854),
    ("Anabel Taylor Hall",  42.4493, -76.4835),
    ("North Campus Dorms",  42.4551, -76.4729),
    ("Kosher Dining Hall",  42.4498, -76.4821),
    ("Ho Plaza",            42.4479, -76.4840),
    ("Duffield Hall",       42.4448, -76.4847),
    ("Engineering Quad",    42.4440, -76.4830),
]

units_pool = [
    "Cornell CUPD Unit 1", "Cornell CUPD Unit 2", "Cornell CUPD Unit 3",
    "Cornell CUPD Unit 4", "Cornell CUPD Unit 5", "Cornell CUPD Unit 6",
    "Cornell CUPD Unit 7", "Ithaca PD Car 3",    "Ithaca PD Car 8",
    "Ithaca PD Car 12",    "Ithaca PD Car 14",   "Ithaca PD Car 21",
    "Ithaca FD Truck 1",   "Bangs EMS 902",
]

minor_bias_keywords = [
    "bias graffiti",
    "offensive flyer",
    "verbal harassment",
    "derogatory slur",
    "threatening note (non-violent)",
    "harassing email"
]

p_followup_positive = 0.15

rows = []
current_time = datetime(2023, 10, 25, 14, 0)

for idx in range(150):

    current_time += timedelta(minutes=int(np.random.randint(1, 9)))

    inc_type = random.choice(incident_types)
    loc_name, lat, lon = random.choice(locations)
    units = random.sample(units_pool, random.randint(1, 3))

    is_positive = False

    if inc_type == "Minor Threat":
        is_positive = True
        kw = random.choice(minor_bias_keywords)
        call_text = f"{kw.capitalize()} reported at {loc_name}."
    elif random.random() < p_followup_positive:
        is_positive = True
        call_text = (
            f"Follow-up patrol related to earlier bias incident at {loc_name}."
        )
    else:
        call_text = f"{inc_type} reported at {loc_name}."

    post_id = f"sm_{145900 + random.randint(0, 200)}" if is_positive else None

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

df = pd.DataFrame(rows)
df.to_csv("police_report_data.csv", index=False)
