import datetime as dt
from typing import List

from pydantic import BaseModel


class Stat(BaseModel):
    GameId: int
    Score: int
    Kills: int
    Deaths: int
    Assists: int
    Headshots: int
    DateTime: dt.datetime
    MapId: int
    Won: bool
    Medals: int
    GameType: int
    KD: float
    LocalizedMapName: str = None


class StatHistory(BaseModel):
    Gamertag: str
    TotalMultiplayerGamesCompleted: int
    Stats: List[Stat]
