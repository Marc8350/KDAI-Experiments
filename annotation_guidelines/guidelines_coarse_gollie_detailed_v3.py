from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class Art(Entity):
    """Denotes titles of artistic productions and media, such as cinematic films, theatrical plays, periodicals, television broadcasts, and operatic works."""
    span: str  # Such as: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "The Gale Storm Show: Oh, Susanna"

@dataclass
class Building(Entity):
    """Represents artificial constructions and various facilities, including athletic stadiums, museum buildings, and international airports."""
    span: str  # Such as: "Henry Ford Museum", "Sheremetyevo International Airport", "Boston Garden"

@dataclass
class Event(Entity):
    """Includes specific organized happenings, historical incidents, social uprisings, revolutions, or particular performance stages."""
    span: str  # Such as: "Iranian Constitutional Revolution", "Eastwood Scoring Stage", "Bicentennial Boycott movement"

@dataclass
class Location(Entity):
    """Covers geographic sites and geopolitical zones, such as nations, urban centers, territories, and aquatic bodies."""
    span: str  # Such as: "Michigan", "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall"

@dataclass
class Organization(Entity):
    """Pertains to organized associations of individuals, encompassing businesses, global agencies, athletic clubs, and professional leagues."""
    span: str  # Such as: "IAEA", "Church's Chicken", "Texas Chicken", "Arsenal", "Tottenham"

@dataclass
class Other(Entity):
    """Used for entities excluded from conventional classifications, such as chemical elements, spoken languages, and biological components like proteins or domains."""
    span: str  # Such as: "Amphiphysin", "N-terminal", "BAR", "English", "uranium"

@dataclass
class Person(Entity):
    """Identifies human individuals, which may include literary writers, historical personalities, film directors, and imaginary figures."""
    span: str  # Such as: "George Axelrod", "Richard Quine", "Gaetano Donizetti", "Ellaline Terriss", "Edmund Payne"

@dataclass
class Product(Entity):
    """Concerns items produced via manufacturing, specifically focusing on car models, prototype vehicles, and particular mechanical devices."""
    span: str  # Such as: "Rolls-Royce Phantom", "Rolls-Royce 100EX", "Corvettes-GT1 C6R", "Fairbottom Bobs"

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