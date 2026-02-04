from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Covers radio broadcasts, television shows, and episodic programs across different formats, including talk shows, dating series, or mockumentaries."""
    span: str  # Examples: "The Gale Storm Show", "12 Corazones", "Jonovision", "Trailer Park Boys", "3 Idiots"

@dataclass
class ArtFilm(Entity):
    """Denotes cinematic productions, encompassing feature films, motion pictures, adaptations, and television series."""
    span: str  # Examples: "L'Atlantide", "The Shawshank Redemption", "Bosch", "Men in Her Diary"

@dataclass
class ArtMusic(Entity):
    """Pertains to musical works such as songs, albums, symphonies, orchestras, and recorded performances."""
    span: str  # Examples: "Hollywood Studio Symphony", "Atkinson, Danko and Ford", "Champion Lover", "Mass in C minor", "Altenberg Lieder"

@dataclass
class ArtOther(Entity):
    """Identifies miscellaneous artistic creations like music videos, sculptures, or fountains not categorized elsewhere."""
    span: str  # Examples: "Venus de Milo", "The Today Show", "Bleed Like Me", "Cloud Gate"

@dataclass
class ArtPainting(Entity):
    """Comprises visual arts like paintings and graffiti, as well as specific product lines such as camera lenses."""
    span: str  # Examples: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Loxia", "Batis", "Kamichama Karin"

@dataclass
class ArtWrittenart(Entity):
    """Includes literary works, for instance, novels, magazines, academic papers, and scripts."""
    span: str  # Examples: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Rita Hayworth and Shawshank Redemption", "Writing, Teachers and Students in Graeco-Roman Egypt"

@dataclass
class BuildingAirport(Entity):
    """Designates aviation hubs, including terminals and the broader airport infrastructure."""
    span: str  # Examples: "Sheremetyevo International Airport", "London Luton Airport", "Newark Liberty International Airport", "Zhuhai Airport"

@dataclass
class BuildingHospital(Entity):
    """Signifies healthcare facilities like clinics, general hospitals, and specialized medical centers."""
    span: str  # Examples: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Hokkaido University Hospital", "Huntington Hospital"

@dataclass
class BuildingHotel(Entity):
    """Includes lodging establishments like hotels, resorts, and large-scale guest accommodations."""
    span: str  # Examples: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel", "Hotel Sacher Salzburg"

@dataclass
class BuildingLibrary(Entity):
    """Refers to archival institutions and libraries at the state or national level."""
    span: str  # Examples: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library", "National Library of Laos"

@dataclass
class BuildingOther(Entity):
    """Covers diverse structures such as recording studios, museums, community halls, mansions, and religious buildings."""
    span: str  # Examples: "Henry Ford Museum", "Communiplex", "Alpha Recording Studios", "Church of England parish church of St John The Evangelist", "Palazzo Monte dei Poveri Vergognosi"

@dataclass
class BuildingRestaurant(Entity):
    """Represents eateries where meals are provided, like restaurants, delis, and dining facilities."""
    span: str  # Examples: "Trumbull dining hall", "Carnegie Deli", "Fatburger", "Morrison's"

@dataclass
class BuildingSportsfacility(Entity):
    """Encompasses athletic venues, including sports arenas, stadiums, and specialized physical activity centers."""
    span: str  # Examples: "Boston Garden", "Sports Center", "Glenn Warner Soccer Facility", "Scotiabank Place"

@dataclass
class BuildingTheater(Entity):
    """Refers to performance spaces such as opera houses and theaters."""
    span: str  # Examples: "Sanders Theatre", "Pittsburgh Civic Light Opera", "National Paris Opera", "Whitehall Theatre"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Denotes armed conflicts, including wars, battles, and specific military offensives."""
    span: str  # Examples: "Vietnam War", "Easter Offensive", "Operation Zipper", "Battle of Romani", "World War I"

@dataclass
class EventDisaster(Entity):
    """Identifies major catastrophes like aviation crashes, earthquakes, famines, or mining accidents."""
    span: str  # Examples: "1693 Sicily earthquake", "1990s North Korean famine", "1912 North Mount Lyell Disaster", "Trigana Air Service Flight 267"

@dataclass
class EventElection(Entity):
    """Covers organized balloting processes, including by-elections and specific legislative terms."""
    span: str  # Examples: "March 1898 elections", "Elections to the European Parliament", "1982 Mitcham and Morden by-election", "1997-2001 parliament"

@dataclass
class EventOther(Entity):
    """Includes miscellaneous occurrences like political movements or events held on professional stages."""
    span: str  # Examples: "Eastwood Scoring Stage", "Masaryk Democratic Movement", "Union for a Popular Movement", "Haq Movement"

@dataclass
class EventProtest(Entity):
    """Represents systematic social resistance, such as rebellions, boycotts, and revolutions."""
    span: str  # Examples: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Iranian revolution", "Irish Rebellion of 1798"

@dataclass
class EventSportsevent(Entity):
    """Pertains to athletic competitions, including tournaments, championships, and specific races."""
    span: str  # Examples: "2021 Stanley Cup", "1958 World Cup", "2008 National Champions", "Round 3/Race 9"

@dataclass
class LocationGpe(Entity):
    """Refers to geopolitical entities, for example, cities, countries, provinces, and states."""
    span: str  # Examples: "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall", "Dearborn", "Michigan"

@dataclass
class LocationBodiesofwater(Entity):
    """Designates natural or artificial aquatic features like rivers, dams, lakes, and seas."""
    span: str  # Examples: "Atatürk Dam Lake", "Arthur Kill", "Norfolk coast", "East China Sea", "Jordan River"

@dataclass
class LocationIsland(Entity):
    """Denotes land surrounded by water, such as archipelagos, peninsulas, and islands."""
    span: str  # Examples: "Samsat district", "Staten Island", "Laccadives", "Maldives", "Mainland", "Shetland"

@dataclass
class LocationMountain(Entity):
    """Includes geographical elevations like mountain ranges, glaciers, and peaks."""
    span: str  # Examples: "Ruweisat Ridge", "Salamander Glacier", "Mount Diablo", "K2", "Himalayan", "Karakoram"

@dataclass
class LocationOther(Entity):
    """Represents various geographic points of interest, transit paths, or estates."""
    span: str  # Examples: "Cartuther", "Victoria line", "Cley next the Sea", "Camino Palmero", "Big Meadows"

@dataclass
class LocationPark(Entity):
    """Signifies designated green spaces, including national parks, city parks, and historical districts."""
    span: str  # Examples: "Gramercy Park", "Painted Desert Community Complex", "Shenandoah National Park", "Millennium Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Covers transportation infrastructure, such as highways, railways, bridges, and transit routes."""
    span: str  # Examples: "Newark-Elizabeth Rail Link", "Friern Barnet Road", "North Jersey Coast Line", "Outerbridge Crossing"

@dataclass
class OrganizationCompany(Entity):
    """Refers to commercial enterprises, including record labels, corporate entities, and fast-food chains."""
    span: str  # Examples: "Church's Chicken", "WHL", "Two Pesos, Inc.", "Taco Cabana, Inc.", "Warner Brothers"

@dataclass
class OrganizationEducation(Entity):
    """Includes academic institutions such as colleges, universities, and specific school departments."""
    span: str  # Examples: "Belfast Royal Academy", "MIT", "Barnard College", "Latvia University of Life Sciences and Technologies"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Denotes governmental bodies, including legislative assemblies, courts, and law enforcement agencies."""
    span: str  # Examples: "Supreme Court", "Congregazione dei Nobili", "Diet", "US Park Police", "US Postal Police"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Represents news organizations, including newspapers, digital platforms, magazines, and TV networks."""
    span: str  # Examples: "Al Jazeera", "Clash", "TimeOut Melbourne", "Nickelodeon", "Wikipedia"

@dataclass
class OrganizationOther(Entity):
    """Covers miscellaneous groups like military units, international organizations, and non-profits."""
    span: str  # Examples: "IAEA", "4th Army", "SS Division Nordland", "Defence Sector C"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Identifies organized political groups and parties."""
    span: str  # Examples: "Shimpotō", "Kenseitō", "Al Wafa ' Islamic party", "National Liberal Party", "Republican"

@dataclass
class OrganizationReligion(Entity):
    """Pertains to religious affiliations, including denominations, schools, and faith traditions."""
    span: str  # Examples: "Jewish", "Christian", "Episcopalians", "United Methodists", "United Church of Christ"

@dataclass
class OrganizationShoworganization(Entity):
    """Includes musical groups, symphony orchestras, and performing arts ensembles."""
    span: str  # Examples: "Mr. Mister", "Yeah Yeah Yeahs", "Bochumer Symphoniker"

@dataclass
class OrganizationSportsleague(Entity):
    """Refers to competitive sports leagues and their internal divisions."""
    span: str  # Examples: "First Division", "China League One", "NHL", "Bundesliga"

@dataclass
class OrganizationSportsteam(Entity):
    """Represents athletic squads, national teams, and professional racing groups."""
    span: str  # Examples: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Swedish national men's ice hockey team", "Audi"

@dataclass
class OtherAstronomything(Entity):
    """Designates astronomical entities and concepts like planets, constellations, and stars."""
    span: str  # Examples: "Zodiac", "Algol", "42 Camelopardalis", "Sun", "Tandun III"

@dataclass
class OtherAward(Entity):
    """Signifies honors and prizes awarded for accomplishments in fields like science, art, or public service."""
    span: str  # Examples: "Order of the Republic of Guinea", "Grammy", "European Car of the Year", "Kodansha Manga Award"

@dataclass
class OtherBiologything(Entity):
    """Includes biological elements such as genes, proteins, and taxonomic orders."""
    span: str  # Examples: "Amphiphysin", "p53 protein", "Ismaridae", "G0 phase", "Rb"

@dataclass
class OtherChemicalthing(Entity):
    """Refers to chemical substances, including gases, compounds, and elements."""
    span: str  # Examples: "uranium", "carbon dioxide", "sulfur", "Carbon monoxide"

@dataclass
class OtherCurrency(Entity):
    """Represents monetary units and specific currency names."""
    span: str  # Examples: "Travancore Rupee", "$", "Rs 25 lac crore", "Aruban florin", "Netherlands Antillean guilder"

@dataclass
class OtherDisease(Entity):
    """Covers medical ailments, including syndromes, diseases, and epidemics."""
    span: str  # Examples: "French Dysentery Epidemic of 1779", "hypothyroidism", "bladder cancer", "Septic shock"

@dataclass
class OtherEducationaldegree(Entity):
    """Denotes academic qualifications, including diplomas and degrees."""
    span: str  # Examples: "BSc ( Hons ) in physics", "Master of Visual Studies", "Bachelor of Education", "Ph.D .", "Medical Degree"

@dataclass
class OtherGod(Entity):
    """Pertains to divine beings, deities, and sacred historical figures."""
    span: str  # Examples: "El", "Raijin", "Fujin", "Baglamukhi", "Jesus"

@dataclass
class OtherLanguage(Entity):
    """Includes various languages and their respective linguistic families."""
    span: str  # Examples: "Hebrew", "Breton-speaking", "Latin", "English", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Refers to legal frameworks, including treaties, acts, and specific legislative sections."""
    span: str  # Examples: "United States Freedom Support Act", "Thirty Years ' Peace", "Leahy–Smith America Invents Act", "Rush–Bagot Treaty"

@dataclass
class OtherLivingthing(Entity):
    """Represents non-human living organisms like plants, animals, and biological families."""
    span: str  # Examples: "monkeys", "insects", "patchouli", "Rafflesiaceae", "zebras"

@dataclass
class OtherMedical(Entity):
    """Covers medical fields, pharmacological agents, and healthcare procedures."""
    span: str  # Examples: "amitriptyline", "Pediatrics", "cryoprecipitate", "heart transplants"

@dataclass
class PersonActor(Entity):
    """Refers to performers known for their roles in theater, film, or television."""
    span: str  # Examples: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Fernando Rey", "Bajpayee"

@dataclass
class PersonArtistAuthor(Entity):
    """Includes creative individuals such as authors, lyricists, composers, and writers."""
    span: str  # Examples: "George Axelrod", "Gaetano Donizetti", "Deborah Lurie", "Stephen King", "Karen O"

@dataclass
class PersonAthlete(Entity):
    """Designates individuals in sports, including racers and professional players."""
    span: str  # Examples: "Neville", "Tozawa", "Jaguar", "Bruno Zanoni", "Ernie Johnson"

@dataclass
class PersonDirector(Entity):
    """Pertains to individuals directing theatrical productions, movies, or TV shows."""
    span: str  # Examples: "Richard Quine", "Bob Swaim", "Frank Darabont", "Costner"

@dataclass
class PersonOther(Entity):
    """Includes people not categorized by profession, such as character names or members of well-known families."""
    span: str  # Examples: "Holden", "Olympia Elizabeth", "Wallis", "Rockefeller", "Binion"

@dataclass
class PersonPolitician(Entity):
    """Represents political figures and royalty, including presidents, monarchs, and legislators."""
    span: str  # Examples: "Emeric", "William III", "Mary II", "Gillis Long", "Barack Obama"

@dataclass
class PersonScholar(Entity):
    """Refers to intellectuals, including researchers, professors, and scholars."""
    span: str  # Examples: "Stedman", "Wurdack", "Davis", "Ted Robert Gurr"

@dataclass
class PersonSoldier(Entity):
    """Signifies military members, including soldiers, commanders, and generals."""
    span: str  # Examples: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "Sir James Outram"

@dataclass
class ProductAirplane(Entity):
    """Includes aircraft like helicopters, planes, and fighter jets."""
    span: str  # Examples: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Su-30", "WC-135"

@dataclass
class ProductCar(Entity):
    """Refers to motor vehicles, encompassing specific car models and platforms."""
    span: str  # Examples: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Lancia Thema 8.32"

@dataclass
class ProductFood(Entity):
    """Represents culinary items, including food types, wines, and grape varieties."""
    span: str  # Examples: "V. labrusca", "yakiniku", "red grape", "Merlot", "Cabernet Sauvignon"

@dataclass
class ProductGame(Entity):
    """Covers games like RPGs, video games, and gaming hardware."""
    span: str  # Examples: "Splinter Cell", "Airforce Delta", "RPG", "Game Boy Advance", "Game Boy Micro"

@dataclass
class ProductOther(Entity):
    """Includes diverse products such as machine parts, hardware, and cryptographic tools."""
    span: str  # Examples: "Fairbottom Bobs", "PDP-1", "X11", "SecurID 800"

@dataclass
class ProductShip(Entity):
    """Refers to watercraft, including submersibles, frigates, and landing ships."""
    span: str  # Examples: "HMS Chinkara", "Congress", "Essex", "Embuscade", "Alvin"

@dataclass
class ProductSoftware(Entity):
    """Signifies computer software, including programming languages and applications."""
    span: str  # Examples: "Wikipedia", "Apdf", "BIDS Helper", "micro-PROLOG", "SQL Server"

@dataclass
class ProductTrain(Entity):
    """Pertains to rail vehicles like locomotives and high-speed train models."""
    span: str  # Examples: "High Speed Trains", "55022 Royal Scots Grey", "Lexus CT 200h", "Keystone Service"

@dataclass
class ProductWeapon(Entity):
    """Includes military weaponry like artillery, rifles, and firearms."""
    span: str  # Examples: "ZU-23-2M Wróbel", "AR-15", "ZSU-57-2", "40mm Bofors gun"

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