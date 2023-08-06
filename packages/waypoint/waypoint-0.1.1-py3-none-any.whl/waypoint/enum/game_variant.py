from enum import Enum, unique


@unique
class GameVariant(str, Enum):
    CTF = "Ctf"
    SLAYER = "Slayer"
    ODDBALL = "Oddball"
    KING_OF_THE_HILL = "Koth"
    JUGGERNAUT = "Juggernaut"
    INFECTION = "Infection"
    FLOOD = "Flood"
    RACE = "Race"
    EXTRACTION = "Extraction"
    DOMINION = "Dominion"
    REGICIDE = "Regicide"
    GRIFBALL = "Grifball"
    RICOCHET = "Ricochet"
    FORGE = "Sandbox"
    VIP = "Vip"
    TERRITORIES = "Territories"
    ASSAULT = "Assault"
