from typing import List, Union
import datetime as dt

from requests.packages.urllib3.util.retry import Retry

from waypoint.models import StatHistory
from waypoint.enum import GameVariant, Game
from waypoint.client.base import APIClient, http_method


class WaypointClient(APIClient):
    retry_strategy = Retry(
        total=10,
        backoff_factor=1,
        status_forcelist=[500],
    )

    def __init__(self, auth_cookie: str):
        super().__init__(
            "https://www.halowaypoint.com/en-us/games/halo-the-master-chief-collection/xbox-one/"
        )
        self.session.cookies.set("Auth", auth_cookie)

    @http_method(StatHistory)
    def get_game_history(
        self,
        gamertags: Union[str, List[str]],
        game_variant: GameVariant = GameVariant.SLAYER,
        game: Game = Game.ALL,
        page: int = 1,
    ):
        if isinstance(gamertags, list):
            gamertags = ",".join(gamertags)
        return self.session.get(
            "game-history",
            params={
                "gameVariant": game_variant.value,
                "gamertags": gamertags,
                "page": page,
                "game": game.value,
                "view": "DataOnly",
                "_": round(dt.datetime.now().timestamp() * 1000),
            },
        )
