from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class ArtBroadcastprogram(Entity):
    """Describes radio or television productions, including episodic series like talk shows, mockumentaries, or dating programs."""
    span: str  # E.g.: "The Gale Storm Show", "12 Corazones", "Jonovision", "Trailer Park Boys", "3 Idiots"

@dataclass
class ArtFilm(Entity):
    """Covers cinematic pieces, encompassing full-length movies, television series or films, and screen adaptations."""
    span: str  # E.g.: "L'Atlantide", "The Shawshank Redemption", "Bosch", "Men in Her Diary"

@dataclass
class ArtMusic(Entity):
    """Pertains to musical works such as songs, albums, orchestral groups, symphonies, and individual recordings or live performances."""
    span: str  # E.g.: "Hollywood Studio Symphony", "Atkinson, Danko and Ford", "Champion Lover", "Mass in C minor", "Altenberg Lieder"

@dataclass
class ArtOther(Entity):
    """Includes varied artistic creations not fitting other groups, like music videos, fountains, and sculptures."""
    span: str  # E.g.: "Venus de Milo", "The Today Show", "Bleed Like Me", "Cloud Gate"

@dataclass
class ArtPainting(Entity):
    """Encompasses visual arts like graffiti and painting series. Also covers specific commercial lines such as camera lenses."""
    span: str  # E.g.: "Production/Reproduction", "Cofiwch Dryweryn", "Touit", "Loxia", "Batis", "Kamichama Karin"

@dataclass
class ArtWrittenart(Entity):
    """Relates to literary creations including novels, magazines, academic theses, scripts, and tragedies."""
    span: str  # E.g.: "Time", "The Seven Year Itch", "Imelda de ' Lambertazzi", "Rita Hayworth and Shawshank Redemption", "Writing, Teachers and Students in Graeco-Roman Egypt"

@dataclass
class BuildingAirport(Entity):
    """Refers to aviation hubs, including the entire airport site and specific terminals."""
    span: str  # E.g.: "Sheremetyevo International Airport", "London Luton Airport", "Newark Liberty International Airport", "Zhuhai Airport"

@dataclass
class BuildingHospital(Entity):
    """Represents healthcare sites like hospitals, medical clinics, and specialized centers for cancer treatment."""
    span: str  # E.g.: "Memorial Sloan-Kettering Cancer Center", "Yeungnam University Hospital", "Hokkaido University Hospital", "Huntington Hospital"

@dataclass
class BuildingHotel(Entity):
    """Covers lodging facilities such as grand hotels, resorts, and standard hotel accommodations."""
    span: str  # E.g.: "The Standard Hotel", "Radisson Blu Sea Plaza Hotel", "Flamingo Hotel", "Hotel Sacher Salzburg"

@dataclass
class BuildingLibrary(Entity):
    """Describes library facilities and archival institutions at the state or national level."""
    span: str  # E.g.: "Bayerische Staatsbibliothek", "British Library", "Berlin State Library", "Edmon Low Library", "National Library of Laos"

@dataclass
class BuildingOther(Entity):
    """Includes various physical edifices like churches, mansions, community centers, recording studios, and museums."""
    span: str  # E.g.: "Henry Ford Museum", "Communiplex", "Alpha Recording Studios", "Church of England parish church of St John The Evangelist", "Palazzo Monte dei Poveri Vergognosi"

@dataclass
class BuildingRestaurant(Entity):
    """Pertains to food service venues, including delis, restaurants, and dining halls."""
    span: str  # E.g.: "Trumbull dining hall", "Carnegie Deli", "Fatburger", "Morrison's"

@dataclass
class BuildingSportsfacility(Entity):
    """Encompasses athletic venues such as stadiums, sports arenas, and specialized fields or gardens."""
    span: str  # E.g.: "Boston Garden", "Sports Center", "Glenn Warner Soccer Facility", "Scotiabank Place"

@dataclass
class BuildingTheater(Entity):
    """Represents performance spaces like opera houses and theaters."""
    span: str  # E.g.: "Sanders Theatre", "Pittsburgh Civic Light Opera", "National Paris Opera", "Whitehall Theatre"

@dataclass
class EventAttackBattleWarMilitaryconflict(Entity):
    """Refers to formal military engagements, wars, battles, and specific combat operations."""
    span: str  # E.g.: "Vietnam War", "Easter Offensive", "Operation Zipper", "Battle of Romani", "World War I"

@dataclass
class EventDisaster(Entity):
    """Describes catastrophic occurrences like famines, earthquakes, plane crashes, and mining accidents."""
    span: str  # E.g.: "1693 Sicily earthquake", "1990s North Korean famine", "1912 North Mount Lyell Disaster", "Trigana Air Service Flight 267"

@dataclass
class EventElection(Entity):
    """Pertains to voting events, parliamentary terms, and legislative by-elections."""
    span: str  # E.g.: "March 1898 elections", "Elections to the European Parliament", "1982 Mitcham and Morden by-election", "1997-2001 parliament"

@dataclass
class EventOther(Entity):
    """Includes miscellaneous occurrences like crackdown operations, stage events, and political movements."""
    span: str  # E.g.: "Eastwood Scoring Stage", "Masaryk Democratic Movement", "Union for a Popular Movement", "Haq Movement"

@dataclass
class EventProtest(Entity):
    """Represents organized political or social resistance, such as boycotts, revolutions, and uprisings."""
    span: str  # E.g.: "Iranian Constitutional Revolution", "Bicentennial Boycott", "Iranian revolution", "Irish Rebellion of 1798"

@dataclass
class EventSportsevent(Entity):
    """Covers organized athletic competitions, tournaments, championships, and specific race rounds."""
    span: str  # E.g.: "2021 Stanley Cup", "1958 World Cup", "2008 National Champions", "Round 3/Race 9"

@dataclass
class LocationGpe(Entity):
    """Describes Geo-Political Entities like cities, nations, provinces, states, and regional territories."""
    span: str  # E.g.: "Republic of Croatia", "Mediterranean Basin", "Near East", "Cornwall", "Dearborn", "Michigan"

@dataclass
class LocationBodiesofwater(Entity):
    """Represents aquatic features, whether natural or artificial, like rivers, dams, seas, and lakes."""
    span: str  # E.g.: "Atatürk Dam Lake", "Arthur Kill", "Norfolk coast", "East China Sea", "Jordan River"

@dataclass
class LocationIsland(Entity):
    """Refers to land surrounded by water, encompassing archipelagos, islands, and peninsulas."""
    span: str  # E.g.: "Samsat district", "Staten Island", "Laccadives", "Maldives", "Mainland", "Shetland"

@dataclass
class LocationMountain(Entity):
    """Includes geographic heights such as ridges, mountain ranges, peaks, and glaciers."""
    span: str  # E.g.: "Ruweisat Ridge", "Salamander Glacier", "Mount Diablo", "K2", "Himalayan", "Karakoram"

@dataclass
class LocationOther(Entity):
    """Pertains to diverse locations like specific travel routes, estates, and geographic landmarks."""
    span: str  # E.g.: "Cartuther", "Victoria line", "Cley next the Sea", "Camino Palmero", "Big Meadows"

@dataclass
class LocationPark(Entity):
    """Encompasses protected areas like city parks, national parks, and historic community zones."""
    span: str  # E.g.: "Gramercy Park", "Painted Desert Community Complex", "Shenandoah National Park", "Millennium Park"

@dataclass
class LocationRoadRailwayHighwayTransit(Entity):
    """Describes transportation infrastructure like highways, rail lines, bridges, and roads."""
    span: str  # E.g.: "Newark-Elizabeth Rail Link", "Friern Barnet Road", "North Jersey Coast Line", "Outerbridge Crossing"

@dataclass
class OrganizationCompany(Entity):
    """Represents commercial businesses, record labels, corporate groups, and fast food franchises."""
    span: str  # E.g.: "Church's Chicken", "WHL", "Two Pesos, Inc.", "Taco Cabana, Inc.", "Warner Brothers"

@dataclass
class OrganizationEducation(Entity):
    """Includes institutions of higher learning like colleges, universities, and specific academic faculties."""
    span: str  # E.g.: "Belfast Royal Academy", "MIT", "Barnard College", "Latvia University of Life Sciences and Technologies"

@dataclass
class OrganizationGovernmentGovernmentagency(Entity):
    """Refers to state bodies, parliaments, courts, and law enforcement agencies at the federal or local level."""
    span: str  # E.g.: "Supreme Court", "Congregazione dei Nobili", "Diet", "US Park Police", "US Postal Police"

@dataclass
class OrganizationMediaNewspaper(Entity):
    """Represents media platforms, periodicals, TV networks, and online information sites."""
    span: str  # E.g.: "Al Jazeera", "Clash", "TimeOut Melbourne", "Nickelodeon", "Wikipedia"

@dataclass
class OrganizationOther(Entity):
    """Includes varied groups such as military divisions, international agencies, armies, and non-profit entities."""
    span: str  # E.g.: "IAEA", "4th Army", "SS Division Nordland", "Defence Sector C"

@dataclass
class OrganizationPoliticalparty(Entity):
    """Describes established political organizations and partisan groups."""
    span: str  # E.g.: "Shimpotō", "Kenseitō", "Al Wafa ' Islamic party", "National Liberal Party", "Republican"

@dataclass
class OrganizationReligion(Entity):
    """Pertains to religious denominations, faith groups, theological schools, and scriptural traditions."""
    span: str  # E.g.: "Jewish", "Christian", "Episcopalians", "United Methodists", "United Church of Christ"

@dataclass
class OrganizationShoworganization(Entity):
    """Covers groups in the performing arts, such as music bands and symphony orchestras."""
    span: str  # E.g.: "Mr. Mister", "Yeah Yeah Yeahs", "Bochumer Symphoniker"

@dataclass
class OrganizationSportsleague(Entity):
    """Describes professional or amateur athletic leagues and their component divisions."""
    span: str  # E.g.: "First Division", "China League One", "NHL", "Bundesliga"

@dataclass
class OrganizationSportsteam(Entity):
    """Represents athletic teams, national squads, and professional racing groups."""
    span: str  # E.g.: "Arsenal", "Tottenham", "Luc Alphand Aventures", "Swedish national men's ice hockey team", "Audi"

@dataclass
class OtherAstronomything(Entity):
    """Refers to celestial bodies and astronomical notions like planets, stars, constellations, and zodiac signs."""
    span: str  # E.g.: "Zodiac", "Algol", "42 Camelopardalis", "Sun", "Tandun III"

@dataclass
class OtherAward(Entity):
    """Represents honors, prizes, and distinctions for accomplishments in science, national service, or the arts."""
    span: str  # E.g.: "Order of the Republic of Guinea", "Grammy", "European Car of the Year", "Kodansha Manga Award"

@dataclass
class OtherBiologything(Entity):
    """Encompasses biological components like proteins, genes, cell cycle stages, and taxonomic orders."""
    span: str  # E.g.: "Amphiphysin", "p53 protein", "Ismaridae", "G0 phase", "Rb"

@dataclass
class OtherChemicalthing(Entity):
    """Describes chemical substances including elements, gases, and compounds."""
    span: str  # E.g.: "uranium", "carbon dioxide", "sulfur", "Carbon monoxide"

@dataclass
class OtherCurrency(Entity):
    """Represents monetary denominations and currency units."""
    span: str  # E.g.: "Travancore Rupee", "$", "Rs 25 lac crore", "Aruban florin", "Netherlands Antillean guilder"

@dataclass
class OtherDisease(Entity):
    """Includes illnesses, syndromes, medical conditions, and large-scale epidemics."""
    span: str  # E.g.: "French Dysentery Epidemic of 1779", "hypothyroidism", "bladder cancer", "Septic shock"

@dataclass
class OtherEducationaldegree(Entity):
    """Refers to academic diplomas, degrees, and scholarly titles."""
    span: str  # E.g.: "BSc ( Hons ) in physics", "Master of Visual Studies", "Bachelor of Education", "Ph.D .", "Medical Degree"

@dataclass
class OtherGod(Entity):
    """Represents divine beings, deities, and religious figures considered holy."""
    span: str  # E.g.: "El", "Raijin", "Fujin", "Baglamukhi", "Jesus"

@dataclass
class OtherLanguage(Entity):
    """Covers specific human languages and linguistic families."""
    span: str  # E.g.: "Hebrew", "Breton-speaking", "Latin", "English", "Arabic"

@dataclass
class OtherLaw(Entity):
    """Pertains to legal statutes, international treaties, acts, and specific legislative clauses."""
    span: str  # E.g.: "United States Freedom Support Act", "Thirty Years ' Peace", "Leahy–Smith America Invents Act", "Rush–Bagot Treaty"

@dataclass
class OtherLivingthing(Entity):
    """Describes non-human life forms, including animals, plants, and taxonomic families."""
    span: str  # E.g.: "monkeys", "insects", "patchouli", "Rafflesiaceae", "zebras"

@dataclass
class OtherMedical(Entity):
    """Includes medical disciplines, surgical procedures, drug treatments, and health-related actions."""
    span: str  # E.g.: "amitriptyline", "Pediatrics", "cryoprecipitate", "heart transplants"

@dataclass
class PersonActor(Entity):
    """Refers to people known for acting in stage, television, or film productions."""
    span: str  # E.g.: "Ellaline Terriss", "Edmund Payne", "Tchéky Karyo", "Fernando Rey", "Bajpayee"

@dataclass
class PersonArtistAuthor(Entity):
    """Encompasses creators like writers, composers, novelists, and lyricists."""
    span: str  # E.g.: "George Axelrod", "Gaetano Donizetti", "Deborah Lurie", "Stephen King", "Karen O"

@dataclass
class PersonAthlete(Entity):
    """Represents individuals in sports, including professional players and racers."""
    span: str  # E.g.: "Neville", "Tozawa", "Jaguar", "Bruno Zanoni", "Ernie Johnson"

@dataclass
class PersonDirector(Entity):
    """Describes individuals who lead the production of films, plays, or TV shows."""
    span: str  # E.g.: "Richard Quine", "Bob Swaim", "Frank Darabont", "Costner"

@dataclass
class PersonOther(Entity):
    """Includes individuals not in specific professional categories, such as fictional characters or members of notable families."""
    span: str  # E.g.: "Holden", "Olympia Elizabeth", "Wallis", "Rockefeller", "Binion"

@dataclass
class PersonPolitician(Entity):
    """Represents royalty and political figures, such as monarchs, presidents, and legislators."""
    span: str  # E.g.: "Emeric", "William III", "Mary II", "Gillis Long", "Barack Obama"

@dataclass
class PersonScholar(Entity):
    """Refers to academics, professors, researchers, and individuals distinguished by their intellectual work."""
    span: str  # E.g.: "Stedman", "Wurdack", "Davis", "Ted Robert Gurr"

@dataclass
class PersonSoldier(Entity):
    """Includes military staff such as commanders, generals, and troops."""
    span: str  # E.g.: "Krukenberg", "Helmuth Weidling", "Bruno Loerzer", "Sir James Outram"

@dataclass
class ProductAirplane(Entity):
    """Represents aviation vehicles like fighter jets, helicopters, and specific plane models."""
    span: str  # E.g.: "EC135T2 CPDS", "FGR.2s", "Mil Mi-58", "Su-30", "WC-135"

@dataclass
class ProductCar(Entity):
    """Pertains to motor vehicles, particular car models, and automotive chassis."""
    span: str  # E.g.: "Rolls-Royce Phantom", "Corvettes", "Renault 12", "Lancia Thema 8.32"

@dataclass
class ProductFood(Entity):
    """Encompasses types of food, specific dishes, wines, and grape varieties."""
    span: str  # E.g.: "V. labrusca", "yakiniku", "red grape", "Merlot", "Cabernet Sauvignon"

@dataclass
class ProductGame(Entity):
    """Represents video games, role-playing game systems, and electronic consoles."""
    span: str  # E.g.: "Splinter Cell", "Airforce Delta", "RPG", "Game Boy Advance", "Game Boy Micro"

@dataclass
class ProductOther(Entity):
    """Includes assorted products like hardware, machine parts, and cryptographic devices."""
    span: str  # E.g.: "Fairbottom Bobs", "PDP-1", "X11", "SecurID 800"

@dataclass
class ProductShip(Entity):
    """Refers to maritime craft, including naval frigates, submarines, and landing vessels."""
    span: str  # E.g.: "HMS Chinkara", "Congress", "Essex", "Embuscade", "Alvin"

@dataclass
class ProductSoftware(Entity):
    """Represents software programs, programming languages, and tools for developers."""
    span: str  # E.g.: "Wikipedia", "Apdf", "BIDS Helper", "micro-PROLOG", "SQL Server"

@dataclass
class ProductTrain(Entity):
    """Includes railway vehicles like locomotives, train sets, and specific high-speed models."""
    span: str  # E.g.: "High Speed Trains", "55022 Royal Scots Grey", "Lexus CT 200h", "Keystone Service"

@dataclass
class ProductWeapon(Entity):
    """Represents military hardware such as rifles, guns, and artillery systems."""
    span: str  # E.g.: "ZU-23-2M Wróbel", "AR-15", "ZSU-57-2", "40mm Bofors gun"

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