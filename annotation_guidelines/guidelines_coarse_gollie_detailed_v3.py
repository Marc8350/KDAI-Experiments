from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Denotes artistic creations like movies, literature, periodicals, musical recordings, theatrical productions, and TV series."""
    span: str  # Such as: "The Shawshank Redemption", "Time", "Bosch", "The Seven Year Itch", "L'Atlantide", "Imelda de' Lambertazzi"

@dataclass
class Building(Entity):
    """Includes constructed facilities and physical edifices, for instance, medical centers, arenas, air terminals, galleries, and sound studios."""
    span: str  # Such as: "Boston Garden", "Henry Ford Museum", "Alpha Recording Studios", "Sheremetyevo International Airport", "Memorial Sloan-Kettering Cancer Center"

@dataclass
class Event(Entity):
    """Categorizes planned happenings and historical milestones, encompassing athletic championships, sociopolitical shifts, uprisings, voting processes, and structured gatherings."""
    span: str  # Such as: "World Cup", "French Revolution", "Union for a Popular Movement", "Stanley Cup", "March 1898 elections", "Eastwood Scoring Stage"

@dataclass
class Location(Entity):
    """Relates to terrestrial sites and geographic areas, such as nations, municipalities, provinces, specific hydrographic basins, or transport routes."""
    span: str  # Such as: "Mediterranean Basin", "Croatia", "London", "Cornwall", "Victoria line", "Michigan", "Northern Europe"

@dataclass
class Organization(Entity):
    """Identifies collective bodies and structured associations, including corporate entities, athletic clubs, state departments, armed forces, and global organizations."""
    span: str  # Such as: "Warner Brothers", "IAEA", "French National Assembly", "Church's Chicken", "Arsenal", "Supreme Court", "4th Army"

@dataclass
class Other(Entity):
    """Covers distinct entities falling outside standard classifications, such as biochemical compounds, chemical elements, statutory laws, awards, linguistics, and metaphysical ideas like astrological signs."""
    span: str  # Such as: "p53 protein", "uranium", "Order of the Republic of Guinea", "Amphiphysin", "United States Freedom Support Act", "English", "Zodiac"

@dataclass
class Person(Entity):
    """Specifies individual humans, whether actual or imaginary, encompassing their monikers and formal designations."""
    span: str  # Such as: "Bette Davis", "George Axelrod", "Binion", "Richard Quine", "Gaetano Donizetti", "Mrs. Strong", "Jacqueline Bouvier Kennedy"

@dataclass
class Product(Entity):
    """Represents commercial items and manufactured goods, such as specialized transportation models, armaments, industrial equipment, software, and computing hardware."""
    span: str  # Such as: "Wikipedia", "Rolls-Royce Phantom", "PDP-1", "Corvettes", "Fairbottom Bobs", "ZU-23-2M Wróbel", "AR-15"

ENTITY_DEFINITIONS: List[Entity] = [
    Art,
    Building,
    Event,
    Location,
    Organization,
    Other,
    Person,
    Product,
]