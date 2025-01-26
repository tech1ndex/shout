import json
import time
from datetime import datetime

import requests
import vlc
import zoneinfo
from src.shout.settings import Settings

settings = Settings(
    api_url="https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?",
    team_name="Bills",
    victory_sound_path="/Users/tech1ndex/Desktop/GoBills.m4a",
    )

current_date = datetime.now(zoneinfo.ZoneInfo('America/New_York')).strftime("%Y%m%d")

def update_score() -> json:
    response = requests.get(f"{settings.api_url}/dates={current_date}", timeout=10)
    return response.json()

def get_team_score(data: json, team_name: str) -> dict | None:
    for event in data.get('events', []):
        competitions = event.get('competitions', [])
        for competition in competitions:
            competitors = competition.get('competitors', [])
            for competitor in competitors:
                if team_name.lower() in competitor['team']['name'].lower():
                    return {
                        'score': competitor['score'],
                    }
    return None


def main() -> None:
    current_score = int(get_team_score(data=update_score(), team_name=settings.team_name)['score'])
    print(f"Current score is: {current_score}")
    while True:
        live_score = int(get_team_score(data=update_score(), team_name=settings.team_name)['score'])
        if abs(live_score - current_score) > 1:
            print(f"Score has been updated to {live_score}")
            player = vlc.MediaPlayer(f'file://{settings.victory_sound_path}')
            player.play()
            current_score = live_score

            time.sleep(30) # Frequency to check the score

if __name__ == "__main__":
    main()
