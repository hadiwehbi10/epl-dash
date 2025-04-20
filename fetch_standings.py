# fetch_standings.py
import requests
import re

API_URL = "https://api.football-data.org/v4/competitions/PL/standings"
FIXTURES_URL = "https://api.football-data.org/v4/competitions/PL/matches?status=SCHEDULED"
SCORERS_URL = "https://api.football-data.org/v4/competitions/PL/scorers"
API_TOKEN = "dc0b70d82c5e49a294eef0e12418207b"

HEADERS = {"X-Auth-Token": API_TOKEN}

def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def get_epl_standings():
    response = requests.get(API_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    standings = data["standings"][0]["table"]
    rows = []
    for team in standings:
        name = team["team"]["name"]
        logo = f"/assets/{slugify(name)}.png"
        rows.append({
            "Position": team["position"],
            "Team": {"name": name, "logo": logo},
            "Played": team["playedGames"],
            "Wins": team["won"],
            "Draws": team["draw"],
            "Losses": team["lost"],
            "Points": team["points"],
            "Goal Difference": team["goalDifference"]
        })
    return rows

def get_upcoming_fixtures():
    response = requests.get(FIXTURES_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    upcoming = data["matches"]
    gameday = upcoming[0]["matchday"] if upcoming else ""
    same_day = [m for m in upcoming if m["matchday"] == gameday]

    fixtures = []
    for match in same_day:
        fixtures.append({
            "home": match["homeTeam"]["name"],
            "away": match["awayTeam"]["name"],
            "date": match["utcDate"][:10],
            "time": match["utcDate"][11:16]
        })

    return gameday, fixtures

def get_top_scorers():
    
    response = requests.get(SCORERS_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    top = []
    for s in data["scorers"][:10]:
        top.append({
            "Player": s["player"]["name"],
            "Logo": f"/assets/{slugify(s['team']['name'])}.png",
            "Team": s["team"]["name"],
            "Goals": s["goals"]
        })
    return top
