from typing import List, Dict, Optional

from pydantic import BaseModel

from waypoint.models.stat import Stat
from waypoint.enum import GameVariant, Game


class GameRound(BaseModel):
    id: str
    Participants: List[str]
    PlayerStats: Dict[str, Stat]
    Winner: Optional[str]
    Map: Optional[str]
    Game: Optional[Game]
    Variant: Optional[GameVariant]
