import json
import time
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import vlc
import zoneinfo
from src.shout.logger import logger
from src.shout.settings import Settings

settings = Settings(
    api_url="https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?", # If using ESPN API
    team_name="Commanders", # Team name to track
    victory_sound_path="/Users/tech1ndex/Desktop/GoBills.m4a", # Path to sound file
    )

current_date = datetime.now(zoneinfo.ZoneInfo('America/New_York')).strftime("%Y%m%d")

def update_score() -> json:
    retry_strategy = Retry(
        total=3,
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    response = http.get(f"{settings.api_url}/dates={current_date}", timeout=10)
    return response.json()

def get_team_score(data: json, team_name: str) -> dict | None:
    for event in data.get('events', []):
        competitions = event.get('competitions', [])
        for competition in competitions:
            competitors = competition.get('competitors', [])
            for competitor in competitors:
                if team_name.lower() in competitor['team']['name'].lower():
                    return {
                        'team': competitor['team']['name'],
                        'score': competitor['score'],
                    }
    return None


def main() -> None:
    current_score = int(get_team_score(data=update_score(), team_name=settings.team_name)['score'])
    current_team = get_team_score(data=update_score(), team_name=settings.team_name)['team']
    logger.info(f"Team is: {current_team}")
    logger.info(f"Current score is: {current_score}")
    while True:
        live_score = int(get_team_score(data=update_score(), team_name=settings.team_name)['score'])
        if abs(live_score - current_score) > 1:
            logger.info(f"Score has been updated to {live_score}")
            player = vlc.MediaPlayer(f'file://{settings.victory_sound_path}')
            player.play()
            current_score = live_score

            time.sleep(20) # Frequency to check the score

if __name__ == "__main__":
    main()
