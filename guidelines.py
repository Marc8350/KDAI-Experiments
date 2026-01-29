from typing import List

from src.tasks.utils_typing import Entity, dataclass

"""
Entity definitions
"""


@dataclass
class PrivateSpaceCompany(Entity):
    """Refers to private companies primarily focused on space exploration, transportation, 
    satellite launch, or space-based services. These are non-governmental entities that have 
    a commercial interest in space activities."""

    span: str  # Such as: "Blue origin", "Boeing", "Northrop Grumman", "Arianespace"


@dataclass
class PublicSpaceCompany(Entity):
    """Refers to governmental entities or agencies that are primarily focused on space 
    exploration, research, transportation, satellite launch, or other space-based services. 
    These entities are state-owned and operated and are generally funded through public funds."""

    span: str  # Such as "ESA", "ISRO", "CNSA"


@dataclass
class Planet(Entity):
    """Refers to celestial bodies that orbit a star. Planets are large enough 
    to have cleared their orbits of other debris and have a nearly round shape 
    due to their self-gravity."""

    span: str  # Such as: "Earth", "Jupiter", "Venus", "Mercury", "Saturn"


@dataclass
class Launcher(Entity):
    """Refers to a vehicle designed primarily to transport payloads from the Earth's 
    surface to space. Launchers can carry various payloads, including satellites, 
    crewed spacecraft, and cargo, into various orbits or even beyond Earth's orbit. 
    They are usually multi-stage vehicles that use rocket engines for propulsion."""

    span: str  # Such as: "Sturn V", "Atlas V", "Soyuz", "Ariane 5"



ENTITY_DEFINITIONS: List[Entity] = [
    PrivateSpaceCompany,
    PublicSpaceCompany,
    Planet,
    Launcher,
]
    
if __name__ == "__main__":
    cell_txt = In[-1]