import random, numpy as np, pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# initialize faker and set random seeds
fake = Faker()
random.seed(2025); np.random.seed(2025)

# possible platforms
PLATFORMS = ["twitter", "reddit"]

# locations, courses, dining halls, bus routes
PLACES = ["104 West"]
COURSES = ["CS 2110", "ECE 2300", "Info 2950", "MATH 2940", "BIOG 1500"]
DINING = ["North Star", "Rose", "Morrison", "Okenshields", "Becker"]
TCAT_RTS = ["10", "30", "32", "51", "90"]

# keywords for threats and rumors
THREAT_KW = ["bomb", "shoot", "attack", "kill", "massacre", "explode"]
RUMOR_KW = ["lockdown", "evacuate", "gas leak", "virus", "outbreak", "fire"]

# emojis and hashtags for post styling
EMOJIS = ["😱", "📢", "🚨", "😳", "🙏", "😰", "🤔", "🔥", "😭", "🤯", "😂"]
HASHTAGS = ["#Cornell", "#Ithaca", "#GoBigRed", "#CampusSafety",
            "#Breaking", "#StaySafe", "#RumorMill"]

# helper to randomly pick hashtags
def h(k=2):
    return " ".join(random.sample(HASHTAGS, k))

# templates for explicit threats
EXPLICIT_THREAT_TMPLS = [
    "{emoji} I WILL {kw} everyone in {loc} at 9pm tonight.",
    "Tomorrow at noon I'm going to {kw} the {loc}. No joke.",
    "Count down: 3 hours until I {kw} {loc}. Try and stop me.",
    "Heads up losers, {loc} gets {kw}ed at sunset. 🔥",
    "Putting a {kw} in {loc} after lecture - watch me."
]

# templates for rumor-based threats
RUMOR_THREAT_TMPLS = [
    "{emoji} hearing someone gonna {kw} {loc} tmrw… legit??",
    "Just saw a post abt a plan to {kw} at {loc}. {emoji}",
    "any truth to the {kw} threat near {loc}? {tags}",
    "Rumor mill says {kw} plot brewing @ {loc}. Why no alert yet??",
    "If you’re on {loc} you better dip rn {tags3}"
]

# generate a random threat text
def make_threat_text() -> str:
    kw = random.choice(THREAT_KW + RUMOR_KW)
    loc = random.choice(PLACES)

    if random.random() < 0.50:
        tmpl = random.choice(EXPLICIT_THREAT_TMPLS).format(
            kw=kw, loc=loc,
            emoji=random.choice(EMOJIS)
        )
    else:
        tmpl = random.choice(RUMOR_THREAT_TMPLS).format(
            kw=kw, loc=loc,
            emoji=random.choice(EMOJIS),
            tags=h(),
            tags3=h(3)
        )
    return tmpl[:280]

# functions to generate neutral (non-threat) text
def neutral_housing():
    return random.choice([
        f"Last-minute housing advice? Everything in Collegetown seems gone by {random.choice(['October', 'November'])}.",
        f"Accepted to Cornell! How bad is noise at {random.choice(['Edgemoor', 'Low Rise 7', 'Donlon'])}?",
        f"Can I still find a lease for fall near CTB or am I doomed? 😭",
    ])

def neutral_dining():
    return random.choice([
        f"Rank your top 3 dining halls – is {random.choice(DINING)} still undefeated? 😂",
        f"Is it true {random.choice(DINING)} switched to paper plates again?? {random.choice(HASHTAGS)}",
        f"Best place for late-night food past 10? Asking for a friend.",
    ])

def neutral_transport():
    rt = random.choice(TCAT_RTS)
    return random.choice([
        f"PSA: TCAT Route {rt} skipping North tonight due to snow. Plan accordingly.",
        f"IF YOU’RE LEAVING ON THE COMMONS BUS BE THERE 5 MIN EARLY OR YOU’LL BE STRANDED – learned the hard way 🚨",
    ])

def neutral_academic():
    return random.choice([
        f"Anyone else drowning in {random.choice(COURSES)} this week? office hours packed.",
        f"Where do you print posters in time for Friday’s {random.choice(['ClubFest','research symposium'])}?",
    ])

def neutral_misc():
    return random.choice([
        f"Lost my {random.choice(['wallet','AirPods','ID'])} on Uris steps – reward = CTB cookie 🙏",
        f"Is the CTB line ever <30 min? Serious question.",
        f"What’s the deal with fireworks over West Campus last night?",
    ])

# list of neutral text generators
NEUTRAL_FUNCS = [neutral_housing, neutral_dining, neutral_transport,
                 neutral_academic, neutral_misc]

# randomly pick a neutral text
def make_neutral_text() -> str:
    return random.choice(NEUTRAL_FUNCS)()[:280]

# generate a random timestamp between start and end
def random_timestamp(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# main simulation function
def simulate(n_posts: int = 3000, threat_ratio: float = 0.6) -> pd.DataFrame:
    start = datetime(2023, 10, 25)
    end = datetime(2023, 10, 31)

    rows = []
    for i in range(n_posts):
        label = int(random.random() < threat_ratio)
        platform = random.choice(PLATFORMS)
        post_id = f"P{i:06d}"
        user_id = fake.uuid4()
        ts = random_timestamp(start, end).isoformat()

        if random.random() < 0.30:
            lat = 42.453 + np.random.normal(scale=0.005)
            lon = -76.473 + np.random.normal(scale=0.005)
        else:
            lat, lon = float(fake.latitude()), float(fake.longitude())

        text = make_threat_text() if label else make_neutral_text()

        rows.append(dict(post_id=post_id, platform=platform, timestamp=ts,
                         user_id=user_id, text=text,
                         latitude=lat, longitude=lon))
    return pd.DataFrame(rows)

# run and save output when executed as main
if __name__ == "__main__":
    df = simulate()
    df.to_csv("cornell_social_media_text_explicit.csv", index=False)
    print(df.head().to_markdown())
