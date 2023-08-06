from typing import List
import hashlib
from collections import defaultdict

from pydantic import ValidationError

from waypoint import WaypointClient
from waypoint.models import StatHistory, GameRound, Stat
from waypoint.data import map_ids
from waypoint.enum import Game, GameVariant


class RoundMapper:
    def __init__(self, client: WaypointClient):
        self.client = client

    @staticmethod
    def _calculate_uid(stat: Stat) -> str:
        ts = stat.DateTime.replace(second=0, microsecond=0).timestamp()
        return hashlib.md5(f"{ts}{stat.MapId}".encode("utf-8")).hexdigest()

    def map_rounds(
        self,
        gamertags: List[str],
        variant: GameVariant = GameVariant.SLAYER,
        game: Game = Game.ALL,
    ) -> List[GameRound]:
        round_map = defaultdict(dict)
        win_map = {}
        map_map = {}
        for page_num in range(1, 11):
            try:
                history: List[StatHistory] = self.client.get_game_history(
                    gamertags,
                    variant,
                    game,
                    page_num,
                )
            except ValidationError:
                continue
            for player_history in history:
                for stat in player_history.Stats:
                    uid = self._calculate_uid(stat)
                    round_map[uid][player_history.Gamertag] = stat
                    map_map[uid] = stat.MapId
                    if stat.Won:
                        win_map[uid] = player_history.Gamertag
        results = []
        for uid, game_round in round_map.items():
            if sorted(list(game_round.keys())) != sorted(gamertags):
                continue
            map_info = map_ids.get(map_map[uid], {})
            results.append(
                GameRound(
                    id=uid,
                    Participants=list(game_round.keys()),
                    Winner=win_map.get(uid),
                    PlayerStats=game_round,
                    Map=map_info.get("map"),
                    Game=map_info.get("game", game),
                    Variant=variant,
                )
            )
        return results
