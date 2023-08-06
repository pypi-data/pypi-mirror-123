from enum import Enum, unique


@unique
class Game(str, Enum):
    ALL = "All"
    HALO_CE = "HaloCombatEvolved"
    HALO_2 = "Halo2"
    HALO_2_ANNIVERSARY = "Halo2Anniversary"
    HALO_3 = "Halo3"
    HALO_4 = "Halo4"
    HALO_REACH = "HaloReach"
