from typing import List, Dict, Optional

from pydantic import BaseModel

from waypoint.models.stat import Stat


class GameRound(BaseModel):
    id: str
    Participants: List[str]
    PlayerStats: Dict[str, Stat]
    Winner: Optional[str] = None
    Map: Optional[str] = None
    Game: Optional[str] = None
