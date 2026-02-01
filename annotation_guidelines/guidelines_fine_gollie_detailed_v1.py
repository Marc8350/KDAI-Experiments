from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Denotes radio or television productions, encompassing series, sitcoms, game shows, and talk shows."""
    span: str  # Examples: "The Gale Storm Show", "12 Corazones", "Street Cents", "Jonovision", "Trailer Park Boys"

@dataclass
class ArtFilm(Entity):
    """Includes motion pictures and cinematic works across all genres."""
    span: str  # Examples: "L'Atlantide", "The Shawshank Redemption", "Bosch"

@dataclass
class ArtMusic(Entity):
    """Identifies musical creations, such as albums, songs, orchestral scores, symphonies, or bands."""
    span: str  # Examples: "Hollywood Studio Symphony", "Atkinson, Danko and Ford", "Champion Lover", "Sex"

@dataclass
class ArtOther(Entity):
    """Covers diverse artistic expressions or programs not fitting specific types, like music videos or sculptures."""
    span: str  # Examples: "Venus de Milo", "The Today Show", "Bleed Like Me"

@dataclass
class ArtPainting(Entity):
    """Represents visual art like graffiti and paintings, or specialized photographic lens series."""
    span: str  # Examples: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Loxia", "Batis"

@dataclass
class ArtWrittenart(Entity):
    """Refers to literary works, including plays, magazines, novels, operas, and short stories."""
    span: str  # Examples: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Rita Hayworth and Shawshank Redemption"

@dataclass
class BuildingAirport(Entity):
    """Designates aviation hubs and airport terminals."""
    span: str  # Examples: "Sheremetyevo International Airport", "London Luton Airport", "Newark Liberty International Airport"

@dataclass
class BuildingHospital(Entity):
    """Identifies clinics, medical facilities, and hospital centers."""
    span: str  # Examples: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Hokkaido University Hospital"

@dataclass
class BuildingHotel(Entity):
    """Refers to lodging venues and hotel establishments."""
    span: str  # Examples: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Covers book collections, journal archives, and libraries."""
    span: str  # Examples: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library"

@dataclass
class BuildingOther(Entity):
    """Includes miscellaneous physical buildings and structures like places of worship, museums, or recording studios."""
    span: str  # Examples: "Henry Ford Museum", "Communiplex", "Alpha Recording Studios", "Saint Matthew Church"

@dataclass
class BuildingRestaurant(Entity):
    """Denotes places for dining, such as cafes, delis, and restaurants."""
    span: str  # Examples: "Trumbull", "Carnegie Deli", "Fatburger"

@dataclass
class BuildingSportsfacility(Entity):
    """Represents athletic complexes, stadiums, sports centers, and indoor arenas."""
    span: str  # Examples: "Boston Garden", "Sports Center", "Glenn Warner Soccer Facility"

@dataclass
class BuildingTheater(Entity):
    """Identifies venues for the performing arts, including opera houses and theaters."""
    span: str  # Examples: "Sanders Theatre", "Pittsburgh Civic Light Opera", "National Paris Opera"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Refers to military engagements, armed conflicts, battles, and wars."""
    span: str  # Examples: "Vietnam War", "Easter Offensive", "Operation Zipper", "Battle of Romani"

@dataclass
class EventDisaster(Entity):
    """Covers industrial accidents or natural catastrophes like famines and earthquakes."""
    span: str  # Examples: "1693 Sicily earthquake", "North Korean famine", "1912 North Mount Lyell Disaster"

@dataclass
class EventElection(Entity):
    """Denotes political voting events, including by-elections and parliamentary polls."""
    span: str  # Examples: "March 1898 elections", "Elections to the European Parliament", "Mitcham and Morden by-election"

@dataclass
class EventOther(Entity):
    """Identifies various organized series, social movements, or events not classified elsewhere."""
    span: str  # Examples: "Eastwood Scoring Stage", "Masaryk Democratic Movement", "Union for a Popular Movement"

@dataclass
class EventProtest(Entity):
    """Represents social uprisings, boycotts, revolutions, and public protests."""
    span: str  # Examples: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Iranian revolution"

@dataclass
class EventSportsevent(Entity):
    """Refers to athletic tournaments, specific match series, and championships."""
    span: str  # Examples: "Stanley Cup", "World Cup", "National Champions"

@dataclass
class LocationGpe(Entity):
    """Designates geopolitical territories such as cities, nations, states, and regional areas."""
    span: str  # Examples: "Croatian", "Republic of Croatia", "Mediterranean Basin", "Cornwall", "Los Angeles"

@dataclass
class LocationBodiesofwater(Entity):
    """Identifies shorelines, kills, dams, and lakes."""
    span: str  # Examples: "Atatürk Dam Lake", "Arthur Kill", "Norfolk coast"

@dataclass
class LocationIsland(Entity):
    """Refers to archipelagos, islands, or specific districts situated on islands."""
    span: str  # Examples: "Samsat", "Staten Island", "Laccadives", "Maldives"

@dataclass
class LocationMountain(Entity):
    """Covers glaciers, mountain ridges, and individual peaks."""
    span: str  # Examples: "Ruweisat Ridge", "Miteirya Ridge", "Salamander Glacier", "Mount Diablo"

@dataclass
class LocationOther(Entity):
    """Represents general transit lines, geographic areas, or bridges not covered by other categories."""
    span: str  # Examples: "Cartuther", "Victoria line", "Northern City Line", "West Gate Bridge"

@dataclass
class LocationPark(Entity):
    """Denotes historic community complexes, national parks, and public parks."""
    span: str  # Examples: "Gramercy Park", "Painted Desert Community Complex", "Shenandoah National Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Identifies transportation links such as subway lines, railways, and roads."""
    span: str  # Examples: "NJT", "Newark-Elizabeth Rail Link", "Friern Barnet Road", "North Jersey Coast Line"

@dataclass
class OrganizationCompany(Entity):
    """Refers to corporate entities, commercial franchises, and businesses."""
    span: str  # Examples: "Church's Chicken", "Two Pesos, Inc.", "Taco Cabana, Inc.", "WHL"

@dataclass
class OrganizationEducation(Entity):
    """Covers schools, academic academies, colleges, and universities."""
    span: str  # Examples: "Belfast Royal Academy", "Ulster College of Physical Education", "MIT", "Barnard College"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Identifies legislative bodies, government agencies, councils, and courts."""
    span: str  # Examples: "Supreme Court", "Congregazione dei Nobili", "Diet", "New York City Council"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Designates TV networks, magazines, news outlets, and newspapers."""
    span: str  # Examples: "Al Jazeera", "Clash", "TimeOut Melbourne", "Fuse"

@dataclass
class OrganizationOther(Entity):
    """Includes various groups like military divisions, consortia, or armies not otherwise specified."""
    span: str  # Examples: "IAEA", "4th Army", "SS Division Nordland"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Represents political groups and parties."""
    span: str  # Examples: "Shimpotō", "Al Wafa' Islamic party", "National Liberal Party"

@dataclass
class OrganizationReligion(Entity):
    """Refers to faith-based institutions, religious denominations, and churches."""
    span: str  # Examples: "Jewish", "Christian", "Catholic Church", "non-denominational Christian"

@dataclass
class OrganizationShoworganization(Entity):
    """Identifies entertainment groups such as orchestras, troupes, and musical bands."""
    span: str  # Examples: "Mr. Mister", "Lizzy", "Bochumer Symphoniker", "Yeah Yeah Yeahs"

@dataclass
class OrganizationSportsleague(Entity):
    """Covers athletic associations, sports leagues, and divisions."""
    span: str  # Examples: "First Division", "NHL", "China League One"

@dataclass
class OrganizationSportsteam(Entity):
    """Designates national or professional teams in various sports."""
    span: str  # Examples: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Swedish national men's ice hockey team"

@dataclass
class OtherAstronomything(Entity):
    """Refers to celestial objects, including planets, constellations, stars, and zodiac signs."""
    span: str  # Examples: "Zodiac", "Algol", "Caput Larvae", "42 Camelopardalis", "Sun"

@dataclass
class OtherAward(Entity):
    """Identifies titles of recognition, formal honors, medals, and awards."""
    span: str  # Examples: "Order of the Republic", "Grand Commander of the Order of the Niger", "Grammy", "European Car of the Year"

@dataclass
class OtherBiologything(Entity):
    """Represents biological components such as genes, proteins, domains, families, and insect orders."""
    span: str  # Examples: "Amphiphysin", "N-terminal", "lipid", "BAR domain", "p53 protein", "Hymenoptera"

@dataclass
class OtherChemicalthing(Entity):
    """Denotes chemical compounds and elements."""
    span: str  # Examples: "uranium", "carbon dioxide", "sulfur", "Carbon monoxide"

@dataclass
class OtherCurrency(Entity):
    """Refers to currency denominations and monetary units."""
    span: str  # Examples: "Travancore Rupee", "$", "Rs 25 lac crore"

@dataclass
class OtherDisease(Entity):
    """Identifies illnesses, medical conditions, and epidemic outbreaks."""
    span: str  # Examples: "Dysentery Epidemic", "hypothyroidism", "bladder cancer"

@dataclass
class OtherEducationaldegree(Entity):
    """Covers certifications and academic degrees."""
    span: str  # Examples: "BSc ( Hons ) in physics", "Master of Visual Studies", "Bachelor of Education", "Ph.D."

@dataclass
class OtherGod(Entity):
    """Represents creators, deities, and gods from mythological or religious traditions."""
    span: str  # Examples: "El", "Raijin", "Fujin", "Baglamukhi"

@dataclass
class OtherLanguage(Entity):
    """Denotes specific dialects or languages."""
    span: str  # Examples: "English", "Breton-speaking", "Latin", "Hebrew", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Refers to treaties, statutes, federal laws, and legislative acts."""
    span: str  # Examples: "United States Freedom Support Act", "Thirty Years' Peace", "America Invents Act"

@dataclass
class OtherLivingthing(Entity):
    """Identifies plants, animals, and various biological organisms."""
    span: str  # Examples: "monkeys", "insects", "patchouli", "Rafflesiaceae", "Euphorbiaceae"

@dataclass
class OtherMedical(Entity):
    """Covers pharmacological treatments, medical specialties, and procedures."""
    span: str  # Examples: "amitriptyline", "Pediatrics", "pediatrician", "cryoprecipitate"

@dataclass
class PersonActor(Entity):
    """Represents performers in television, theater, and film."""
    span: str  # Examples: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Fernando Rey", "Bajpayee"

@dataclass
class PersonArtistAuthor(Entity):
    """Refers to creators such as poets, musicians, authors, and writers."""
    span: str  # Examples: "George Axelrod", "Gaetano Donizetti", "Stephen King", "Deborah Lurie"

@dataclass
class PersonAthlete(Entity):
    """Identifies professional players, including quarterbacks, cyclists, and athletes."""
    span: str  # Examples: "Neville", "Tozawa", "Jaguar", "Bruno Zanoni", "Sam"

@dataclass
class PersonDirector(Entity):
    """Designates directors of theatrical, film, or artistic productions."""
    span: str  # Examples: "Richard Quine", "Bob Swaim", "Frank Darabont", "Jonze"

@dataclass
class PersonOther(Entity):
    """Includes individuals not falling into specific professional roles, such as notable family members or historical figures."""
    span: str  # Examples: "Holden", "Campbell", "Wallis", "Rockefeller", "Bette Davis"

@dataclass
class PersonPolitician(Entity):
    """Represents monarchs, political representatives, and government leaders."""
    span: str  # Examples: "Emeric", "Rivière", "William III", "Mary II", "Barack Obama"

@dataclass
class PersonScholar(Entity):
    """Refers to researchers, scientists, and academic experts."""
    span: str  # Examples: "Stalmine", "Stedman", "Wurdack", "Davis"

@dataclass
class PersonSoldier(Entity):
    """Identifies commanders and military personnel."""
    span: str  # Examples: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "Wolfe"

@dataclass
class ProductAirplane(Entity):
    """Denotes specific helicopter and airplane models."""
    span: str  # Examples: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Mil Mi-28"

@dataclass
class ProductCar(Entity):
    """Refers to automotive platforms and specific car models."""
    span: str  # Examples: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Fiat 128"

@dataclass
class ProductFood(Entity):
    """Identifies ingredients, food products, and particular varieties of crops."""
    span: str  # Examples: "V. labrusca", "yakiniku", "red grape"

@dataclass
class ProductGame(Entity):
    """Covers video games and their respective sequels."""
    span: str  # Examples: "Splinter Cell", "Airforce Delta", "Hardcore RPG"

@dataclass
class ProductOther(Entity):
    """Includes diverse items like technical components, museum artifacts, or miscellaneous products."""
    span: str  # Examples: "Fairbottom Bobs", "PDP-1", "X11", "E-mount"

@dataclass
class ProductShip(Entity):
    """Represents naval vessels, landing craft, and ships."""
    span: str  # Examples: "HMS Chinkara", "Congress", "Essex", "Embuscade"

@dataclass
class ProductSoftware(Entity):
    """Refers to programming tools, platforms, and computer software."""
    span: str  # Examples: "Wikipedia", "Apdf", "AmiPDF", "BIDS", "SQL Server"

@dataclass
class ProductTrain(Entity):
    """Identifies locomotive types and specific train models."""
    span: str  # Examples: "High Speed Trains", "55022 Royal Scots Grey", "Lexus CT 200h"

@dataclass
class ProductWeapon(Entity):
    """Designates military weapon systems, artillery, and firearms."""
    span: str  # Examples: "ZU-23-2M Wróbel", "AR-15", "M-14", "ZSU-57-2"

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