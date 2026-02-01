from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Identifies content produced for radio or television, such as serials, talk programs, and sitcoms."""
    span: str  # For example: "The Tonight Show", "Seinfeld", "MasterChef", "CSI: Miami"

@dataclass
class ArtFilm(Entity):
    """Identifies cinematic productions and motion pictures regardless of genre."""
    span: str  # For example: "Pulp Fiction", "Inception", "Parasite", "The Godfather"

@dataclass
class ArtMusic(Entity):
    """Identifies musical creations, including individual tracks, albums, bands, or orchestral works."""
    span: str  # For example: "The Beatles", "Bohemian Rhapsody", "London Philharmonic Orchestra", "Thriller"

@dataclass
class ArtOther(Entity):
    """Identifies miscellaneous creative outputs not fitting specific art categories, like music videos or sculptures."""
    span: str  # For example: "The Thinker", "Sledgehammer (video)", "David", "Cloud Gate"

@dataclass
class ArtPainting(Entity):
    """Identifies visual artworks like murals and canvases, or specific series of camera lenses considered artistic."""
    span: str  # For example: "Starry Night", "Guernica", "The Scream", "Voigtländer Nokton"

@dataclass
class ArtWrittenart(Entity):
    """Identifies literary works such as periodicals, novels, theatrical scripts, or operas."""
    span: str  # For example: "The Great Gatsby", "The New Yorker", "Hamlet", "Les Misérables"

@dataclass
class BuildingAirport(Entity):
    """Identifies aviation hubs and flight terminals."""
    span: str  # For example: "Heathrow Airport", "Haneda Airport", "LAX", "Dubai International"

@dataclass
class BuildingHospital(Entity):
    """Identifies healthcare facilities, clinics, and medical centers."""
    span: str  # For example: "Mayo Clinic", "Johns Hopkins Hospital", "St. Jude Children's Research Hospital"

@dataclass
class BuildingHotel(Entity):
    """Identifies hospitality venues and commercial lodging buildings."""
    span: str  # For example: "The Ritz-Carlton", "Hilton Tokyo", "Burj Al Arab", "The Plaza Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Identifies book repositories and archival institutions."""
    span: str  # For example: "Library of Congress", "Bodleian Library", "Vatican Library", "New York Public Library"

@dataclass
class BuildingOther(Entity):
    """Identifies various physical edifices like galleries, shrines, or recording studios not listed elsewhere."""
    span: str  # For example: "Louvre Museum", "Abbey Road Studios", "Parthenon", "Notre-Dame Cathedral"

@dataclass
class BuildingRestaurant(Entity):
    """Identifies places for dining, including cafes, bistros, and delicatessens."""
    span: str  # For example: "Noma", "Denny's", "Starbucks", "Olive Garden"

@dataclass
class BuildingSportsfacility(Entity):
    """Identifies arenas, athletic stadiums, and specialized sports centers."""
    span: str  # For example: "Wembley Stadium", "Madison Square Garden", "Allianz Arena", "Fenway Park"

@dataclass
class BuildingTheater(Entity):
    """Identifies performing arts centers, opera houses, and playhouses."""
    span: str  # For example: "Globe Theatre", "Metropolitan Opera House", "Bolshoi Theatre", "Sydney Opera House"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Identifies historical wars, armed engagements, and combat operations."""
    span: str  # For example: "World War II", "Battle of Waterloo", "Operation Desert Storm", "The Crusades"

@dataclass
class EventDisaster(Entity):
    """Identifies catastrophic incidents, whether natural or man-made, such as floods or industrial accidents."""
    span: str  # For example: "Chernobyl disaster", "Great Famine of Ireland", "Hurricane Katrina", "The Great Fire of London"

@dataclass
class EventElection(Entity):
    """Identifies political voting processes, including referendums and parliamentary polls."""
    span: str  # For example: "2020 US Presidential Election", "Brexit Referendum", "General Election 1997"

@dataclass
class EventOther(Entity):
    """Identifies miscellaneous happenings, social movements, or event series not otherwise categorized."""
    span: str  # For example: "Civil Rights Movement", "Renaissance", "The Enlightenment", "Industrial Revolution"

@dataclass
class EventProtest(Entity):
    """Identifies organized boycotts, civil uprisings, and public demonstrations."""
    span: str  # For example: "French Revolution", "Salt March", "Black Lives Matter protests", "Arab Spring"

@dataclass
class EventSportsevent(Entity):
    """Identifies athletic championships, competitive tournaments, and game series."""
    span: str  # For example: "The Olympics", "Super Bowl", "Wimbledon", "Tour de France"

@dataclass
class LocationGpe(Entity):
    """Identifies geopolitical territories such as nations, municipalities, and regional states."""
    span: str  # For example: "France", "Tokyo", "California", "South East Asia", "Brazil"

@dataclass
class LocationBodiesofwater(Entity):
    """Identifies hydrographic features like reservoirs, shorelines, and rivers."""
    span: str  # For example: "Hoover Dam", "English Channel", "Lake Victoria", "Amazon River"

@dataclass
class LocationIsland(Entity):
    """Identifies landmasses surrounded by water or island-based administrative districts."""
    span: str  # For example: "Tasmania", "Hawaiian Islands", "Bali", "Crete", "Madagascar"

@dataclass
class LocationMountain(Entity):
    """Identifies geological heights like peaks, mountain chains, and glaciers."""
    span: str  # For example: "Mount Everest", "The Andes", "Hubbard Glacier", "Pyrenees"

@dataclass
class LocationOther(Entity):
    """Identifies generic zones, transit routes, or bridges not covered by specific labels."""
    span: str  # For example: "Golden Gate Bridge", "Silk Road", "Circle Line", "Grand Canyon"

@dataclass
class LocationPark(Entity):
    """Identifies public greenspaces, wildlife reserves, and historic community districts."""
    span: str  # For example: "Central Park", "Yellowstone National Park", "Hyde Park", "Serengeti"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Identifies transportation infrastructure including avenues, rail tracks, and subway networks."""
    span: str  # For example: "Route 66", "Trans-Siberian Railway", "M25 Motorway", "Tokyo Subway"

@dataclass
class OrganizationCompany(Entity):
    """Identifies commercial firms, corporate entities, and business franchises."""
    span: str  # For example: "Apple Inc.", "Toyota", "McDonald's", "Sony", "Microsoft"

@dataclass
class OrganizationEducation(Entity):
    """Identifies academic institutions like schools, polytechnics, and universities."""
    span: str  # For example: "Oxford University", "Harvard", "Eton College", "Stanford"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Identifies state regulatory bodies, judiciaries, and legislative assemblies."""
    span: str  # For example: "United Nations", "FBI", "The Kremlin", "Parliament of Canada", "The White House"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Identifies news outlets, publishing houses, and television networks."""
    span: str  # For example: "The Guardian", "BBC", "The New York Times", "CNN", "Reuters"

@dataclass
class OrganizationOther(Entity):
    """Identifies groups such as military divisions, international consortia, or alliances not elsewhere specified."""
    span: str  # For example: "NATO", "Red Cross", "The 101st Airborne Division", "World Wildlife Fund"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Identifies associations formed for political purposes."""
    span: str  # For example: "Labour Party", "Republican Party", "African National Congress", "The Green Party"

@dataclass
class OrganizationReligion(Entity):
    """Identifies faith groups, ecclesiastical bodies, and religious education centers."""
    span: str  # For example: "Islam", "Buddhism", "Church of England", "The Vatican", "Hinduism"

@dataclass
class OrganizationShoworganization(Entity):
    """Identifies performing groups like musical ensembles, theater troupes, or philharmonic orchestras."""
    span: str  # For example: "Rolling Stones", "Berlin Philharmonic", "Cirque du Soleil", "U2"

@dataclass
class OrganizationSportsleague(Entity):
    """Identifies associations and federations managing sports competitions."""
    span: str  # For example: "NBA", "FIFA", "Major League Baseball", "Premier League"

@dataclass
class OrganizationSportsteam(Entity):
    """Identifies national squads and representational sports clubs."""
    span: str  # For example: "Real Madrid", "New Zealand All Blacks", "Los Angeles Lakers", "Scuderia Ferrari"

@dataclass
class OtherAstronomything(Entity):
    """Identifies space entities like planets, galaxies, and signs of the zodiac."""
    span: str  # For example: "Mars", "Andromeda Galaxy", "Scorpio", "Sirius", "Milky Way"

@dataclass
class OtherAward(Entity):
    """Identifies trophies, medals, and formal honors or titles."""
    span: str  # For example: "Nobel Peace Prize", "Academy Award", "Victoria Cross", "Pulitzer Prize"

@dataclass
class OtherBiologything(Entity):
    """Identifies biological components such as protein sequences, cells, and taxonomic classifications."""
    span: str  # For example: "DNA", "Insulin", "Mitochondria", "Coleoptera", "Hemoglobin"

@dataclass
class OtherChemicalthing(Entity):
    """Identifies molecular compounds and chemical elements."""
    span: str  # For example: "Oxygen", "Sodium Chloride", "Methane", "Iron", "Glucose"

@dataclass
class OtherCurrency(Entity):
    """Identifies financial symbols and monetary units."""
    span: str  # For example: "Euro", "Yen", "£", "Bitcoin", "Swiss Franc"

@dataclass
class OtherDisease(Entity):
    """Identifies medical conditions, pathological states, and epidemics."""
    span: str  # For example: "COVID-19", "Malaria", "Alzheimer's", "Tuberculosis", "Diabetes"

@dataclass
class OtherEducationaldegree(Entity):
    """Identifies academic credentials and professional certifications."""
    span: str  # For example: "Master of Arts", "MBA", "Juris Doctor", "B.S. in Biology"

@dataclass
class OtherGod(Entity):
    """Identifies mythological deities and divine figures across cultures."""
    span: str  # For example: "Zeus", "Vishnu", "Odin", "Athena", "Anubis"

@dataclass
class OtherLanguage(Entity):
    """Identifies human communication forms and specific regional dialects."""
    span: str  # For example: "Spanish", "Mandarin", "Swahili", "Klingon", "Cantonese"

@dataclass
class OtherLaw(Entity):
    """Identifies legal statutes, international treaties, and federal acts."""
    span: str  # For example: "Magna Carta", "Treaty of Versailles", "The Patriot Act", "Geneva Convention"

@dataclass
class OtherLivingthing(Entity):
    """Identifies flora, fauna, and various biological organisms."""
    span: str  # For example: "Oak tree", "Tiger", "Fungi", "Lavender", "Blue Whale"

@dataclass
class OtherMedical(Entity):
    """Identifies pharmacological treatments, clinical procedures, and medical specialties."""
    span: str  # For example: "Cardiology", "Chemotherapy", "Aspirin", "MRI scan", "Penicillin"

@dataclass
class PersonActor(Entity):
    """Identifies performers in film, stage, and television."""
    span: str  # For example: "Meryl Streep", "Tom Hanks", "Shah Rukh Khan", "Viola Davis"

@dataclass
class PersonArtistAuthor(Entity):
    """Identifies individuals who create fine art, compose music, or write literature."""
    span: str  # For example: "Ernest Hemingway", "J.K. Rowling", "Ludwig van Beethoven", "Pablo Picasso"

@dataclass
class PersonAthlete(Entity):
    """Identifies sports competitors, professional players, and olympians."""
    span: str  # For example: "Serena Williams", "Lionel Messi", "Michael Jordan", "Usain Bolt"

@dataclass
class PersonDirector(Entity):
    """Identifies individuals leading film or theatrical productions."""
    span: str  # For example: "Steven Spielberg", "Sofia Coppola", "Christopher Nolan", "Akira Kurosawa"

@dataclass
class PersonOther(Entity):
    """Identifies public figures, historical persons, or famous individuals not defined by a single category."""
    span: str  # For example: "Marie Antoinette", "The Wright Brothers", "Winston Churchill", "Princess Diana"

@dataclass
class PersonPolitician(Entity):
    """Identifies policy makers, elected officials, and heads of state."""
    span: str  # For example: "Angela Merkel", "Nelson Mandela", "Jacinda Ardern", "Abraham Lincoln"

@dataclass
class PersonScholar(Entity):
    """Identifies professors, researchers, and scientific experts."""
    span: str  # For example: "Albert Einstein", "Marie Curie", "Noam Chomsky", "Stephen Hawking"

@dataclass
class PersonSoldier(Entity):
    """Identifies military members, commanders, and combatants."""
    span: str  # For example: "General Patton", "Sun Tzu", "Joan of Arc", "Dwight D. Eisenhower"

@dataclass
class ProductAirplane(Entity):
    """Identifies specific models of fixed-wing planes and helicopters."""
    span: str  # For example: "Boeing 747", "Airbus A380", "Black Hawk helicopter", "Cessna 172"

@dataclass
class ProductCar(Entity):
    """Identifies automotive platforms and specific car models."""
    span: str  # For example: "Ford Mustang", "Tesla Model S", "Volkswagen Beetle", "Honda Civic"

@dataclass
class ProductFood(Entity):
    """Identifies edible items, culinary ingredients, and specific crop varieties."""
    span: str  # For example: "Tofu", "Saffron", "Honeycrisp apple", "Durian", "Quinoa"

@dataclass
class ProductGame(Entity):
    """Identifies electronic entertainment including PC and console titles."""
    span: str  # For example: "Minecraft", "The Legend of Zelda", "Grand Theft Auto V", "Pac-Man"

@dataclass
class ProductOther(Entity):
    """Identifies industrial components, technical hardware, or specific artifacts."""
    span: str  # For example: "Enigma machine", "Intel Core i7", "Rosetta Stone", "Raspberry Pi"

@dataclass
class ProductShip(Entity):
    """Identifies naval vessels, maritime craft, and ships."""
    span: str  # For example: "Titanic", "USS Enterprise", "Queen Mary 2", "Santa Maria"

@dataclass
class ProductSoftware(Entity):
    """Identifies digital platforms, operating systems, and computer applications."""
    span: str  # For example: "Windows 11", "Adobe Photoshop", "Linux", "Python", "Slack"

@dataclass
class ProductTrain(Entity):
    """Identifies specific rail vehicles and locomotive models."""
    span: str  # For example: "Shinkansen", "Orient Express", "Eurostar", "Flying Scotsman"

@dataclass
class ProductWeapon(Entity):
    """Identifies ballistic systems, armaments, and military explosives."""
    span: str  # For example: "AK-47", "Tomahawk missile", "M1 Abrams", "Excalibur"

ENTITY_DEFINITIONS: List[Entity] = [
    ArtBroadcastprogram,
    ArtFilm,
    ArtMusic,
    ArtOther,
    ArtPainting,
    ArtWrittenart,
    BuildingAirport,
    BuildingHospital,
    BuildingHotel,
    BuildingLibrary,
    BuildingOther,
    BuildingRestaurant,
    BuildingSportsfacility,
    BuildingTheater,
    EventAttackBattleWarMilitaryconflict,
    EventDisaster,
    EventElection,
    EventOther,
    EventProtest,
    EventSportsevent,
    LocationGpe,
    LocationBodiesofwater,
    LocationIsland,
    LocationMountain,
    LocationOther,
    LocationPark,
    LocationRoadRailwayHighwayTransit,
    OrganizationCompany,
    OrganizationEducation,
    OrganizationGovernmentGovernmentagency,
    OrganizationMediaNewspaper,
    OrganizationOther,
    OrganizationPoliticalparty,
    OrganizationReligion,
    OrganizationShoworganization,
    OrganizationSportsleague,
    OrganizationSportsteam,
    OtherAstronomything,
    OtherAward,
    OtherBiologything,
    OtherChemicalthing,
    OtherCurrency,
    OtherDisease,
    OtherEducationaldegree,
    OtherGod,
    OtherLanguage,
    OtherLaw,
    OtherLivingthing,
    OtherMedical,
    PersonActor,
    PersonArtistAuthor,
    PersonAthlete,
    PersonDirector,
    PersonOther,
    PersonPolitician,
    PersonScholar,
    PersonSoldier,
    ProductAirplane,
    ProductCar,
    ProductFood,
    ProductGame,
    ProductOther,
    ProductShip,
    ProductSoftware,
    ProductTrain,
    ProductWeapon,
]