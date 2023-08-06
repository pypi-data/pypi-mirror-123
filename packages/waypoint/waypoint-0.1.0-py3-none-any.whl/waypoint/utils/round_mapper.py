from typing import List
import hashlib
from collections import defaultdict

from waypoint import WaypointClient
from waypoint.models import StatHistory, GameRound, Stat
from waypoint.data import map_ids


class RoundMapper:
    def __init__(self, client: WaypointClient):
        self.client = client

    @staticmethod
    def _calculate_uid(stat: Stat) -> str:
        ts = stat.DateTime.replace(second=0, microsecond=0).timestamp()
        return hashlib.md5(f"{ts}{stat.MapId}".encode("utf-8")).hexdigest()

    def map_rounds(self, gamertags: List[str]) -> List[GameRound]:
        round_map = defaultdict(dict)
        win_map = {}
        map_map = {}
        for page_num in range(1, 11):
            history: List[StatHistory] = self.client.get_game_history(
                gamertags, page=page_num
            )
            for player_history in history:
                for game in player_history.Stats:
                    uid = self._calculate_uid(game)
                    round_map[uid][player_history.Gamertag] = game
                    map_map[uid] = game.MapId
                    if game.Won:
                        win_map[uid] = player_history.Gamertag
        results = []
        for uid, game_round in round_map.items():
            if sorted(list(game_round.keys())) != sorted(gamertags):
                continue
            map_info = map_ids.get(map_map[uid], {})
            results.append(
                GameRound(
                    Participants=list(game_round.keys()),
                    Winner=win_map.get(uid, "N/A"),
                    PlayerStats=game_round,
                    Map=map_info.get("map", "N/A"),
                    Game=map_info.get("game", "N/A"),
                )
            )
        return results
