from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Covers radio and television shows, such as sitcoms, talk programs, and series."""
    span: str  # Examples: "The Gale Storm Show", "12 Corazones", "Street Cents", "Jonovision", "Trailer Park Boys"

@dataclass
class ArtFilm(Entity):
    """Denotes cinematic works or motion pictures across all genres."""
    span: str  # Examples: "L'Atlantide", "The Shawshank Redemption", "Bosch"

@dataclass
class ArtMusic(Entity):
    """Pertains to compositions, albums, musical acts, or symphonies."""
    span: str  # Examples: "Hollywood Studio Symphony", "Atkinson, Danko and Ford", "Champion Lover", "Sex"

@dataclass
class ArtOther(Entity):
    """Includes varied artistic creations or shows not fitting specific classes, such as sculptures or music videos."""
    span: str  # Examples: "Venus de Milo", "The Today Show", "Bleed Like Me"

@dataclass
class ArtPainting(Entity):
    """Consists of visual arts such as paintings, street art, or particular photographic lens series."""
    span: str  # Examples: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Loxia", "Batis"

@dataclass
class ArtWrittenart(Entity):
    """Represents literary productions including books, journals, theatrical scripts, and operas."""
    span: str  # Examples: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Rita Hayworth and Shawshank Redemption"

@dataclass
class BuildingAirport(Entity):
    """Pertains to air travel hubs and flight terminals."""
    span: str  # Examples: "Sheremetyevo International Airport", "London Luton Airport", "Newark Liberty International Airport"

@dataclass
class BuildingHospital(Entity):
    """Covers healthcare facilities, clinics, and medical institutions."""
    span: str  # Examples: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Hokkaido University Hospital"

@dataclass
class BuildingHotel(Entity):
    """Refers to accommodation venues and hospitality establishments."""
    span: str  # Examples: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel"

@dataclass
class BuildingLibrary(Entity):
    """Denotes book collections, journal archives, and libraries."""
    span: str  # Examples: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library"

@dataclass
class BuildingOther(Entity):
    """Includes diverse architectural sites like galleries, recording spaces, or sacred buildings not categorized elsewhere."""
    span: str  # Examples: "Henry Ford Museum", "Communiplex", "Alpha Recording Studios", "Saint Matthew Church"

@dataclass
class BuildingRestaurant(Entity):
    """Represents eateries, cafes, and delicatessens."""
    span: str  # Examples: "Trumbull", "Carnegie Deli", "Fatburger"

@dataclass
class BuildingSportsfacility(Entity):
    """Covers athletic arenas, sports complexes, and stadiums."""
    span: str  # Examples: "Boston Garden", "Sports Center", "Glenn Warner Soccer Facility"

@dataclass
class BuildingTheater(Entity):
    """Refers to performance spaces, opera houses, and venues for the performing arts."""
    span: str  # Examples: "Sanders Theatre", "Pittsburgh Civic Light Opera", "National Paris Opera"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Pertains to armed skirmishes, military campaigns, and historic wars."""
    span: str  # Examples: "Vietnam War", "Easter Offensive", "Operation Zipper", "Battle of Romani"

@dataclass
class EventDisaster(Entity):
    """Includes calamities of natural or human origin, such as famines or industrial accidents."""
    span: str  # Examples: "1693 Sicily earthquake", "North Korean famine", "1912 North Mount Lyell Disaster"

@dataclass
class EventElection(Entity):
    """Denotes governmental voting processes, by-elections, and parliamentary polls."""
    span: str  # Examples: "March 1898 elections", "Elections to the European Parliament", "Mitcham and Morden by-election"

@dataclass
class EventOther(Entity):
    """Covers various happenings, social movements, or sequences not specifically categorized."""
    span: str  # Examples: "Eastwood Scoring Stage", "Masaryk Democratic Movement", "Union for a Popular Movement"

@dataclass
class EventProtest(Entity):
    """Represents social uprisings, organized boycotts, and civil protests."""
    span: str  # Examples: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Iranian revolution"

@dataclass
class EventSportsevent(Entity):
    """Refers to athletic tournaments, title matches, and competitive series."""
    span: str  # Examples: "Stanley Cup", "World Cup", "National Champions"

@dataclass
class LocationGpe(Entity):
    """Covers political regions such as nations, municipalities, and provinces."""
    span: str  # Examples: "Croatian", "Republic of Croatia", "Mediterranean Basin", "Cornwall", "Los Angeles"

@dataclass
class LocationBodiesofwater(Entity):
    """Denotes aquatic features like reservoirs, coastlines, and waterways."""
    span: str  # Examples: "Atatürk Dam Lake", "Arthur Kill", "Norfolk coast"

@dataclass
class LocationIsland(Entity):
    """Pertains to landmasses surrounded by water or island-based districts."""
    span: str  # Examples: "Samsat", "Staten Island", "Laccadives", "Maldives"

@dataclass
class LocationMountain(Entity):
    """Includes geographic features like peaks, mountain ranges, and glaciers."""
    span: str  # Examples: "Ruweisat Ridge", "Miteirya Ridge", "Salamander Glacier", "Mount Diablo"

@dataclass
class LocationOther(Entity):
    """Represents general sites, transit lines, or areas not fitting other labels."""
    span: str  # Examples: "Cartuther", "Victoria line", "Northern City Line", "West Gate Bridge"

@dataclass
class LocationPark(Entity):
    """Refers to recreational parks, protected wilderness areas, or historic zones."""
    span: str  # Examples: "Gramercy Park", "Painted Desert Community Complex", "Shenandoah National Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Denotes transportation routes, subway systems, and transit corridors."""
    span: str  # Examples: "NJT", "Newark-Elizabeth Rail Link", "Friern Barnet Road", "North Jersey Coast Line"

@dataclass
class OrganizationCompany(Entity):
    """Represents corporate entities, firms, and commercial franchises."""
    span: str  # Examples: "Church's Chicken", "Two Pesos, Inc.", "Taco Cabana, Inc.", "WHL"

@dataclass
class OrganizationEducation(Entity):
    """Includes academic institutions, colleges, and learning academies."""
    span: str  # Examples: "Belfast Royal Academy", "Ulster College of Physical Education", "MIT", "Barnard College"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Covers judicial bodies, legislative assemblies, and state agencies."""
    span: str  # Examples: "Supreme Court", "Congregazione dei Nobili", "Diet", "New York City Council"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Refers to journalism outlets, periodicals, and broadcasting networks."""
    span: str  # Examples: "Al Jazeera", "Clash", "TimeOut Melbourne", "Fuse"

@dataclass
class OrganizationOther(Entity):
    """Pertains to miscellaneous groups like military units, divisions, or international consortia."""
    span: str  # Examples: "IAEA", "4th Army", "SS Division Nordland"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Denotes organized political factions and parties."""
    span: str  # Examples: "Shimpotō", "Al Wafa' Islamic party", "National Liberal Party"

@dataclass
class OrganizationReligion(Entity):
    """Covers faith-based communities, churches, and sectarian schools."""
    span: str  # Examples: "Jewish", "Christian", "Catholic Church", "non-denominational Christian"

@dataclass
class OrganizationShoworganization(Entity):
    """Represents performing groups, orchestras, and entertainment ensembles."""
    span: str  # Examples: "Mr. Mister", "Lizzy", "Bochumer Symphoniker", "Yeah Yeah Yeahs"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to athletic associations, divisions, and professional sports circuits."""
    span: str  # Examples: "First Division", "NHL", "China League One"

@dataclass
class OrganizationSportsteam(Entity):
    """Denotes national or professional-level athletic squads."""
    span: str  # Examples: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Swedish national men's ice hockey team"

@dataclass
class OtherAstronomything(Entity):
    """Includes astronomical objects such as stars, planets, and astrological signs."""
    span: str  # Examples: "Zodiac", "Algol", "Caput Larvae", "42 Camelopardalis", "Sun"

@dataclass
class OtherAward(Entity):
    """Refers to prizes, formal decorations, medals, and titles of distinction."""
    span: str  # Examples: "Order of the Republic", "Grand Commander of the Order of the Niger", "Grammy", "European Car of the Year"

@dataclass
class OtherBiologything(Entity):
    """Covers biological components like genes, proteins, domains, and taxonomic orders."""
    span: str  # Examples: "Amphiphysin", "N-terminal", "lipid", "BAR domain", "p53 protein", "Hymenoptera"

@dataclass
class OtherChemicalthing(Entity):
    """Represents atomic elements and molecular compounds."""
    span: str  # Examples: "uranium", "carbon dioxide", "sulfur", "Carbon monoxide"

@dataclass
class OtherCurrency(Entity):
    """Denotes monetary forms and financial denominations."""
    span: str  # Examples: "Travancore Rupee", "$", "Rs 25 lac crore"

@dataclass
class OtherDisease(Entity):
    """Pertains to ailments, health disorders, and widespread outbreaks."""
    span: str  # Examples: "Dysentery Epidemic", "hypothyroidism", "bladder cancer"

@dataclass
class OtherEducationaldegree(Entity):
    """Includes university certifications and scholastic credentials."""
    span: str  # Examples: "BSc ( Hons ) in physics", "Master of Visual Studies", "Bachelor of Education", "Ph.D."

@dataclass
class OtherGod(Entity):
    """Refers to divine figures and gods from theological or mythological traditions."""
    span: str  # Examples: "El", "Raijin", "Fujin", "Baglamukhi"

@dataclass
class OtherLanguage(Entity):
    """Represents distinct tongues or regional dialects."""
    span: str  # Examples: "English", "Breton-speaking", "Latin", "Hebrew", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Covers legislation, treaties, federal acts, and legal mandates."""
    span: str  # Examples: "United States Freedom Support Act", "Thirty Years' Peace", "America Invents Act"

@dataclass
class OtherLivingthing(Entity):
    """Includes flora, fauna, and various biological organisms."""
    span: str  # Examples: "monkeys", "insects", "patchouli", "Rafflesiaceae", "Euphorbiaceae"

@dataclass
class OtherMedical(Entity):
    """Refers to healthcare disciplines, clinical methods, and pharmaceutical drugs."""
    span: str  # Examples: "amitriptyline", "Pediatrics", "pediatrician", "cryoprecipitate"

@dataclass
class PersonActor(Entity):
    """Denotes individuals acting in cinematic, theatrical, or television productions."""
    span: str  # Examples: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Fernando Rey", "Bajpayee"

@dataclass
class PersonArtistAuthor(Entity):
    """Represents literary creators, writers, poets, and musical composers."""
    span: str  # Examples: "George Axelrod", "Gaetano Donizetti", "Stephen King", "Deborah Lurie"

@dataclass
class PersonAthlete(Entity):
    """Includes pro-level athletes, competitors, and sports stars."""
    span: str  # Examples: "Neville", "Tozawa", "Jaguar", "Bruno Zanoni", "Sam"

@dataclass
class PersonDirector(Entity):
    """Refers to individuals overseeing artistic productions, plays, or films."""
    span: str  # Examples: "Richard Quine", "Bob Swaim", "Frank Darabont", "Jonze"

@dataclass
class PersonOther(Entity):
    """Pertains to people outside specific professions, like historical or family figures."""
    span: str  # Examples: "Holden", "Campbell", "Wallis", "Rockefeller", "Bette Davis"

@dataclass
class PersonPolitician(Entity):
    """Denotes heads of state, monarchs, and political representatives."""
    span: str  # Examples: "Emeric", "Rivière", "William III", "Mary II", "Barack Obama"

@dataclass
class PersonScholar(Entity):
    """Represents researchers, intellectuals, and scientific experts."""
    span: str  # Examples: "Stalmine", "Stedman", "Wurdack", "Davis"

@dataclass
class PersonSoldier(Entity):
    """Covers soldiers, combatants, and high-ranking military officers."""
    span: str  # Examples: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "Wolfe"

@dataclass
class ProductAirplane(Entity):
    """Refers to distinct types of planes and helicopters."""
    span: str  # Examples: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Mil Mi-28"

@dataclass
class ProductCar(Entity):
    """Represents automotive makes and vehicle platforms."""
    span: str  # Examples: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Fiat 128"

@dataclass
class ProductFood(Entity):
    """Includes edible goods, ingredients, and specific plant varieties."""
    span: str  # Examples: "V. labrusca", "yakiniku", "red grape"

@dataclass
class ProductGame(Entity):
    """Denotes electronic games and their sequels."""
    span: str  # Examples: "Splinter Cell", "Airforce Delta", "Hardcore RPG"

@dataclass
class ProductOther(Entity):
    """Covers varied manufactured goods, technical parts, or museum exhibits."""
    span: str  # Examples: "Fairbottom Bobs", "PDP-1", "X11", "E-mount"

@dataclass
class ProductShip(Entity):
    """Pertains to watercraft, ships, and naval transport."""
    span: str  # Examples: "HMS Chinkara", "Congress", "Essex", "Embuscade"

@dataclass
class ProductSoftware(Entity):
    """Represents digital applications, computing platforms, and coding utilities."""
    span: str  # Examples: "Wikipedia", "Apdf", "AmiPDF", "BIDS", "SQL Server"

@dataclass
class ProductTrain(Entity):
    """Refers to locomotive types and specific rail car models."""
    span: str  # Examples: "High Speed Trains", "55022 Royal Scots Grey", "Lexus CT 200h"

@dataclass
class ProductWeapon(Entity):
    """Includes military weaponry, guns, and combat systems."""
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