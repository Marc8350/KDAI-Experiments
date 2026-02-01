from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Identifies content broadcast over radio or television, such as talk segments, episodic series, and game shows."""
    span: str  # e.g., "The Tonight Show", "The Simpsons", "MasterChef", "CSI: Miami", "Saturday Night Live"

@dataclass
class ArtFilm(Entity):
    """Covers cinematic productions and motion pictures across all genres."""
    span: str  # e.g., "Pulp Fiction", "Inception", "Parasite", "The Godfather"

@dataclass
class ArtMusic(Entity):
    """Includes musical compositions like albums, individual tracks, bands, or orchestral arrangements."""
    span: str  # e.g., "Bohemian Rhapsody", "The Beatles", "Dark Side of the Moon", "London Philharmonic Orchestra"

@dataclass
class ArtOther(Entity):
    """Captures diverse creative outputs not fitting standard categories, including sculptures or music videos."""
    span: str  # e.g., "David by Michelangelo", "Thriller music video", "The Gates installation"

@dataclass
class ArtPainting(Entity):
    """Refers to visual art such as murals, canvas paintings, or specific artistic photography collections."""
    span: str  # e.g., "The Starry Night", "Guernica", "The Scream", "Mona Lisa"

@dataclass
class ArtWrittenart(Entity):
    """Denotes literary works including novels, periodicals, theatrical plays, and operas."""
    span: str  # e.g., "The Great Gatsby", "The New Yorker", "Hamlet", "War and Peace"

@dataclass
class BuildingAirport(Entity):
    """Pertains to aviation hubs and flight terminals."""
    span: str  # e.g., "John F. Kennedy International Airport", "Haneda Airport", "Charles de Gaulle Airport"

@dataclass
class BuildingHospital(Entity):
    """Refers to medical institutions, specialized clinics, and healthcare centers."""
    span: str  # e.g., "Mayo Clinic", "St. Jude Children's Research Hospital", "Massachusetts General Hospital"

@dataclass
class BuildingHotel(Entity):
    """Includes various lodging facilities and resort establishments."""
    span: str  # e.g., "The Ritz-Carlton", "Burj Al Arab", "Marriott Marquis"

@dataclass
class BuildingLibrary(Entity):
    """Designates repositories of books, research archives, and public libraries."""
    span: str  # e.g., "Library of Congress", "New York Public Library", "Bodleian Library"

@dataclass
class BuildingOther(Entity):
    """Identifies miscellaneous physical constructions like shrines, museums, or recording spaces."""
    span: str  # e.g., "The Louvre", "Guggenheim Museum", "Abbey Road Studios", "St. Peter's Basilica"

@dataclass
class BuildingRestaurant(Entity):
    """Covers eateries, bistros, cafes, and snack bars."""
    span: str  # e.g., "The French Laundry", "McDonald's", "Noma", "Starbucks"

@dataclass
class BuildingSportsfacility(Entity):
    """Refers to athletic arenas, stadiums, and multipurpose sports complexes."""
    span: str  # e.g., "Wembley Stadium", "Madison Square Garden", "Camp Nou"

@dataclass
class BuildingTheater(Entity):
    """Identifies venues for performance arts, including opera houses and playhouses."""
    span: str  # e.g., "La Scala", "Sydney Opera House", "Royal Shakespeare Theatre"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Relates to armed hostilities, historic battles, and large-scale military campaigns."""
    span: str  # e.g., "World War II", "Battle of Gettysburg", "Operation Desert Storm", "The Napoleonic Wars"

@dataclass
class EventDisaster(Entity):
    """Covers catastrophic occurrences, whether natural or resulting from human error."""
    span: str  # e.g., "The Great Fire of London", "Hurricane Katrina", "Chernobyl Disaster"

@dataclass
class EventElection(Entity):
    """Pertains to the process of political voting, including referendums and parliamentary polls."""
    span: str  # e.g., "2020 Presidential Election", "Brexit Referendum", "German Federal Election"

@dataclass
class EventOther(Entity):
    """Identifies various social movements or organized series of events not otherwise classified."""
    span: str  # e.g., "The Renaissance", "Civil Rights Movement", "The Industrial Revolution"

@dataclass
class EventProtest(Entity):
    """Refers to organized public demonstrations, uprisings, and socio-political revolutions."""
    span: str  # e.g., "The Arab Spring", "French Revolution", "The Salt March"

@dataclass
class EventSportsevent(Entity):
    """Covers competitive tournaments, championships, and athletic matches."""
    span: str  # e.g., "The Super Bowl", "Wimbledon", "The Olympic Games", "Tour de France"

@dataclass
class LocationGpe(Entity):
    """Designates political regions such as sovereign nations, municipalities, and administrative states."""
    span: str  # e.g., "Japan", "New York City", "Bavaria", "The European Union", "South Africa"

@dataclass
class LocationBodiesofwater(Entity):
    """Identifies aquatic features like oceans, reservoirs, rivers, and coastal areas."""
    span: str  # e.g., "Pacific Ocean", "Lake Superior", "The Nile River", "Hoover Dam"

@dataclass
class LocationIsland(Entity):
    """Refers to landmasses surrounded by water or island groups."""
    span: str  # e.g., "Madagascar", "Hawaii", "The Philippines", "Tasmania"

@dataclass
class LocationMountain(Entity):
    """Covers topographic peaks, mountain chains, and glacial formations."""
    span: str  # e.g., "Mount Everest", "The Andes", "Kilimanjaro", "Matterhorn"

@dataclass
class LocationOther(Entity):
    """Designates geographic markers or transit routes like bridges and specific coordinate lines."""
    span: str  # e.g., "Golden Gate Bridge", "The Equator", "Panama Canal", "38th Parallel"

@dataclass
class LocationPark(Entity):
    """Identifies protected nature reserves, city parks, and heritage sites."""
    span: str  # e.g., "Yellowstone National Park", "Central Park", "Serengeti National Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Pertains to transport infrastructure including thoroughfares, subway lines, and rail systems."""
    span: str  # e.g., "Route 66", "The Orient Express", "Trans-Siberian Railway", "M1 Motorway"

@dataclass
class OrganizationCompany(Entity):
    """Refers to corporate entities, commercial firms, and business franchises."""
    span: str  # e.g., "Apple Inc.", "Toyota Motor Corporation", "Amazon", "Coca-Cola"

@dataclass
class OrganizationEducation(Entity):
    """Identifies learning institutions like universities, research colleges, and primary schools."""
    span: str  # e.g., "Harvard University", "Oxford University", "Stanford", "Eton College"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Denotes state institutions, legislative bodies, and judicial courts."""
    span: str  # e.g., "The Pentagon", "U.S. Congress", "The Kremlin", "United Nations Security Council"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Includes journalism outlets, broadcasting networks, and magazine publishers."""
    span: str  # e.g., "The New York Times", "BBC News", "Reuters", "National Geographic"

@dataclass
class OrganizationOther(Entity):
    """Covers miscellaneous collective bodies like military divisions, NGOs, or international unions."""
    span: str  # e.g., "The Red Cross", "NATO", "Amnesty International", "82nd Airborne Division"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Refers to political factions and organized interest groups."""
    span: str  # e.g., "Democratic Party", "Labour Party", "African National Congress"

@dataclass
class OrganizationReligion(Entity):
    """Identifies faith-based groups, denominations, and ecclesiastical organizations."""
    span: str  # e.g., "Anglican Church", "Sunni Islam", "The Vatican", "Sikhism"

@dataclass
class OrganizationShoworganization(Entity):
    """Denotes performance groups like musical bands, ensembles, and dance companies."""
    span: str  # e.g., "Pink Floyd", "Vienna Philharmonic", "The Rolling Stones", "Bolshoi Ballet"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to governing bodies for sports and professional leagues."""
    span: str  # e.g., "NBA", "Premier League", "FIFA", "Major League Baseball"

@dataclass
class OrganizationSportsteam(Entity):
    """Designates specific athletic clubs and national squads."""
    span: str  # e.g., "Real Madrid", "New Zealand All Blacks", "Chicago Bulls", "Ferrari F1 Team"

@dataclass
class OtherAstronomything(Entity):
    """Covers celestial entities such as planets, stars, and astrological signs."""
    span: str  # e.g., "Mars", "Alpha Centauri", "Andromeda Galaxy", "The Big Dipper"

@dataclass
class OtherAward(Entity):
    """Refers to formal honors, prizes, and decorative titles."""
    span: str  # e.g., "Nobel Peace Prize", "Academy Award", "Pulitzer Prize", "Victoria Cross"

@dataclass
class OtherBiologything(Entity):
    """Identifies biological components like DNA sequences, specific proteins, or insect orders."""
    span: str  # e.g., "Hemoglobin", "CRISPR", "Coleoptera", "Mitochondria"

@dataclass
class OtherChemicalthing(Entity):
    """Denotes chemical substances, molecular compounds, and periodic elements."""
    span: str  # e.g., "Methane", "Sodium Chloride", "Helium", "Glucose"

@dataclass
class OtherCurrency(Entity):
    """Refers to monetary units and financial denominations."""
    span: str  # e.g., "US Dollar", "Euro", "Japanese Yen", "Bitcoin"

@dataclass
class OtherDisease(Entity):
    """Covers medical ailments, viral infections, and chronic health conditions."""
    span: str  # e.g., "Type 2 Diabetes", "Influenza", "Malaria", "Alzheimer's Disease"

@dataclass
class OtherEducationaldegree(Entity):
    """Identifies academic certifications and diplomas."""
    span: str  # e.g., "Master of Business Administration", "Doctor of Philosophy", "Juris Doctor"

@dataclass
class OtherGod(Entity):
    """Refers to deities, mythological figures, and creators in various faiths."""
    span: str  # e.g., "Zeus", "Vishnu", "Odin", "Athena"

@dataclass
class OtherLanguage(Entity):
    """Designates specific human tongues and regional dialects."""
    span: str  # e.g., "Mandarin Chinese", "Spanish", "Swahili", "Old English"

@dataclass
class OtherLaw(Entity):
    """Includes legal statutes, formal treaties, and constitutional acts."""
    span: str  # e.g., "Magna Carta", "Treaty of Versailles", "Civil Rights Act of 1964"

@dataclass
class OtherLivingthing(Entity):
    """Covers non-human biological life such as animal species and plants."""
    span: str  # e.g., "African Elephant", "Giant Sequoia", "Honeybee", "Great White Shark"

@dataclass
class OtherMedical(Entity):
    """Pertains to clinical specialties, pharmacological drugs, and healthcare procedures."""
    span: str  # e.g., "Cardiology", "Penicillin", "Chemotherapy", "Dermatology"

@dataclass
class PersonActor(Entity):
    """Identifies individuals known for acting in stage, screen, or voice productions."""
    span: str  # e.g., "Meryl Streep", "Tom Hanks", "Viola Davis", "Robert De Niro"

@dataclass
class PersonArtistAuthor(Entity):
    """Refers to creative individuals such as painters, novelists, and poets."""
    span: str  # e.g., "Pablo Picasso", "J.K. Rowling", "Maya Angelou", "Vincent van Gogh"

@dataclass
class PersonAthlete(Entity):
    """Covers professional competitors in any sporting discipline."""
    span: str  # e.g., "Serena Williams", "Lionel Messi", "Michael Jordan", "Usain Bolt"

@dataclass
class PersonDirector(Entity):
    """Designates those who manage the creative vision of films or theater."""
    span: str  # e.g., "Steven Spielberg", "Greta Gerwig", "Akira Kurosawa", "Alfred Hitchcock"

@dataclass
class PersonOther(Entity):
    """Identifies people who fall outside specific professions, such as socialites or historical figures."""
    span: str  # e.g., "Elon Musk", "Princess Diana", "Anne Frank", "Rosa Parks"

@dataclass
class PersonPolitician(Entity):
    """Refers to elected officials, heads of state, and political representatives."""
    span: str  # e.g., "Winston Churchill", "Angela Merkel", "Nelson Mandela", "Barack Obama"

@dataclass
class PersonScholar(Entity):
    """Covers academics, scientists, and dedicated researchers."""
    span: str  # e.g., "Albert Einstein", "Marie Curie", "Stephen Hawking", "Noam Chomsky"

@dataclass
class PersonSoldier(Entity):
    """Identifies military personnel, generals, and combatants."""
    span: str  # e.g., "George Patton", "Douglas MacArthur", "Joan of Arc"

@dataclass
class ProductAirplane(Entity):
    """Refers to specific models of fixed-wing aircraft or rotorcraft."""
    span: str  # e.g., "Boeing 747", "Airbus A380", "Concorde", "Spitfire"

@dataclass
class ProductCar(Entity):
    """Covers automotive models and vehicle series."""
    span: str  # e.g., "Tesla Model S", "Ford Mustang", "Volkswagen Beetle", "Porsche 911"

@dataclass
class ProductFood(Entity):
    """Identifies edible items, culinary ingredients, or specific plant varieties used for food."""
    span: str  # e.g., "Quinoa", "Parmesan Cheese", "Saffron", "Granny Smith Apple"

@dataclass
class ProductGame(Entity):
    """Designates interactive entertainment, including video games and board games."""
    span: str  # e.g., "The Legend of Zelda", "Minecraft", "Chess", "Grand Theft Auto V"

@dataclass
class ProductOther(Entity):
    """Captures various manufactured goods, hardware components, or specialized equipment."""
    span: str  # e.g., "iPhone 13", "Hubble Space Telescope", "PlayStation 5"

@dataclass
class ProductShip(Entity):
    """Refers to watercraft, naval vessels, and submarines."""
    span: str  # e.g., "RMS Titanic", "USS Enterprise", "HMS Victory", "Santa Maria"

@dataclass
class ProductSoftware(Entity):
    """Identifies computer applications, operating systems, and digital tools."""
    span: str  # e.g., "Microsoft Windows", "Linux", "Adobe Photoshop", "Google Chrome"

@dataclass
class ProductTrain(Entity):
    """Covers locomotive models and high-speed rail vehicles."""
    span: str  # e.g., "Shinkansen", "TGV", "Flying Scotsman", "Eurostar"

@dataclass
class ProductWeapon(Entity):
    """Designates military armament, firearms, and defense systems."""
    span: str  # e.g., "AK-47", "M1 Abrams Tank", "Tomahawk Missile", "Excalibur"

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